import os
import sys
from datetime import date

from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from google import genai

load_dotenv()

today_dates = date.today()

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

sys.path.append(os.path.abspath("."))
sys.path.append(os.path.abspath("./fetchers"))

from fetchers.fundamental import get_fundamentals
from fetchers.market import makeTable
from fetchers.news import news_search
from RAG.technicalSignal import build_rag_prompt


def promptUser1():
    inputText = str(input("What coin do you want to analyze? (Solana, Bitcoin, Ethereum etc): "))
    return inputText.lower().strip()


def jalankan_gemini():
    console = Console()

    if not os.environ.get("GEMINI_API_KEY"):
        console.print("[bold red]Error: GEMINI_API_KEY is not founded in environment or env file![/bold red]")
        return

    inputText = promptUser1()
    
    console.print("your AI is working right now please wait ..")
    
    try:

        data_fundamental = str(get_fundamentals(ids=inputText))
        market_df = makeTable().tail(30)
        news = str(news_search())

        # Build RAG prompt (includes automated technical summary)
        prompt = build_rag_prompt(data_fundamental, market_df, news)

        response = client.models.generate_content(
                    model="gemini-3.5-flash",
                    contents=prompt
                )

        markdown_response = Markdown(response.text)

        console.print("\n[bold green]Gemini responds:[/bold green]\n")
        console.print(markdown_response)
        
    except Exception as e:
        console.print(f"[bold red]There is a mistake from the AI: {e}[/bold red]")


if __name__ == "__main__":
    jalankan_gemini()
