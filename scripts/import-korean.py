"""Build the catalog from reviewed, checksum-pinned Korean edition snapshots.

Never downloads a newer edition or rewrites literary text. New source approval
requires a separately reviewed research/korean-editions/manifest.json change.
"""
from pathlib import Path
import hashlib
import json
import math
import re

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / 'research/korean-editions'
BASELINE = ROOT / 'research/original-package-20261026'
DATA = ROOT / 'dist/data'

def load(path):
    return json.loads(path.read_bytes())

def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def safe(root, relative):
    path = (root / relative).resolve()
    assert path.is_relative_to(root.resolve()), relative
    return path

def main():
    manifest = load(INPUT / 'manifest.json')
    for relative, expected in load(INPUT / 'sha256.json')['files'].items():
        assert sha(safe(INPUT, relative).read_bytes()) == expected, relative
    original = load(BASELINE / 'catalog.json')
    original_sources = load(BASELINE / 'sources.json')
    original_hashes = load(BASELINE / 'package-sha256.json')['files']
    for relative, expected in original_hashes.items():
        if relative.startswith(('books/', 'txt/')):
            assert sha(safe(DATA, relative).read_bytes()) == expected, relative

    catalog = []
    sources = []
    for row in manifest['books']:
        raw = safe(INPUT, row['sourceBook']).read_bytes()
        assert sha(raw) == row['sourceBookSha256'], row['id']
        book = json.loads(raw)
        assert book['id'] == row['id'] and book['language'] == 'ko'
        paragraphs = [p for c in book['chapters'] for p in c['paragraphs']]
        body = '\n'.join(paragraphs)
        assert '\ufffd' not in body
        assert not any(0xE000 <= ord(c) <= 0xF8FF or 0xF0000 <= ord(c) <= 0xFFFFD or 0x100000 <= ord(c) <= 0x10FFFD for c in body)
        edition = {key: row[key] for key in [
            'license', 'licenseUrl', 'sourceUrl', 'pinnedSourceUrl', 'historyUrl',
            'attribution', 'modifications', 'sourceCredits', 'editionNote', 'rightsNote',
            'sourceVersionNote']}
        edition['verifiedOn'] = manifest['verifiedOn']
        if row['id'].startswith('ko-'):
            edition['scanPageRevisionsUrl'] = 'https://nanalab.kr/nocturne-library/data/revisions/yiinjik-scan-pages.json'
        book['edition'] = edition
        relative_json = 'books/' + book['id'] + '.json'
        relative_txt = 'txt/' + book['id'] + '.txt'
        save(DATA / relative_json, book)

        sections = ['%s\n%s' % (book['title'], book['author'])]
        sections.extend(c['title'] + '\n\n' + '\n\n'.join(c['paragraphs']) for c in book['chapters'])
        footer = ['[출처·이용 조건 / Source and reuse]',
                  '저자 / Author: ' + book['author'],
                  '판본 / Edition: ' + row['editionNote'],
                  '수록 범위 / Scope: ' + row['completeness'],
                  '출처 / Source: ' + row['sourceUrl'],
                  '수집 판본 / Edition reference: ' + row['pinnedSourceUrl'],
                  '저작자 표시 / Attribution: ' + row['attribution'],
                  '이용 조건 / License: ' + row['license'],
                  'License URL: ' + row['licenseUrl'],
                  '권리 고지 / Rights: ' + row['rightsNote'],
                  '판본 식별 / Version: ' + row['sourceVersionNote'],
                  '변경 내역 / Modifications:'] + ['- ' + note for note in row['modifications']]
        if row.get('historyUrl'):
            footer.insert(6, '기여 이력 / Contributors and history: ' + row['historyUrl'])
        if edition.get('scanPageRevisionsUrl'):
            footer.append('개별 전사 페이지 고정판 / Transcluded page revisions: ' + edition['scanPageRevisionsUrl'])
        if row['license'] == 'CC-BY-SA-4.0':
            footer.append('This adapted transcription is provided under CC BY-SA 4.0. This license applies to the covered text, not to unrelated application code or other books. No additional restrictions or DRM are imposed.')
        footer.append('원문 JSON SHA-256 / Frozen source JSON SHA-256: ' + row['sourceBookSha256'])
        footer.append('확인일 / Verified: ' + manifest['verifiedOn'])
        (DATA / relative_txt).parent.mkdir(exist_ok=True)
        (DATA / relative_txt).write_text('\n\n'.join(sections) + '\n\n' + '\n'.join(footer) + '\n', encoding='utf-8', newline='\n')
        count = len(re.findall(r'\S+', body))
        meta = {k:v for k,v in row.items() if k not in ['provenance','sourceBook','sourceBookSha256']}
        meta.update(file=relative_json, txt=relative_txt, wordCount=count, wordCountUnit='eojeol',
                    characterCount=sum(len(p) for p in paragraphs), readingMinutes=max(1, math.ceil(count / 180)),
                    chapterCount=len(book['chapters']), mainChapterCount=len(book['chapters']))
        if edition.get('scanPageRevisionsUrl'):
            meta['scanPageRevisionsUrl'] = edition['scanPageRevisionsUrl']
        catalog.append(meta)
        sources.append(dict(id=row['id'], title=row['title'], author=row['author'], language='ko', **edition,
                            editionProvenance=row['provenance'], sourceBookSha256=row['sourceBookSha256'],
                            readableCharacterCount=meta['characterCount'],
                            exportSha256={'json':sha((DATA/relative_json).read_bytes()), 'txt':sha((DATA/relative_txt).read_bytes())}))

    copy_revision = INPUT / 'evidence/yiinjik/scan-pages.json'
    (DATA/'revisions').mkdir(exist_ok=True)
    (DATA/'revisions/yiinjik-scan-pages.json').write_bytes(copy_revision.read_bytes())
    save(DATA/'catalog.json', dict(schemaVersion=1, books=catalog+original['books'], references=manifest['references']))
    original_sources.update(verifiedOn=manifest['verifiedOn'],
        policy='English originals and Korean original/provider transcriptions. No newly created translation. Original rights and each electronic edition license are assessed separately. Modern spelling in the official provider files is identified as such.',
        koreanEditionEvidence='https://nanalab.kr/nocturne-library/data/sources.json',
        books=original_sources['books']+sources)
    save(DATA/'sources.json', original_sources)
    all_books = catalog + original['books']
    decoded = [load(DATA/m['file']) for m in all_books]
    english_words = sum(m['wordCount'] for m in original['books'])
    korean_eojeol = sum(m['wordCount'] for m in catalog)
    save(DATA/'verification.json', dict(schemaVersion=2, verifiedOn=manifest['verifiedOn'],
        books=len(all_books), originalEnglishBooks=len(original['books']), koreanBooks=len(catalog),
        externalReferences=len(manifest['references']), wordCount=english_words+korean_eojeol,
        englishWordCount=english_words, koreanEojeolCount=korean_eojeol,
        countNote='wordCount is a compatibility aggregate of English word tokens and approximate Korean whitespace units; they are reported separately above. Original print line breaks may split Korean words. Character counts are Unicode code points, not graphemes.',
        sectionCount=sum(len(b['chapters']) for b in decoded), mainChapterCount=sum(m['mainChapterCount'] for m in all_books),
        verifiedTextBlocks=sum(len(c['paragraphs']) for b in decoded for c in b['chapters']),
        translatedBooks=0, sourceToExportBodyIntegrity=True,
        integrityBoundary='Original 24 English book/TXT files retain pinned 2026-10-26 byte hashes. Korean chapter text equals the reviewed frozen transcription snapshots; this does not assert manual glyph collation of every historical printed page.',
        jsonBytes=sum((DATA/m['file']).stat().st_size for m in all_books),
        txtBytes=sum((DATA/m['txt']).stat().st_size for m in all_books)))
    files = sorted([m[key] for m in all_books for key in ['file','txt']] + ['catalog.json','sources.json','verification.json','revisions/yiinjik-scan-pages.json'])
    save(DATA/'package-sha256.json',dict(algorithm='SHA256',files={p:sha((DATA/p).read_bytes()) for p in files}))
    print(json.dumps({'books':len(all_books), 'koreanBooks':len(catalog), 'englishBooks':len(original['books']), 'externalReferences':len(manifest['references']), 'pinnedFiles':len(files)}, ensure_ascii=False))

if __name__ == '__main__':
    main()
