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

from fetchers.fundamental import get_fundamentals
from fetchers.market import makeTable

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
        data_market = str(makeTable().tail(30))
        
        prompt = (
prompt = (
    "You are a World-Class Crypto Market Analyst and Quantitative Strategist. "
    "Your task is to analyze the provided data, synthesize macro/micro news, and generate a precise trading signal.\n\n"
    
    "### DATA TO ANALYZE:\n"
    f"- Fundamental Data: {data_fundamental}\n"
    f"- Market & Technical Data: {data_market}\n"
    f"- Target Date Range (Today & 1 Week Prior): {today_dates}\n\n"
    
    "### INSTRUCTIONS:\n"
    "1. Analyze the technical indicators (RSI, Stochastic, SMAs, Volume) and identify the current short-term trend.\n"
    "2. Evaluate how the recent macro/micro economic news (from the past week up to today) impacts this specific coin. Look for any divergence between macro sentiment and technical realities.\n"
    "3. Based on the confluence of data, generate EXACTLY ONE high-probability trading signal (Long or Short).\n"
    "4. Determine the Entry price, Stop-Loss (SL), and Take-Profit (TP) based on the support/resistance levels visible in the data. Ensure the Risk-to-Reward (R/R) ratio is at least 1:2.\n\n"
    
    "### OUTPUT FORMAT (Strictly Respond in Markdown):\n"
    "## 1. Market Snapshot & Technical View\n"
    "[Provide a concise bullet-point summary of the technical indicators and trend]\n\n"
    
    "## 2. Macro & Micro Narrative Impact\n"
    "[Summarize how recent news influences the coin's price action]\n\n"
    
    "## 3. Trading Signal Setup\n"
    "- **Position Type**: [Long / Short]\n"
    "- **Entry Price**: [$\n"
    "- **Stop-Loss (SL)**: [$\n"
    "- **Take-Profit (TP)**: [$\n"
    "- **Risk/Reward Ratio**: [e.g., 1:2.15]\n"
    "- **Rationale**: [Provide a 3-bullet point justification combining technicals and macro factors]\n"
    "- **Key Monitoring Points**: [Invalidation triggers or volume conditions]"
)
        )

        response = client.chat.completions.create(
            model="qwen/qwen3.6-plus", 
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