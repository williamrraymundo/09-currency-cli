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


def get_rate(base: str, target: str) -> float:
    """Return the exchange rate, using a one-hour on-disk cache."""
    key = f"{base}->{target}"
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    entry = cache.get(key)
    if entry and time.time() - entry["time"] < CACHE_TTL:
        return entry["rate"]

    data = _fetch(f"/latest?from={base}&to={target}")
    rate = data["rates"][target]
    cache[key] = {"rate": rate, "time": time.time()}
    CACHE.write_text(json.dumps(cache))
    return rate


def list_currencies() -> dict:
    return _fetch("/currencies")


def convert(amount: float, base: str, target: str) -> float:
    if base == target:
        return amount
    return amount * get_rate(base, target)


def build_parser() -> argparse.ArgumentParser:
