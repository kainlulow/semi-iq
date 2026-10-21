#!/usr/bin/env python3
"""Demonstrate the minimal allowed model-facing payload. Does NOT call an LLM."""
import json
from pathlib import Path
root = Path(__file__).resolve().parents[1]
data = json.loads((root/'data/v1.0/wp2_benchmark.json').read_text(encoding='utf-8'))
item = data['items'][0]['item']
payload = {key:item[key] for key in ('question','input_data','assumptions')}
# IMPORTANT: Do not supply answer/rubric/criteria/provenance in the evaluated model context.
print(json.dumps(payload,ensure_ascii=False,indent=2))
