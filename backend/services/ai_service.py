import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"

def should_save_memory(message):

    prompt = f"""
You are a strict memory classifier.

Your job is to decide whether a message should be saved as a LONG-TERM MEMORY.

Save ONLY personal information such as:

- Name
- Age
- Birthday
- Address
- City
- Country
- College
- School
- Job
- Profession
- Favourite things
- Likes
- Dislikes
- Goals
- Hobbies
- Skills
- Languages
- Family members
- Daily routine

DO NOT save:

- Questions
- Homework
- PDF questions
- General knowledge
- Greetings
- Requests
- Commands
- Conversations
- Temporary information

Examples:

"My name is John." -> YES

"I live in Delhi." -> YES

"My favourite language is Python." -> YES

"I wake up at 6 AM." -> YES

"What subjects are in Semester V?" -> NO

"Who is the first man on the moon?" -> NO

"2+2?" -> NO

"Hello" -> NO

Reply ONLY with YES or NO.

Message:
{message}
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }
    )

    data = response.json()

    return data["response"].strip().upper().startswith("YES")

def ask_llama(prompt):

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()