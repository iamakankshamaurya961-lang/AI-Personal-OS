from backend.services.ai_service import ask_llama

def summarize_email(body):

    prompt = f"""
You are an email assistant.

Summarize this email in 5 bullet points.

Email:

{body}
"""

    result = ask_llama(prompt)

    return result["response"]
def generate_email_reply(body):

    prompt = f"""
You are an AI Email Assistant.

Write a professional and natural reply to the following email.

Rules:
- Be polite and concise.
- Directly address the email.
- Do not invent information.
- Do not add a subject.
- Return only the reply body.

Email:

{body}
"""

    result = ask_llama(prompt)

    return result["response"]