import os
import sys
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from google import genai

# Load environment variables
load_dotenv()

# Konfigurasi API Key secara global (Sintaks yang benar untuk google.generativeai)
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

sys.path.append(os.path.abspath("."))
sys.path.append(os.path.abspath("./fetchers"))

from fetchers.fundamental import get_fundamentals
from fetchers.market import makeTable

def promptUser1():
    inputText = str(input("What coin do you want to analyze? (Solana, Bitcoin, Ethereum etc): "))
    return inputText.lower().strip()

def jalankan_gemini():
    console = Console()
    
    # Validasi API Key
    if not os.environ.get("GEMINI_API_KEY"):
        console.print("[bold red]Error: GEMINI_API_KEY tidak ditemukan di environment atau file .env![/bold red]")
        return

    inputText = promptUser1()
    
    console.print("Meminta data fundamental dan market, serta menunggu respon AI...")
    
    try:
        # Panggil fetcher
        data_fundamental = str(get_fundamentals(ids=inputText))
        data_market = str(makeTable().tail(5))
        
        # Susun prompt menjadi satu string utuh
        prompt = (
            f"Analyze this data and give me a summary of the coin's performance: {data_fundamental} "
            f"along with this market data: {data_market} "
            "and give a 1 signal from that data with Target profit and Stop lose"
        )
        response = client.models.generate_content(
                    model="gemini-3.1-flash",
                    contents=prompt
                )

        markdown_response = Markdown(response.text)

        console.print("\n[bold green]Gemini responds:[/bold green]\n")
        console.print(markdown_response)
        
    except Exception as e:
        console.print(f"[bold red]Terjadi kesalahan saat memproses AI: {e}[/bold red]")

if __name__ == "__main__":
    jalankan_gemini()