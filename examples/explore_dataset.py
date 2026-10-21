#!/usr/bin/env python3
"""Small usage example: explore the public metadata without contacting external services."""
import json
from pathlib import Path
from collections import Counter
root = Path(__file__).resolve().parents[1]
w1 = json.loads((root/'data/v1.0/wp1_knowledge.json').read_text(encoding='utf-8'))
w2 = json.loads((root/'data/v1.0/wp2_benchmark.json').read_text(encoding='utf-8'))
print('WP1 knowledge records:',len(w1['records']))
print('WP2 approved items:',len(w2['items']))
print('Modules:',dict(sorted(Counter(e['item']['module_id'] for e in w2['items']).items())))
print('Task profiles:',dict(sorted(Counter(e['item']['task_profile'] for e in w2['items']).items())))
