"""Currency converter CLI using the free Frankfurter exchange-rate API."""
import argparse
import json
import sys
import time
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

API = "https://api.frankfurter.app"
CACHE = Path.home() / ".currency_cli_cache.json"
CACHE_TTL = 3600


def _fetch(path: str) -> dict:
    with urlopen(f"{API}{path}", timeout=10) as response:
        return json.load(response)
