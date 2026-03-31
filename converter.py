"""Currency converter CLI using the free Frankfurter exchange-rate API."""
import argparse
import json
import sys
import time
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

