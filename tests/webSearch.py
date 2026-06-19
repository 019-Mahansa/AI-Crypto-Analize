# first_automation.py
import os
from dotenv import load_dotenv
from tinyfish import TinyFish, CompleteEvent

load_dotenv()
client = TinyFish()  # Reads TINYFISH_API_KEY from environment


def news_search():
    with client.agent.stream(
        url="https://www.google.com",
        goal=(
            "Search on Google for: 'site:bloombergtechnoz.com macro economics crypto'"
            "Find 5 relevant news articles published within the last 1 week regarding international macroeconomics "
            "and its impact on cryptocurrency. "
            "For each article found, click the link or extract a deep, comprehensive summary. "
            "The 'description' field MUST be a detailed, long paragraph (at least 3-5 sentences) explaining the context, "
            "the macroeconomic factors involved (e.g., interest rates, inflation), and the exact impact on crypto. "
            "Return the output as a JSON array of objects, where each object contains: "
            "'title', 'description' (long & detailed), and 'release_date'."
        ),
    ) as stream:
        for event in stream:
                print(f"⏳ [Status]: Searching news... ({type(event).__name__})")
                

                # if hasattr(event, 'streaming_url') and event.streaming_url:
                #     print(f"🔗 LIHAT LIVE PROGRESS DI SINI: {event.streaming_url}")
                #     print("--------------------------------------------------")


                if isinstance(event, CompleteEvent):
                    print("\n✅ SELESAI! Ini hasilnya:")
                    return event.result_json