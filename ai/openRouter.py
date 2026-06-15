from openai import OpenAI
import os
import sys
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown

# Load 
load_dotenv()

sys.path.append(os.path.abspath("."))
sys.path.append(os.path.abspath("./fetchers"))

from fetchers.fundamental import get_fundamentals
from fetchers.market import makeTable

def promptUser1():
    inputText = str(input("What coin do you want to analyze? (Solana, Bitcoin, Ethereum etc): "))
    return inputText.lower().strip()


def jalankan_openrouter():
    console = Console()
    

    api_key = os.getenv("OPENROUTER_API")
    if not api_key:
        console.print("[bold red]Error: OPENROUTER_API tidak ditemukan di file .env![/bold red]")
        return

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    inputText = promptUser1()
    
    console.print("Meminta data fundamental dan market, serta menunggu respon AI...")
    
    try:
        # Panggil fetcher
        data_fundamental = str(get_fundamentals(ids=inputText))
        data_market = str(makeTable().tail(5))
        
        response = client.chat.completions.create(
            model="qwen/qwen3.5-9b",
            messages=[
                {
                    "role": "user",
                    "content": "Analyze this data and give me a summary of the coin's performance: " + data_fundamental + " along with this market data: " + data_market + " and give a 1 signal from that data with Target profit and Stop lose"
                }
            ],
            extra_body={"reasoning": {"enabled": True}}
        )

        markdown_response = Markdown(response.choices[0].message.content)

        console.print("\n[bold green]Ai responds:[/bold green]\n")
        console.print(markdown_response)
        
    except Exception as e:
        console.print(f"[bold red]Terjadi kesalahan saat memproses AI: {e}[/bold red]")
