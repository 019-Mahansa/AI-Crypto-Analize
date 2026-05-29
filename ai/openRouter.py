from openai import OpenAI
import os
import sys
from dotenv import load_dotenv
load_dotenv()

from rich.console import Console
from rich.markdown import Markdown

console = Console()

sys.path.append(os.path.abspath("."))
sys.path.append(os.path.abspath("./fetchers"))

from fetchers.fundamental import get_fundamentals
from fetchers.market import makeTable


client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=os.getenv("OPENROUTER_API"),
)

def promptUser1():
  inputText = str(input("What coin do you want to analyze? (Solana, Bitcoin, Ethereum etc) "))
  return(inputText.lower().strip())

inputText = promptUser1()

response = client.chat.completions.create(
  model="google/gemini-2.0-flash-lite-001",
  messages=[
          {
            "role": "user",
            "content": "Analayze this data and give me a summary of the coin's performance: " + str(get_fundamentals(ids=inputText)) + "along with this market data: " + str(makeTable().tail(5)) + "and give a 1 signal from that data with Target profit and Stop lose"
          }
        ],
  extra_body={"reasoning": {"enabled": True}}
)

markdown_response = Markdown(response.choices[0].message.content)


console.print("Ai responds:\n")
console.print(markdown_response)
