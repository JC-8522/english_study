"""Audit the vocabulary chapters and their reading index (stdlib only)."""
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
LIBRARY = ROOT / '分类词库'
DATA = LIBRARY / '资料'
CHAPTERS = LIBRARY / '分册'
MAX_ENTRIES_PER_CHAPTER = 100
EXCLUDED_CATEGORIES = {
    '专名 / 人名 / 历史文化与公众人物',
    '专名 / 人名 / 女性名字',
    '专名 / 人名 / 姓氏与其他人名',
    '专名 / 人名 / 男性名字',
}

def normalize(text):
    text = unicodedata.normalize('NFKC', text).replace('’', "'").replace('‘', "'")
    text = text.replace('–', '-').replace('—', '-')
    text = re.sub(r'\\([*_`\\\[\]])', r'\1', html.unescape(text))
    return re.sub(r'\s+', ' ', text).strip(' *`.,;:!?“”"').casefold()

def read_tsv(name):
    with (DATA / name).open(encoding='utf8', newline='') as stream:
        return list(csv.DictReader(stream, delimiter='\t'))

def chapter_filename(category):
    return re.sub(r'[^\w\u4e00-\u9fff-]+', '-', category).strip('-') + '.md'

def main():
    manifest = json.loads((DATA / 'manifest.json').read_text(encoding='utf8'))
    assert LIBRARY.is_dir() and CHAPTERS.is_dir() and DATA.is_dir()
    contents = LIBRARY / 'README.md'
    assert (ROOT / 'README.md').is_file() and contents.is_file()
    assert not (ROOT / 'study').exists(), 'Old generated layout remains'
    assert set(manifest['user_excluded_categories']) == EXCLUDED_CATEGORIES
    assert not EXCLUDED_CATEGORIES.intersection(manifest['category_counts'])
    counts = {}
    word_lines = {}
    expected_links = Counter()
    index_pages = manifest['chapter_index_pages']
    seen_index_pages = set()
    assert not index_pages.keys() & manifest['category_counts'].keys()
    chapter_files = sorted(CHAPTERS.glob('*.md'))
    entry = re.compile(r'^(\d+)\. \*\*(.*?)\*\*，读音：(.+?)，重音：(.+?)，中文：(.+?)；口语：① (.+) ② (.+)$')
    for path in chapter_files:
        heading, *lines = path.read_text(encoding='utf8').splitlines()
        assert heading.startswith('# '), ('Missing chapter title', path.name)
        category = heading[2:]
        assert path.name == chapter_filename(category), ('Chapter filename does not match category', path.name, category)
        if category in index_pages:
            destinations = index_pages[category]
            assert destinations and destinations.keys() <= manifest['category_counts'].keys()
            assert all(0 < total <= manifest['category_counts'][name] for name, total in destinations.items())
            expected_destinations = {
                f'- [{name}（{total}）]({chapter_filename(name)})'
                for name, total in destinations.items()
            }
            redirect_lines = [line for line in lines if line.startswith('- ')]
            assert Counter(redirect_lines) == Counter(expected_destinations), ('Invalid old chapter index', path.name)
            assert not any(re.match(r'^\d+\. ', line) for line in lines), ('Old chapter still has entries', path.name)
            seen_index_pages.add(category)
            continue
        assert category in manifest['category_counts'], ('Unknown category', category)
        assert category not in counts, ('Duplicate chapter', category)
        assert path.stat().st_size < 500_000, ('Chapter too large for comfortable GitHub reading', path.name)
        counts[category] = 0
        for line in lines:
            assert not line.startswith('|'), ('Table in chapter', path.name)
            match = entry.fullmatch(line)
            if not match:
                assert not re.match(r'^\d+\. ', line), 'Malformed entry: ' + line[:100]
                continue
            number, word, pronunciation, stress, meaning, ex1, ex2 = match.groups()
            counts[category] += 1
            assert int(number) == counts[category], (category, number)
            key = normalize(word)
            assert key not in word_lines, 'Duplicate: ' + key
            assert all(x.strip() and x.strip() != '—' for x in (pronunciation, stress, meaning, ex1, ex2)), key
            assert ex1 != ex2, 'Repeated example: ' + key
            word_lines[key] = (category, ex1, ex2)
        leaf = category.rsplit(' / ', 1)[-1]
        assert 0 < counts[category] <= MAX_ENTRIES_PER_CHAPTER, ('Chapter exceeds entry limit or is empty', category)
        expected_links[leaf, str(counts[category]), f'分册/{path.name}'] += 1
    assert len(word_lines) == manifest['entries']
    assert counts == manifest['category_counts']
    assert seen_index_pages == index_pages.keys(), 'Missing old chapter indexes'
    index = contents.read_text(encoding='utf8')
    links = re.findall(r'\[([^\]\n]+)（(\d+)）\]\((分册/[^)]+)\)', index)
    assert Counter(links) == expected_links, 'Index chapter links or counts differ from the chapters'
    topics = {category.split(' / ', 1)[0] for category in counts}
    headings = set(re.findall(r'^## (.+)$', index, re.M))
    jump_links = Counter(re.findall(r'\[[^\]\n]+\]\(#([^)]+)\)', index))
    assert topics <= headings and jump_links == Counter(topics), 'Index topic links differ from the topics'

    provenance = read_tsv('word-provenance.tsv')
    supplemental = manifest.get('supplemental_words', [])
    supplemental_keys = set(supplemental)
    original_keys = {r['word'] for r in provenance}
    assert len(supplemental_keys) == len(supplemental), 'Duplicate supplemental word'
    assert not original_keys & supplemental_keys, 'Supplemental word is already in the original sources'
    assert original_keys | supplemental_keys == word_lines.keys(), 'Source/output coverage differs'
    source_rows = defaultdict(set)
    for row in provenance:
        assert row['category'] == word_lines[row['word']][0]
        source_rows[row['source_file']].add(int(row['source_line']))
    scanned_rows = 0
    for source in manifest['original_files']:
        name = source['file']
        original = subprocess.check_output(['git', 'show', manifest['base_commit'] + ':' + name], cwd=ROOT)
        assert hashlib.sha256(original).hexdigest() == source['sha256'], name
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
        excluded = set(manifest['user_excluded_source_rows'].get(name, []))
        assert not excluded.intersection(source_rows[name]), ('Excluded name source row reappears', name)
        assert expected == source_rows[name] | excluded, ('Uncovered source rows', name, sorted(expected - source_rows[name] - excluded))
        for row in provenance:
            if row['source_file'] == name:
                assert row['source_headword'] == headwords[int(row['source_line'])], ('Source text mismatch', row)
    assert scanned_rows == manifest['source_table_and_heading_rows']

    examples = read_tsv('example-attribution.tsv')
    assert Counter(r['word'] for r in examples) == Counter({key: 2 for key in word_lines})
    for row in examples:
        index = int(row['example'])
        assert index in (1, 2)
        if row['word'] in supplemental_keys:
            assert row['source'] == 'authored', ('Missing authored example', row['word'])
        rendered = word_lines[row['word']][index]
        if row['source'] == 'Tatoeba':
            assert row['sentence_id'] and row['author']
            assert row['license'] in ('CC0-1.0', 'CC-BY-2.0-FR')
            assert row['url'] == 'https://tatoeba.org/en/sentences/show/' + row['sentence_id']
            rendered = re.sub(r'^\[(.*)\]\(https://tatoeba.org/en/sentences/show/\d+\)$', r'\1', rendered)
        rendered = re.sub(r'\\([*_`\\\[\]])', r'\1', html.unescape(rendered))
        assert rendered == row['sentence'], ('Example differs from attribution', row['word'], index)
    assert not any('专名-人名-' in p.name for p in LIBRARY.rglob('*')), 'Removed name chapter remains'
    for path in [ROOT / 'README.md', *LIBRARY.rglob('*.md')]:
        for link in re.findall(r'(?<!\\)\]\(([^)]+)\)', path.read_text(encoding='utf8')):
            if '://' not in link and not link.startswith('#'):
                target = path.parent / unquote(link.split('#')[0])
                assert target.exists() or target.resolve() == (DATA / 'validation.json').resolve(), (path.name, link)
    result = {'passed': True, 'source_documents': manifest['source_documents'], 'source_rows_scanned': scanned_rows,
              'entries': len(word_lines), 'categories': len(counts), 'examples': len(examples),
              'chapter_files': len(counts), 'max_entries_per_chapter': max(counts.values()),
              'chapter_index_pages': len(seen_index_pages), 'all_original_files_unchanged': len(manifest['original_files']),
              'removed_person_name_entries': manifest['user_excluded_person_name_entries'],
              'explicitly_excluded_name_source_rows': sum(len(rows) for rows in manifest['user_excluded_source_rows'].values()),
              'contents': '分类词库/README.md',
              'unresolved_original_labels': manifest['unresolved_original_labels'],
              'uncertain_context_entries': manifest['uncertain_context_entries'],
              'supplemental_entries': len(supplemental_keys)}
    (DATA / 'validation.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf8')
    print(json.dumps(result, ensure_ascii=False))

if __name__ == '__main__':
    main()
