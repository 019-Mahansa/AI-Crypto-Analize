import os
import sys
from datetime import date

from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from openai import OpenAI

load_dotenv()

today_dates = date.today()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API"), 
)

sys.path.append(os.path.abspath("."))
sys.path.append(os.path.abspath("./fetchers"))
# sys.path.append(os.path.abspath("./tests"))

from fetchers.fundamental import get_fundamentals
from fetchers.market import makeTable
from fetchers.news import news_search
from RAG.technicalSignal import build_rag_prompt

def promptUser1():
    inputText = str(input("What coin do you want to analyze? (Solana, Bitcoin, Ethereum etc): "))
    return inputText.lower().strip()

def jalankan_openrouter():
    console = Console()

    if not os.environ.get("OPENROUTER_API"):
        console.print("[bold red]Error: OPENROUTER_API_KEY is not found in environment or env file![/bold red]")
        return

    inputText = promptUser1()
    
    console.print("Your AI is working right now please wait ..")
    
    try:
        data_fundamental = str(get_fundamentals(ids=inputText))
        market_df = makeTable().tail(30)
        news = str(news_search())

        # Build RAG prompt (includes automated technical summary)
        prompt = build_rag_prompt(data_fundamental, market_df, news)

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b:free", 
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        ai_response_text = response.choices[0].message.content
        markdown_response = Markdown(ai_response_text)

        console.print("\n[bold green]AI responds:[/bold green]\n")
        console.print(markdown_response)
        
    except Exception as e:
        console.print(f"[bold red]There is a mistake from the AI: {e}[/bold red]")

if __name__ == "__main__":
    jalankan_openrouter()
