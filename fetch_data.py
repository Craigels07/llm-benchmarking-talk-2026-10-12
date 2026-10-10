"""Fetch LLM benchmark data from Artificial Analysis and cache it in data/models.json.

Usage: python fetch_data.py [--all]
The API key is read from the AA_API_KEY environment variable or from .env.
"""

import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

PROVIDERS = ["openai", "anthropic"]  # model_creator slugs to keep
API_URL = "https://artificialanalysis.ai/api/v2/data/llms/models"
SOURCE = "https://artificialanalysis.ai/"
ROOT = Path(__file__).parent
OUTPUT = ROOT / "data" / "models.json"


def read_api_key():
    key = os.environ.get("AA_API_KEY")
    env_file = ROOT / ".env"
    if not key and env_file.exists():
        for line in env_file.read_text().splitlines():
            name, _, value = line.partition("=")
            if name.strip() == "AA_API_KEY":
                key = value.strip().strip("\"'")
    if not key:
        sys.exit("AA_API_KEY not found. Set it in the environment or in .env")
    return key


def fetch_models(key):
    request = urllib.request.Request(
        API_URL, headers={"x-api-key": key, "User-Agent": "llm-benchmark-chart"}
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.load(response)["data"]
    except urllib.error.HTTPError as error:
        sys.exit(f"API request failed: HTTP {error.code} {error.reason}")
    except urllib.error.URLError as error:
        sys.exit(f"API request failed: {error.reason}")


def flatten(model):
    evaluations = model["evaluations"]
    pricing = model["pricing"]
    return {
        "id": model["id"],
        "name": model["name"],
        "slug": model["slug"],
        "provider": model["model_creator"]["name"],
        "provider_slug": model["model_creator"]["slug"],
        "release_date": model["release_date"],
        "intelligence": evaluations["artificial_analysis_intelligence_index"],
        "coding": evaluations["artificial_analysis_coding_index"],
        "math": evaluations["artificial_analysis_math_index"],
        "cost_blended": pricing["price_1m_blended_3_to_1"],
        "cost_input": pricing["price_1m_input_tokens"],
        "cost_output": pricing["price_1m_output_tokens"],
        "speed_tps": model["median_output_tokens_per_second"],
        "ttft_s": model["median_time_to_first_token_seconds"],
        "ttfat_s": model["median_time_to_first_answer_token"],
    }


def main():
    models = fetch_models(read_api_key())
    if "--all" not in sys.argv:
        models = [m for m in models if m["model_creator"]["slug"] in PROVIDERS]
    result = {
        "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source": SOURCE,
        "models": [flatten(m) for m in models],
    }
    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(json.dumps(result, separators=(",", ":")))
    print(f"Wrote {len(result['models'])} models to {OUTPUT}")


main()
