#!/usr/bin/env python3
"""Validate the cleaned V1.0.0 public distribution (stdlib only)."""
import collections
import csv
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

root=Path(__file__).resolve().parents[1]
def read(f):return json.loads((root/f).read_text(encoding='utf-8'))
def packaged(path):return '.git' not in path.relative_to(root).parts
w1=read('data/v1.0/wp1_knowledge.json');w2=read('data/v1.0/wp2_benchmark.json')
manifest=read('metadata/release_manifest.json');summary=read('metadata/content_summary.json')
records=w1['records'];entries=w2['items']
assert manifest['release_id']=='semi-iq-v1.0.0'
assert w2['project']['title']=='SemiIQ'
assert len(records)==225==manifest['wp1_count']==summary['wp1_records']
assert len(entries)==769==manifest['wp2_item_count']==summary['wp2_items']
assert w1['schema_version']=='WP1-PUBLIC-V1.0' and w2['schema_version']=='WP2-PUBLIC-V1.0'
assert all(d['dataset_release']['approval_status']=='Approved' and d['dataset_release']['distribution']=='public-release' for d in (w1,w2))
assert manifest['distribution_status']=='GITHUB_PUBLIC_DISTRIBUTION_READY'
if '--require-publication-ready' in sys.argv:
 assert manifest['distribution_status']=='GITHUB_PUBLIC_DISTRIBUTION_READY', 'GitHub publication gate BLOCKED: unresolved source-reference/locator verification'
 assert manifest.get('source_traceability',{}).get('reference_locator_named_work_conflicts_pending')==0, 'GitHub publication gate BLOCKED: outstanding evidence checks'
 assert manifest.get('source_traceability',{}).get('evidence_verification_complete') is True, 'GitHub publication gate BLOCKED: source evidence verification incomplete'
assert manifest['licenses']['dataset_and_documentation']=='CC-BY-NC-4.0'
assert manifest['licenses']['software']=='PolyForm-Noncommercial-1.0.0'
representative='Kain Lu Low, acting on behalf of the authorized licensors'
assert manifest['licensing_representative']==representative
for f in ['LICENSE','LICENSE-DATA','LICENSE-SOFTWARE','LICENSING.md','COMMERCIAL-LICENSING.md','CONTRIBUTORS.md','ACKNOWLEDGMENTS.md','CITATION.cff']:
 assert (root/f).is_file(),f
assert 'creativecommons.org/licenses/by-nc/4.0/legalcode.en' in (root/'LICENSE-DATA').read_text()
assert 'polyformproject.org/licenses/noncommercial/1.0.0' in (root/'LICENSE-SOFTWARE').read_text()
for f in ['LICENSE','LICENSE-DATA','LICENSE-SOFTWARE','LICENSING.md','COMMERCIAL-LICENSING.md','README.md','RELEASE_NOTES.md']:
 text=(root/f).read_text()
 assert 'Kain Lu Low' in text and 'acting on behalf of the authorized licensors' in text,('Missing licensing representative',f)

# Public attribution has no per-record contributor fields. Check centralized credits
# against the requested dataset citation (stdlib-only for dependency-free CI).
contributors_text=(root/'CONTRIBUTORS.md').read_text(encoding='utf-8')
citation_text=(root/'CITATION.cff').read_text(encoding='utf-8')
assert 'title: "SemiIQ"' in citation_text
assert 'repository-code: "https://github.com/kainlulow/semi-iq"' in citation_text
contributor_pattern=re.compile(r'^\|\s*([^|]+?)\s*\|\s*\[`([^`]+)`\]\((https://github\.com/[^)\s]+)\)\s*\|\s*$',re.M)
contributor_rows=[(name.strip(),handle,url) for name,handle,url in contributor_pattern.findall(contributors_text)]
assert contributor_rows, 'No contributor rows found in CONTRIBUTORS.md'
assert len(set(contributor_rows))==len(contributor_rows),'Duplicate CONTRIBUTORS.md entries'
for name,handle,url in contributor_rows:
 assert url.rstrip('/').split('/')[-1]==handle,(name,handle,url)

# Extract the supported plain-scalar CFF 1.2 author fields without a YAML dependency.
citation_lines=citation_text.splitlines()
assert 'authors:' in citation_lines,'CITATION.cff must contain authors:'
start=citation_lines.index('authors:')+1
citation_rows=[]
author={}
for line in citation_lines[start:]:
 if line and not line.startswith(' '):break
 if line.startswith('  - '):
  if author:citation_rows.append(author)
  author={}
  field_line=line[4:].strip()
 elif line.startswith('    '):field_line=line.strip()
 else:continue
 match=re.fullmatch(r'(family-names|given-names|website):\s*(.+)',field_line)
 if match:
  raw_value=match.group(2).strip()
  value=json.loads(raw_value) if raw_value.startswith('"') else raw_value
  assert match.group(1) not in author,('Duplicate author field',match.group(1))
  author[match.group(1)]=value
if author:citation_rows.append(author)
assert citation_rows,'No CITATION.cff authors found'
assert all({'family-names','given-names','website'}<=set(a) for a in citation_rows),'Incomplete CITATION.cff author'
citation_credits=[(f"{a['given-names']} {a['family-names']}",a['website']) for a in citation_rows]
public_credits=[(name,url) for name,handle,url in contributor_rows]
assert citation_credits==public_credits,("CONTRIBUTORS.md and CITATION.cff names, GitHub profiles, or author order do not match",public_credits,citation_credits)
assert len(set(citation_credits))==len(citation_credits),'Duplicate CITATION.cff authors'

w1_remove={'contributor','notes','review_status','reviewer_comments','intended_use'}
w2_remove={'student_owner','review_status','reviewer_comments','dataset_quality_warning','created_at','status','structural_validation','schema_version','domain','version'}
for d in (w1,w2):
 assert not ({'interface_version','review'} & set(d))
 assert 'internal_workflow_metadata' not in d['dataset_release']
index={r['record_id']:r for r in records}
assert len(index)==len(records)
for r in records:
 assert not (w1_remove & set(r)),r['record_id']
 assert r['source_reference'] and r['source_locator']
 assert r['module_id'] in {'SEM','DEV','MAT','PRO','SIM','ENG'}
ids=set();criterion_keys=set();criterion_count=0
for e in entries:
 item,link,criteria=e['item'],e['wp1_link'],e['criteria'];identifier=item['item_id']
 assert identifier not in ids,identifier
 ids.add(identifier)
 assert not (w2_remove & set(item)),identifier
 assert 'review_status' not in link
 assert item['primary_wp1_record_id'] in index,identifier
 wp=index[item['primary_wp1_record_id']]
 for left,right in [('record_id','primary_wp1_record_id'),('module_id','module_id'),('module_name','module_name'),('subdomain_id','subdomain_id'),('subdomain_name','subdomain_name'),('knowledge_title','wp1_knowledge_title')]:
  assert link[left]==item[right]==wp[left],(identifier,left)
 for key in ('question','reference_answer','rubric','source_reference','source_locator'):
  assert item[key],(identifier,key)
 assert all(key in item for key in ('input_data','assumptions'))
 assert float(item['maximum_score'])>0
 criterion_count+=len(criteria)
 for c in criteria:
  assert c['item_id']==identifier
  ckey=(identifier,c['criterion_id']); assert ckey not in criterion_keys;criterion_keys.add(ckey)
  assert float(c['points'])>=0
  assert 'score_anchors' in c and ('grading_policy' in c or 'aggregation' in c)
  assert not re.search(r'PROPOSED SCORING CONTENT|GENERATOR-VERIFIED CANDIDATE|NOT (?:HUMAN|FORMAL) APPROV',str(c.get('approved_evidence','')),re.I),(identifier,c['criterion_id'])
 if item['task_profile']!='expert_only':
  assert abs(sum(float(c['points']) for c in criteria)-float(item['maximum_score']))<1e-7,identifier
 for key in ('source_reference','source_locator'):
  assert not re.search(r'local authorized mirror|SHA-256\s+[0-9a-f]{64}|Original bibliographic attribution:|directly inspected',item[key],re.I),(identifier,key)
assert criterion_count==1247==manifest['scoring_criterion_count']==summary['scoring_criteria']

# Release-specific task, rubric, and scoring-alignment checks.
by_item_id={e['item']['item_id']:e for e in entries}
pattern=by_item_id['WP2-PRO-PATTERN-0126']
assert pattern['item']['task_profile']=='conceptual_rubric'
assert pattern['item']['task_type']=='Reasoning'
assert [(c['criterion_id'],c['criterion_type'],c['points'],c['match_mode']) for c in pattern['criteria']]==[
 ('C1','conceptual',3,'semantic'),('C2','conceptual',3,'semantic'),('C3','conceptual',4,'semantic')
]
assert 'two supplied array options' not in by_item_id['WP2-ENG-CODESIGN-KP-026-Q03']['item']['question']
for fixed_rubric_id in ('WP2-PRO-DOPING-0049','WP2-PRO-DOPING-0053','WP2-PRO-DOPING-0069'):
 rubric=by_item_id[fixed_rubric_id]['item']['rubric']
 assert 'C1:' in rubric and not re.search(r'(?:[A-Za-z0-9] ){8}',rubric),(fixed_rubric_id,'Malformed rubric typography')


# Workbook reader uses OOXML from the Python standard library: no build/runtime dependencies.
ns={'x':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
book_path=root/'data/v1.0/wp2_benchmark.xlsx'
with zipfile.ZipFile(book_path) as zipf:
 work=ET.fromstring(zipf.read('xl/workbook.xml'))
 names=[node.attrib['name'] for node in work.findall('x:sheets/x:sheet',ns)]
 assert names==['Instructions','Items','Criteria','Responses'],names
 strings=[]
 if 'xl/sharedStrings.xml' in zipf.namelist():
  rootstr=ET.fromstring(zipf.read('xl/sharedStrings.xml'))
  for si in rootstr.findall('x:si',ns):strings.append(''.join(n.text or '' for n in si.findall('.//x:t',ns)))
 def read_sheet(number):
  doc=ET.fromstring(zipf.read(f'xl/worksheets/sheet{number}.xml'))
  out=[]
  for row in doc.findall('x:sheetData/x:row',ns):
   cells={}
   for c in row.findall('x:c',ns):
    col=re.match(r'[A-Z]+',c.attrib['r']).group(0)
    idx=0
    for ch in col:idx=idx*26+ord(ch)-ord('A')+1
    idx-=1
    t=c.attrib.get('t','n');v=c.find('x:v',ns)
    value=v.text if v is not None and v.text is not None else ''
    if t=='s':value=strings[int(value)]
    elif t in ('n','') and value!='':value=float(value)
    elif t=='b' and value!='':value=value=='1'
    elif t=='inlineStr':value=''.join(x.text or '' for x in c.findall('.//x:t',ns))
    cells[idx]=value
   if cells:
    out.append([cells.get(i,'') for i in range(max(cells)+1)])
  return out
 instructions=read_sheet(1)
 item_table=read_sheet(2);criterion_table=read_sheet(3);response_table=read_sheet(4)
 assert 'V1.0.0' in instructions[0][0]
 assert not any('quality_summary.json' in str(v) or 'release candidate' in str(v).lower() for row in instructions for v in row)

item_fields=['item_id','question','input_data','assumptions','reference_answer','rubric','maximum_score','task_profile','difficulty','capability_category','task_type','module_id','module_name','subdomain_id','subdomain_name','wp1_knowledge_title','source_reference','source_locator']
criterion_fields=['item_id','criterion_id','criterion_type','points','expected_value','accepted_variants','quantity_label','tolerance_type','tolerance_value','expected_unit','approved_evidence','forbidden_evidence','match_mode']
response_fields=['item_id','final_answer','response_status','response_source']
def table_as_dict(rows,headers):
 assert rows[0]==headers,(rows[0],headers)
 return [dict(zip(headers,row+['']*(len(headers)-len(row)))) for row in rows[1:]]
items=table_as_dict(item_table,item_fields)
criteria=table_as_dict(criterion_table,criterion_fields)
responses=table_as_dict(response_table,response_fields)
assert len(items)==len(responses)==769 and len(criteria)==1247

def projection(v):
 if v is None:return ''
 if isinstance(v,(list,dict)):return json.dumps(v,ensure_ascii=False,separators=(',',':'))
 return v

def cell_same(a,b):
 a,b=projection(a),projection(b)
 if isinstance(a,(int,float)) and not isinstance(a,bool) and isinstance(b,(int,float)) and not isinstance(b,bool):return abs(float(a)-float(b))<1e-10
 return a==b
by_id={r['item_id']:r for r in items}
assert len(by_id)==769 and set(by_id)==ids
for entry in entries:
 itm=entry['item'];row=by_id[itm['item_id']]
 for field in item_fields:assert cell_same(row[field],itm.get(field)),('Items',itm['item_id'],field)
crit_by_id={(r['item_id'],r['criterion_id']):r for r in criteria}
assert len(crit_by_id)==1247 and set(crit_by_id)==criterion_keys
for entry in entries:
 for c in entry['criteria']:
  row=crit_by_id[(c['item_id'],c['criterion_id'])]
  for field in criterion_fields:assert cell_same(row[field],c.get(field)),('Criteria',c['item_id'],c['criterion_id'],field)
assert [r['item_id'] for r in responses]==[e['item']['item_id'] for e in entries]
for row in responses:assert all(projection(row[f])=='' for f in response_fields[1:])

with (root/'metadata/source_register.csv').open(encoding='utf-8-sig',newline='') as f:
 reg=list(csv.DictReader(f))
assert len(reg)==165
assert all('resolution_status' not in x and 'Original bibliographic attribution:' not in x['source_reference'] for x in reg)
# Audit the exact source string registry and the explicit unresolved source-work mismatch gate.
source_rows={r['source_reference']:r for r in reg}
assert len(source_rows)==len(reg)==len(set(r['source_key'] for r in reg))==165
assert all(r['source_key']=='ref-'+hashlib.sha256(r['source_reference'].encode('utf-8')).hexdigest()[:12] for r in reg)
all_sources=collections.Counter()
wp1_sources=collections.Counter()
wp2_sources=collections.Counter()
for record in records:wp1_sources[record['source_reference']]+=1
for entry in entries:wp2_sources[entry['item']['source_reference']]+=1
assert set(source_rows)==set(wp1_sources)|set(wp2_sources)
for name,row in source_rows.items():
 assert int(row['wp1_record_count'])==wp1_sources[name],name
 assert int(row['wp2_item_count'])==wp2_sources[name],name
with (root/'metadata/source_item_index.csv').open(encoding='utf-8-sig',newline='') as f:src_index=list(csv.DictReader(f))
expected={("WP1",r['record_id']):r for r in records}
expected.update({('WP2',e['item']['item_id']):e['item'] for e in entries})
assert len(src_index)==len(expected)==994
flags=collections.Counter()
seen=set()
for row in src_index:
 key=(row['record_type'],row['record_id']);assert key not in seen and key in expected,key;seen.add(key)
 assert row['source_key']==source_rows[expected[key]['source_reference']]['source_key'],key
 flags[row['traceability_flag']]+=1
assert len(seen)==len(expected)
assert flags['DIFFERENT_NAMED_WORK_VERIFY']==0
assert flags['DIFFERENT_LOCAL_IDS_SAME_NAMED_WORK']==manifest['source_traceability']['legacy_id_aliases_same_named_work']
assert manifest['source_traceability']['reference_locator_named_work_conflicts_pending']==0
assert manifest['source_traceability']['evidence_verification_complete'] is True
assert not any('Proposed additional source:' in x['item']['source_reference'] for x in entries)

assert 'source_register_resolution' not in summary and 'populated_dataset_quality_warnings' not in summary
assert 'authorization_status' not in manifest and 'public_attribution_identifiers' not in manifest
for private_name in ['historical_warning_flags.csv','quality_summary.json','release_checklist.md','PUBLIC_TRANSFORM_SUMMARY.json','RELEASE-AUTHORIZATION-REQUIRED.md']:
 assert not any(p.name==private_name for p in root.rglob('*'))
private=re.compile(r'https?://(?:drive|docs)\.google\.com/|drive\s+(?:archive\s+)?file\s+id\s*:|internal file\s*:|archive sha256\s*:|/home/[^/\s]+',re.I)
for path in root.rglob('*'):
 if packaged(path) and path.is_file() and path.suffix.lower() in {'.json','.csv','.md','.py','.yml','.yaml','.cff',''}:
  if path==Path(__file__).resolve():continue
  text=path.read_text(encoding='utf-8-sig')
  assert not private.search(text),path
sha=root/'metadata/SHA256SUMS';lines=sha.read_text().splitlines()
actual={str(p.relative_to(root)) for p in root.rglob('*') if packaged(p) and p.is_file() and p!=sha}
covered=set()
for line in lines:
 digest,rel=line.split('  ',1)
 target=root/rel
 assert target.is_file() and rel not in covered,rel
 covered.add(rel)
 assert hashlib.sha256(target.read_bytes()).hexdigest()==digest,rel
assert covered==actual,(sorted(actual-covered),sorted(covered-actual))
print(f'PASS: structural packaging integrity ({manifest["distribution_status"]}) | {len(records)} WP1 | {len(entries)} WP2 | {criterion_count} criteria | {len(reg)} source strings | 0 unresolved named-work source conflicts | XLSX exact correspondence | SHA-256 complete.')
print('This checks distribution integrity, not fresh scientific claim verification, documentary rights clearance, remote GitHub CI, or WP3 runtime isolation.')
