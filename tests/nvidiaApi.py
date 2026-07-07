from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# Inisialisasi OpenAI client ke NVIDIA API
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.environ.get("NVIDIA_API_KEY")
)

completion = client.chat.completions.create(
    model="z-ai/glm-5.2", 
    messages=[{
        "role": "user", 
        "content": "write me a code in python to make an triangle!"
    }],
    temperature=1,
    top_p=0.95,
    max_tokens=4080,
    stream=False 
)

print(completion.choices[0].message.content)