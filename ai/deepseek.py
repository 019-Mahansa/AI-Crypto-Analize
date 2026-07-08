from openai import OpenAI
import os
import sys
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown


load_dotenv()

sys.path.append(os.path.abspath("."))
sys.path.append(os.path.abspath("./fetchers"))

from fetchers.fundamental import get_fundamentals
from fetchers.market import makeTable
from fetchers.news import news_search
from RAG.technicalSignal import build_rag_prompt


def promptUser1():
    inputText = str(input("What coin do you want to analyze? (Solana, Bitcoin, Ethereum etc): "))
    return inputText.lower().strip()


def jalankan_openrouter():
    console = Console()
    

    api_key = os.getenv("DEEPSEEK_API")
    if not os.environ.get("DEEPSEEK_API"):
        console.print("[bold red]Error: DEEPSEEK_API is not found in environment or env file![/bold red]")
        return

    console.print("Your AI is working right now please wait ..")

    client = OpenAI(
        base_url="https://api.deepseek.com",
        api_key=api_key,
    )

    inputText = promptUser1()
    
    console.print("Meminta data fundamental dan market, serta menunggu respon AI...")
    
    try:
        data_fundamental = str(get_fundamentals(ids=inputText))
        market_df = makeTable().tail(30)
        news = str(news_search())
        
        # Build RAG prompt (includes automated technical summary)
        prompt = build_rag_prompt(data_fundamental, market_df, news)

        response = client.chat.completions.create(
            model="deepseek-v4-flash",
            messages= prompt,
            stream=False,
            reasoning_effort="high",
            extra_body={"thinking": {"type": "enabled"}}
        )

        markdown_response = Markdown(response.choices[0].message.content)

        console.print("\n[bold green]Ai responds:[/bold green]\n")
        console.print(markdown_response)
        
    except Exception as e:
        console.print(f"[bold red]There is a mistake from the AI: {e}[/bold red]")

if __name__ == "__main__":
    jalankan_openrouter()