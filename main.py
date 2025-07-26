import requests
from bs4 import BeautifulSoup
import json
import time
from generate_letter import generate_cover_letter
import os

def load_sent_jobs():
    if not os.path.exists("sent_jobs.json"):
        return set()
    with open("sent_jobs.json", "r") as f:
        return set(json.load(f))

def save_sent_jobs(sent):
    with open("sent_jobs.json", "w") as f:
        json.dump(list(sent), f, indent=2)

def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

def load_resume():
    with open("resume.txt", "r") as f:
        return f.read()

def load_template():
    with open("template.txt", "r") as f:
        return f.read()

def search_jobs_google(keyword, location):
    return ["https://www.linkedin.com/jobs/view/3924571423/"]  # реальная вакансия QA Engineer

def extract_job_description(url):
    try:
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(resp.text, "html.parser")
        paragraphs = soup.find_all("p")
        text = "\n".join(p.get_text(strip=True) for p in paragraphs)
        return text[:3000]  # Обрезаем, чтобы GPT не утонул
    except:
        return "No description available."

def send_telegram_message(bot_token, chat_id, text):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

def main():
    print("🚀 Скрипт запущен")
    config = load_config()
    resume = load_resume()
    template = load_template()
    sent_jobs = load_sent_jobs()

    for keyword in config["keywords"]:
        print(f"🔍 Ищу вакансии по ключу: {keyword}")
        links = search_jobs_google(keyword, config["location"])
        print(f"🔗 Найдено ссылок: {len(links)}")

        for link in links:
            if link in sent_jobs:
                print(f"⚠️ Уже отправляли: {link}")
                continue  # пропускаем дубликаты

            print(f"➡️ Обрабатываю: {link}")
            job_description = extract_job_description(link)
            print(f"📄 Получено описание длиной {len(job_description)} символов")

            letter = generate_cover_letter(keyword, job_description, resume, template)
            print("✉️ Письмо сгенерировано")

            message = f"🔎 Вакансия по ключевому слову *{keyword}*:\n{link}"
            send_telegram_message(config["telegram_bot_token"], config["telegram_chat_id"], message)
            time.sleep(1)
            send_telegram_message(config["telegram_bot_token"], config["telegram_chat_id"], f"✉️ Черновик письма:\n\n{letter}")
            time.sleep(2)

            sent_jobs.add(link)
            save_sent_jobs(sent_jobs)


if __name__ == "__main__":
    main()
