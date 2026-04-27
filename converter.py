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
    parser = argparse.ArgumentParser(description="Convert between currencies.")
    parser.add_argument("amount", type=float, nargs="?", help="Amount to convert")
    parser.add_argument("base", nargs="?", help="Source currency, e.g. USD")
    parser.add_argument("target", nargs="?", help="Target currency, e.g. BRL")
    parser.add_argument("--list", action="store_true", help="List supported currencies")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.list:
            for code, name in list_currencies().items():
                print(f"{code}  {name}")
            return 0
        if args.amount is None or not args.base or not args.target:
            print("usage: converter.py AMOUNT BASE TARGET", file=sys.stderr)
            return 2
        base, target = args.base.upper(), args.target.upper()
        result = convert(args.amount, base, target)
        print(f"{args.amount:,.2f} {base} = {result:,.2f} {target}")
        return 0
    except (URLError, KeyError) as error:
        print(f"Could not fetch exchange rates: {error}", file=sys.stderr)
        return 1

