"""Audit the consolidated vocabulary and its readable chapter copies (stdlib only)."""
from collections import Counter, defaultdict
import csv
import hashlib
import html
import json
from pathlib import Path
import re
import subprocess
import unicodedata
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]

def normalize(text):
    text = unicodedata.normalize('NFKC', text).replace('’', "'").replace('‘', "'")
    text = text.replace('–', '-').replace('—', '-')
    text = re.sub(r'\\([*_`\\\[\]])', r'\1', html.unescape(text))
    return re.sub(r'\s+', ' ', text).strip(' *`.,;:!?“”"').casefold()

def read_tsv(name):
    with (ROOT / 'study' / name).open(encoding='utf8', newline='') as stream:
        return list(csv.DictReader(stream, delimiter='\t'))

def main():
    manifest = json.loads((ROOT / 'study/manifest.json').read_text(encoding='utf8'))
    master = (ROOT / 'active words.md').read_text(encoding='utf8')
    groups = defaultdict(list)
    word_lines = {}
    category = None
    for line in master.splitlines():
        if line.startswith('## ') and line[3:] in manifest['category_counts']:
            category = line[3:]
        match = re.match(r'^(\d+)\. \*\*(.*?)\*\*，读音：(.+?)，重音：(.+?)，中文：(.+?)；口语：① (.+) ② (.+)$', line)
        if not match:
            assert not re.match(r'^\d+\. \*\*', line), 'Malformed entry: ' + line[:100]
            continue
        assert category, 'Entry outside a category'
        number, word, pronunciation, stress, meaning, ex1, ex2 = match.groups()
        assert int(number) == len(groups[category]) + 1, (category, number)
        key = normalize(word)
        assert key not in word_lines, 'Duplicate: ' + key
        assert all(x.strip() and x.strip() != '—' for x in (pronunciation, stress, meaning, ex1, ex2)), key
        assert ex1 != ex2, 'Repeated example: ' + key
        word_lines[key] = (category, line, ex1, ex2)
        groups[category].append(line)
    assert len(word_lines) == manifest['entries']
    assert dict((c, len(rows)) for c, rows in groups.items()) == manifest['category_counts']
    assert not any(line.startswith('|') for line in master.splitlines()), 'Table in master'

    provenance = read_tsv('word-provenance.tsv')
    assert {r['word'] for r in provenance} == set(word_lines), 'Source/output coverage differs'
    source_rows = defaultdict(set)
    for row in provenance:
        assert row['category'] == word_lines[row['word']][0]
        source_rows[row['source_file']].add(int(row['source_line']))
    scanned_rows = 0
    for source in manifest['original_files']:
        name = source['file']
        original = subprocess.check_output(['git', 'show', manifest['base_commit'] + ':' + name], cwd=ROOT)
        assert hashlib.sha256(original).hexdigest() == source['sha256'], name
        if name != 'active words.md':
            assert (ROOT / name).is_file(), 'Deleted source: ' + name
            # Git may check out LF blobs as CRLF on Windows without any content edit.
            assert (ROOT / name).read_bytes().replace(b'\r\n', b'\n') == original.replace(b'\r\n', b'\n'), 'Modified source: ' + name
        text = original.decode('utf-8-sig')
        expected = set()
        headwords = {}
        for number, line in enumerate(text.splitlines(), 1):
            if name == 'INDEX.md':
                continue
            if name == 'need-to-know-hit-list.md' and line.startswith('### '):
                expected.add(number)
                headwords[number] = re.sub(r'^### \d+\. ', '', line).split(' (', 1)[0]
            elif line.startswith('|'):
                cells = [c.strip() for c in re.split(r'(?<!\\)\|', line.strip('|'))]
                if len(cells) == 4 and cells[0] != 'Word' and not re.fullmatch(r'[- :]+', cells[0]):
                    expected.add(number)
                    headwords[number] = cells[0].replace('\\|', '|')
        scanned_rows += len(expected)
        if name == '旅游 英语.md':
            heading_labels = set(manifest['source_exclusions'][0]['headwords'])
            expected = {n for n in expected if headwords[n] not in heading_labels}
        assert expected == source_rows[name], ('Uncovered source rows', name, sorted(expected - source_rows[name]))
        for row in provenance:
            if row['source_file'] == name:
                assert row['source_headword'] == headwords[int(row['source_line'])], ('Source text mismatch', row)
    assert scanned_rows == manifest['source_table_and_heading_rows']

    examples = read_tsv('example-attribution.tsv')
    assert Counter(r['word'] for r in examples) == Counter({key: 2 for key in word_lines})
    for row in examples:
        index = int(row['example'])
        assert index in (1, 2)
        rendered = word_lines[row['word']][index + 1]
        if row['source'] == 'Tatoeba':
            assert row['sentence_id'] and row['author']
            assert row['license'] in ('CC0-1.0', 'CC-BY-2.0-FR')
            assert row['url'] == 'https://tatoeba.org/en/sentences/show/' + row['sentence_id']
            rendered = re.sub(r'^\[(.*)\]\(https://tatoeba.org/en/sentences/show/\d+\)$', r'\1', rendered)
        rendered = re.sub(r'\\([*_`\\\[\]])', r'\1', html.unescape(rendered))
        assert rendered == row['sentence'], ('Example differs from attribution', row['word'], index)
    chapter_files = set()
    for category, rows in groups.items():
        filename = re.sub(r'[^\w\u4e00-\u9fff-]+', '-', category).strip('-') + '.md'
        path = ROOT / 'study' / filename
        assert path.is_file(), filename
        chapter_rows = [line for line in path.read_text(encoding='utf8').splitlines() if re.match(r'^\d+\. \*\*', line)]
        assert rows == chapter_rows, 'Chapter differs from master: ' + category
        assert path.stat().st_size < 500_000, 'Chapter too large for comfortable GitHub reading'
        chapter_files.add(filename)
    existing_chapters = {p.name for p in (ROOT / 'study').glob('*.md') if '[返回总目录]' in p.read_text(encoding='utf8')[:200]}
    assert existing_chapters == chapter_files, 'Stale chapter copies'
    for path in [ROOT / 'active words.md', *(ROOT / 'study').glob('*.md')]:
        for link in re.findall(r'(?<!\\)\]\(([^)]+)\)', path.read_text(encoding='utf8')):
            if '://' not in link and not link.startswith('#'):
                target = path.parent / unquote(link.split('#')[0])
                assert target.exists() or target.resolve() == (ROOT / 'study/validation.json').resolve(), (path.name, link)
    result = {'passed': True, 'source_documents': manifest['source_documents'], 'source_rows_scanned': scanned_rows,
              'entries': len(word_lines), 'categories': len(groups), 'examples': len(examples),
              'chapter_copies': len(chapter_files), 'other_original_files_unchanged': len(manifest['original_files']) - 1,
              'unresolved_original_labels': manifest['unresolved_original_labels']}
    (ROOT / 'study/validation.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf8')
    print(json.dumps(result, ensure_ascii=False))

if __name__ == '__main__':
    main()
