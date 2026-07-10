"""Minimal structural checks for the GitBook metabolic-modeling manuscript."""
from pathlib import Path
import re

root = Path(__file__).parents[1]
errors = []
for path in root.rglob('*.md'):
    text = path.read_text()
    for n, line in enumerate(text.splitlines(), 1):
        if re.search(r'(?<!\\)qquad', line):
            errors.append(f'{path.relative_to(root)}:{n}: malformed qquad')
        if re.search(r'(?<!\\)left\\\{', line):
            errors.append(f'{path.relative_to(root)}:{n}: malformed left brace')

summary = (root / 'SUMMARY.md').read_text()
if 'textbook-completeness-supplement.md' not in summary:
    errors.append('SUMMARY.md: textbook supplement missing from navigation')
for n in range(1, 11):
    page = (root / f'chapter-{n}' / 'README.md').read_text()
    if f'interactive/index.html?chapter={n}' not in page:
        errors.append(f'chapter-{n}/README.md: interactive figure link missing')

if errors:
    raise SystemExit('\n'.join(errors))
print('PASS: manuscript structural checks; 10 interactive chapter links and supplement navigation present.')
