from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=os.getenv("OPENROUTER_API"),
)

response = client.chat.completions.create(
  model="anthropic/claude-3-haiku",
  messages=[
          {
            "role": "user",
            "content": "give me code of a simple python function that adds two numbers"
          }
        ],
  extra_body={"reasoning": {"enabled": True}}
)

response = response.choices[0].message
print("Assistant's response:", response.content)