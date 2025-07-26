import openai
import json

def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

def generate_cover_letter(job_title, job_description, resume_text, template_text):
    config = load_config()
    client = openai.OpenAI(api_key=config["openai_api_key"])

    prompt = f"""
You are a helpful assistant that writes personalized cover letters.

Use the template and resume below to write a cover letter for the following job:

Job Title:
{job_title}

Job Description:
{job_description}

Resume:
{resume_text}

Template:
{template_text}

Respond with a complete cover letter ready to be sent.
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response.choices[0].message.content
