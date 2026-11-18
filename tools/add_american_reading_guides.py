"""Add/update the two reading fields without changing any existing entry fields.

Run from any directory. --check reports stale/missing generated reading fields.
"""
import argparse
import json
from pathlib import Path
import re

from american_reading import make_reading

ROOT = Path(__file__).resolve().parents[1]
LIBRARY = ROOT / '分类词库'
DATA = LIBRARY / '资料'
ENTRY = re.compile(
    r'^(\d+\. \*\*(.*?)\*\*，读音：)(.+?)'
    r'(?:，美式易读：(.+?)，读法理解：(.+?))?'
    r'，重音：(.+?)，中文：(.+?)；口语：① (.+) ② (.+)$', re.M
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    overrides = json.loads((DATA / 'american-reading-overrides.json').read_text(encoding='utf8'))['entries']
    seen, references, initials, changed = set(), 0, 0, []
    updates = {}
    for path in sorted((LIBRARY / '分册').glob('*.md')):
        text = path.read_text(encoding='utf8')
        def replace(match):
            nonlocal references, initials
            prefix, word, ipa, _, _, stress, meaning, ex1, ex2 = match.groups()
            key = word.casefold()
            assert key not in seen, ('Duplicate headword', key)
            seen.add(key)
            try:
                spelling, explanation, reference, letters = make_reading(word, ipa, stress, overrides.get(key))
            except ValueError as error:
                raise ValueError(f'{word}: {error}') from error
            references += reference
            initials += letters
            return (f'{prefix}{ipa}，美式易读：{spelling}，读法理解：{explanation}'
                    f'，重音：{stress}，中文：{meaning}；口语：① {ex1} ② {ex2}')
        updated = ENTRY.sub(replace, text)
        if updated != text:
            changed.append(str(path.relative_to(ROOT)))
            updates[path] = updated
    manifest_path = DATA / 'manifest.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf8'))
    assert len(seen) == manifest['entries'], (len(seen), manifest['entries'])
    assert overrides.keys() <= seen, ('Override has no matching entry', overrides.keys() - seen)
    metadata = {
        'scheme': 'american-respelling-v1', 'entries': len(seen),
        'reference_entries': references, 'letter_spelling_entries': initials,
        'guide': '分类词库/美式易读说明.md',
    }
    if manifest.get('american_reading_guides') != metadata:
        changed.append(str(manifest_path.relative_to(ROOT)))
        if not args.check:
            manifest['american_reading_guides'] = metadata
            updates[manifest_path] = json.dumps(manifest, ensure_ascii=False, indent=2) + '\n'
    if not args.check:
        for path, updated in updates.items():
            path.write_text(updated, encoding='utf8', newline='\n')
    print(json.dumps({'entries': len(seen), 'reference_entries': references,
                      'letter_spelling_entries': initials, 'changed_files': len(changed),
                      'check': args.check}, ensure_ascii=False))
    if args.check and changed:
        raise SystemExit('Reading fields need regeneration: ' + ', '.join(changed[:5]))


if __name__ == '__main__':
    main()
