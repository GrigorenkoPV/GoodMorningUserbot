#!/usr/bin/env bash
set -euxo pipefail

cd "$(dirname "$0")"/..

python3 -m venv venv
source venv/bin/atcivate
pip install -r requirements.txt
exec python -m userbot
