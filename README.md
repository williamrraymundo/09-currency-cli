# Currency Converter CLI

> Command-line currency converter using live exchange rates with caching.

## Features

- Live rates from the free Frankfurter API
- One-hour on-disk cache
- `--list` shows supported currencies
- No third-party dependencies

## Tech stack

Python 3.10+, Frankfurter API

## Getting started

```bash
python converter.py 100 USD BRL
python converter.py --list
```
