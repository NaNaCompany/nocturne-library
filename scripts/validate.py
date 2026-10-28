"""Verify frozen editions and unchanged originals, not manual print collation."""
from pathlib import Path, PurePosixPath
from urllib.parse import urlsplit
from html.parser import HTMLParser
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
DATA = DIST / 'data'
BASELINE = ROOT / 'research/original-package-20261026'
EDITIONS = ROOT / 'research/korean-editions'
LANGUAGES = ['ko', 'en', 'es', 'zh', 'ja', 'de']
FOOTER = '[출처·이용 조건 / Source and reuse]'
KOREAN_IDS = {'ko-hyeorui-nu', 'ko-chiaksan-upper', 'jayujong', 'gumageom', 'binsangseol',
              'hwaui-hyeol', 'ahn-gongjinhoe', 'ahn-geumsuhoeuirok', 'heogyun-honggildong-30', 'gwandong-byeolgok'}
ORIGINAL_FIXTURE_DIGESTS = {
    'catalog.json': '339f1fb05c695c7939e2d8060a48b40cd1c34a675ca3b7911b4c0a559be0957a',
    'sources.json': '6727f5bc58290a5d155bac1e932b4b384550eecdc214f8552c3697fb8d7f0e97',
    'verification.json': '0f2a1dba702466eb2ee56cc3a989fa9da4d39225d603dc918bd41436d775eecb',
    'package-sha256.json': 'a5c616c1cddeaed0cdfabddfece686f299874f8f9f4e0c5fe9e1f71c127beacf',
}


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def load(path):
    return json.loads(path.read_bytes())


def digest(data):
    return hashlib.sha256(data).hexdigest()


def safe_path(base, relative):
    require(isinstance(relative, str) and relative and '\\' not in relative, f'Invalid path: {relative!r}')
    parsed = PurePosixPath(relative)
    require(not parsed.is_absolute() and all(part not in ('.', '..') for part in parsed.parts), f'Unsafe path: {relative}')
    target = (base / relative).resolve()
    require(target.is_relative_to(base.resolve()) and target.is_file(), f'Missing/unsafe file: {relative}')
    return target


def https(value, label, hosts=None):
    require(isinstance(value, str), f'Missing URL: {label}')
    parsed = urlsplit(value)
    require(parsed.scheme == 'https' and parsed.hostname and not parsed.username and not parsed.password,
            f'Invalid public HTTPS URL: {label}')
    if hosts:
        require(parsed.hostname in hosts, f'Unexpected URL host: {label}')


def check_hashes(base, manifest):
    require(manifest.get('algorithm') == 'SHA256' and isinstance(manifest.get('files'), dict), 'Invalid checksum manifest')
    for relative, expected in manifest['files'].items():
        require(re.fullmatch(r'[a-f0-9]{64}', expected) is not None, f'Invalid SHA-256: {relative}')
        require(digest(safe_path(base, relative).read_bytes()) == expected, f'Hash mismatch: {relative}')


def private_use(character):
    value = ord(character)
    return 0xE000 <= value <= 0xF8FF or 0xF0000 <= value <= 0xFFFFD or 0x100000 <= value <= 0x10FFFD


def validate():
    for name, expected in ORIGINAL_FIXTURE_DIGESTS.items():
        encoded = json.dumps(load(BASELINE/name), ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')
        require(digest(encoded) == expected, f'Original semantic fixture changed: {name}')
    original_catalog = load(BASELINE/'catalog.json')['books']
    original_sources = load(BASELINE/'sources.json')['books']
    original_package = load(BASELINE/'package-sha256.json')
    require(len(original_catalog) == 12 and len(original_package['files']) == 27, 'Original baseline scope')
    for relative, expected in original_package['files'].items():
        base = DATA if relative.startswith(('books/', 'txt/')) else BASELINE
        require(digest(safe_path(base, relative).read_bytes()) == expected, f'Original export changed: {relative}')
    frozen = load(EDITIONS/'manifest.json')
    frozen_books = {row['id']: row for row in frozen['books']}
    require(set(frozen_books) == KOREAN_IDS and len(frozen['books']) == 10, 'Rights-reviewed edition set changed')
    check_hashes(EDITIONS, load(EDITIONS/'sha256.json'))
    catalog_object = load(DATA/'catalog.json')
    catalog = catalog_object['books']
    by_id = {book['id']: book for book in catalog}
    require(len(catalog) == len(by_id) == 22, 'Expected 22 distinct readable works')
    require([book for book in catalog if book['language'] == 'en'] == original_catalog, 'Original English catalog records/order changed')
    require({book['id'] for book in catalog if book['language'] == 'ko'} == KOREAN_IDS, 'Held/unreviewed edition imported')
    sources = load(DATA/'sources.json')['books']
    source_by_id = {source['id']: source for source in sources}
    require(len(sources) == len(source_by_id) == 22 and set(source_by_id) == set(by_id), 'Incomplete/duplicate source records')
    original_ids = {book['id'] for book in original_catalog}
    require([row for row in sources if row['id'] in original_ids] == original_sources, 'Original source records/order changed')
    package = load(DATA/'package-sha256.json')
    expected_files = {'catalog.json', 'sources.json', 'verification.json', 'revisions/yiinjik-scan-pages.json'}
    expected_files.update(book['file'] for book in catalog)
    expected_files.update(book['txt'] for book in catalog)
    require(set(package['files']) == expected_files and len(expected_files) == 48, 'Package must cover exactly 48 edition files')
    check_hashes(DATA, package)
    sections = paragraphs = english_words = korean_eojeol = korean_characters = main_chapters = json_bytes = txt_bytes = 0
    group_headings = []
    original_totals = {'sections': 0, 'paragraphs': 0, 'words': 0}
    for meta in catalog:
        ident = meta['id']
        require(re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', ident) is not None, f'Unsafe book ID: {ident}')
        require(meta['language'] in ('en', 'ko'), f'Unexpected language: {ident}')
        for key in ['sourceUrl', 'licenseUrl']:
            https(meta.get(key), ident+':'+key)
        require(meta['file'] == f'books/{ident}.json' and meta['txt'] == f'txt/{ident}.txt', f'Unexpected edition path: {ident}')
        book_raw = safe_path(DATA, meta['file']).read_bytes()
        txt_raw = safe_path(DATA, meta['txt']).read_bytes()
        book = json.loads(book_raw)
        require(all(book[key] == meta[key] for key in ['id', 'title', 'author', 'language']), f'Book identity mismatch: {ident}')
        chapters = book['chapters']
        require(len(chapters) == meta['chapterCount'] and chapters, f'Invalid chapter count: {ident}')
        require(len({chapter['id'] for chapter in chapters}) == len(chapters), f'Duplicate chapter: {ident}')
        blocks = []
        for chapter in chapters:
            require(isinstance(chapter['id'], str) and chapter['id'] and isinstance(chapter['title'], str)
                    and chapter['title'].strip() and isinstance(chapter['paragraphs'], list), f'Invalid chapter: {ident}')
            if not chapter['paragraphs']:
                group_headings.append((ident, chapter['id'], chapter['title']))
            require(all(isinstance(p, str) and p.strip() for p in chapter['paragraphs']), f'Invalid text block: {ident}')
            blocks.extend(chapter['paragraphs'])
        require(not txt_raw.startswith(b'\xef\xbb\xbf') and b'\r' not in txt_raw, f'TXT encoding/line endings: {ident}')
        txt = txt_raw.decode('utf-8')
        sections += len(chapters)
        paragraphs += len(blocks)
        main_chapters += meta['mainChapterCount']
        json_bytes += len(book_raw)
        txt_bytes += len(txt_raw)
        if meta['language'] == 'en':
            require(meta['license'] == 'CC0-1.0' and meta['authorDeathYear'] <= 1946 and meta['publishedYear'] <= 1925,
                    f'Original selection changed: {ident}')
            https(meta['sourceRepository'], ident+':repository', {'github.com'})
            require(meta['sourceRepository'].startswith('https://github.com/standardebooks/')
                    and re.fullmatch(r'[a-f0-9]{40}', meta['sourceCommit']), f'Original source pin: {ident}')
            english_words += meta['wordCount']
            original_totals['words'] += meta['wordCount']
            original_totals['sections'] += len(chapters)
            original_totals['paragraphs'] += len(blocks)
            continue
        approved = frozen_books[ident]
        frozen_path = safe_path(EDITIONS, approved['sourceBook'])
        frozen_book = load(frozen_path)
        require(digest(frozen_path.read_bytes()) == approved['sourceBookSha256'], f'Frozen checksum: {ident}')
        require(all(book.get(key) == value for key, value in frozen_book.items())
                and set(book) == set(frozen_book) | {'edition'}, f'Frozen reading text altered: {ident}')
        require(meta['metadataLanguage'] == 'ko' and meta['wordCountUnit'] == 'eojeol', f'Korean metadata/units: {ident}')
        for key in ['title', 'author', 'genre', 'description', 'publishedYear', 'authorDeathYear', 'sourceUrl',
                    'pinnedSourceUrl', 'historyUrl', 'license', 'licenseUrl', 'editionNote', 'rightsNote',
                    'completeness', 'sourceInstitution', 'sourceCredits']:
            require(meta.get(key) == approved.get(key), f'Approved metadata changed: {ident}:{key}')
        require(meta['genre'] in ('korean-modern', 'korean-classic', 'travel')
                and meta['license'] in ('Public-domain', 'CC-BY-SA-4.0'), f'Korean classification/license: {ident}')
        for key in ['sourceUrl', 'pinnedSourceUrl']:
            https(meta[key], ident+':'+key, {'ko.wikisource.org', 'gongu.copyright.or.kr'})
        if meta.get('historyUrl'):
            https(meta['historyUrl'], ident+':history', {'ko.wikisource.org'})
        for key in ['editionNote', 'rightsNote', 'completeness']:
            require(isinstance(meta[key], str) and len(meta[key]) >= 10, f'Missing scope/rights: {ident}:{key}')
        require(isinstance(meta['readingMinutes'], int) and meta['readingMinutes'] > 0, f'Invalid reading estimate: {ident}')
        count_chars = sum(map(len, blocks))
        count_eojeol = len(re.findall(r'\S+', '\n'.join(blocks)))
        require(meta['characterCount'] == count_chars and meta['wordCount'] == count_eojeol, f'Korean text counts: {ident}')
        korean_characters += count_chars
        korean_eojeol += count_eojeol
        reading_text = '\n'.join(blocks)
        require('\ufffd' not in reading_text and not any(map(private_use, reading_text)), f'Unresolved glyph: {ident}')
        require(FOOTER in txt, f'Missing standalone TXT attribution: {ident}')
        body, footer = txt.rsplit(FOOTER, 1)
        cursor = 0
        for paragraph in blocks:
            position = body.find(paragraph, cursor)
            require(position >= 0, f'TXT missing/reordered reading paragraph: {ident}')
            cursor = position + len(paragraph)
        require(meta['author'] in footer and meta['title'] in txt, f'TXT identity credit: {ident}')
        for key in ['sourceUrl', 'pinnedSourceUrl', 'licenseUrl']:
            require(meta[key] in footer, f'Missing TXT credit URL: {ident}:{key}')
        require(meta['license'] in footer and approved['attribution'] in footer, f'Missing TXT license/attribution: {ident}')
        require(all(change in footer for change in approved['modifications']), f'Missing TXT changes: {ident}')
        edition = book['edition']
        for key in ['license', 'licenseUrl', 'sourceUrl', 'pinnedSourceUrl', 'historyUrl', 'sourceCredits']:
            require(edition.get(key) == meta.get(key), f'JSON rights mismatch: {ident}:{key}')
        require(edition.get('attribution') == approved['attribution']
                and edition.get('modifications') == approved['modifications'], f'JSON attribution/changes: {ident}')
        if meta['license'] == 'CC-BY-SA-4.0':
            require(meta['licenseUrl'] == 'https://creativecommons.org/licenses/by-sa/4.0/' and meta.get('historyUrl')
                    and meta['historyUrl'] in footer and 'oldid=' in meta['pinnedSourceUrl'], f'Wikisource license/pin/credit: {ident}')
        else:
            require(urlsplit(meta['sourceUrl']).hostname == 'gongu.copyright.or.kr', f'Official expired source required: {ident}')
        source = source_by_id[ident]
        require(source.get('verifiedOn') == frozen['verifiedOn'], f'Source verification date: {ident}')
        require(source.get('editionProvenance') == approved['provenance'], f'Edition evidence changed: {ident}')
        require(source.get('sourceBookSha256') == approved['sourceBookSha256']
                and source.get('readableCharacterCount') == count_chars, f'Source audit mismatch: {ident}')
        require(source.get('exportSha256') == {'json': digest(book_raw), 'txt': digest(txt_raw)}, f'Export audit hashes: {ident}')
        for key in ['language', 'sourceUrl', 'pinnedSourceUrl', 'historyUrl', 'license', 'licenseUrl', 'sourceCredits', 'editionNote', 'rightsNote']:
            require(source.get(key) == meta.get(key), f'Source/catalog mismatch: {ident}:{key}')
        require(source.get('attribution') == approved['attribution']
                and source.get('modifications') == approved['modifications'], f'Source attribution/changes: {ident}')
    require(original_totals == {'sections': 450, 'paragraphs': 19476, 'words': 1149507}, 'Original English totals changed')
    require(set(group_headings) == {(ident, 'endnotes', 'Endnotes') for ident in
                                   ['frankenstein', 'moby-dick', 'time-machine']}, 'Unexpected empty section')
    require(by_id['ko-hyeorui-nu']['title'].endswith('(상편)')
            and by_id['ko-chiaksan-upper']['title'].endswith('(상편)'), 'Volume scope must remain explicit')
    require(by_id['heogyun-honggildong-30']['publishedYear'] is None
            and by_id['heogyun-honggildong-30']['chapterCount'] == 1, 'Unknown date/30-leaf scope changed')
    require(len(load(DATA/by_id['gwandong-byeolgok']['file'])['chapters'][0]['paragraphs']) == 146, 'Gwandong 146-line scope')
    revisions = load(DATA/'revisions/yiinjik-scan-pages.json')
    require(revisions == load(EDITIONS/'evidence/yiinjik/scan-pages.json'), 'Transclusion revision manifest changed')
    pages = revisions['pages']
    require(len(pages) == len({page['title'] for page in pages}) == 289, 'Expected 289 pinned transcluded pages')
    for page in pages:
        require(isinstance(page['revid'], int) and page['revid'] > 0
                and f'oldid={page["revid"]}' in page['permalink'], 'Unpinned source scan page')
        https(page['permalink'], 'scan revision', {'ko.wikisource.org'})
        https(page['historyUrl'], 'scan history', {'ko.wikisource.org'})
        require(isinstance(page['contributors'], list) and page['contributors'], 'Missing scan-page credits')
    for volume in revisions['volumes']:
        require(len(volume['pageTitles']) == volume['to']-volume['from']+1
                and set(volume['pageTitles']).issubset({page['title'] for page in pages}), 'Missing scan page range')
    references = catalog_object.get('references', [])
    require(references == frozen.get('references') and len(references) == 1, 'External reference scope changed')
    ref = references[0]
    require(ref['id'] == 'dongmyeong-ilgi' and ref['status'] == 'external-reference' and ref['id'] not in by_id
            and 'file' not in ref and 'txt' not in ref and ref.get('notice'), 'Uncleared Dongmyeong counted as readable')
    https(ref['sourceUrl'], 'Dongmyeong reference', {'ko.wikisource.org'})
    require(not any('dongmyeong' in path.name.lower() for folder in ['books', 'txt'] for path in (DATA/folder).glob('*')),
            'Uncleared Dongmyeong reading text exported')
    verification = load(DATA/'verification.json')
    require(verification.get('sourceToExportBodyIntegrity') is True and verification.get('translatedBooks') == 0,
            'Integrity/translation audit mismatch')
    expected = {'books': 22, 'originalEnglishBooks': 12, 'koreanBooks': 10, 'sectionCount': sections,
                'mainChapterCount': main_chapters, 'verifiedTextBlocks': paragraphs, 'wordCount': english_words+korean_eojeol,
                'englishWordCount': english_words, 'koreanEojeolCount': korean_eojeol, 'jsonBytes': json_bytes, 'txtBytes': txt_bytes}
    for key, value in expected.items():
        require(verification.get(key) == value, f'Verification total mismatch: {key}')
    if 'koreanCharacterCount' in verification:
        require(verification['koreanCharacterCount'] == korean_characters, 'Korean character total mismatch')

    class Document(HTMLParser):
        def __init__(self):
            super().__init__()
            self.ids, self.assets = [], []

        def handle_starttag(self, tag, attrs):
            attrs = dict(attrs)
            if 'id' in attrs:
                self.ids.append(attrs['id'])
            if tag == 'script' and attrs.get('src'):
                self.assets.append(attrs['src'])
            if tag == 'link' and attrs.get('rel') in ['stylesheet', 'icon']:
                self.assets.append(attrs['href'])
    doc = Document()
    doc.feed((DIST/'index.html').read_text(encoding='utf-8'))
    require(len(doc.ids) == len(set(doc.ids)), 'Duplicate root HTML IDs')
    js = (DIST/'app.js').read_text(encoding='utf-8')
    locale_source = (DIST/'locales.js').read_text(encoding='utf-8')
    locales = json.loads(locale_source.split('window.NOCTURNE_I18N = ', 1)[1].rstrip().removesuffix(';'))
    require(set(locales) == set(LANGUAGES) and len({frozenset(value) for value in locales.values()}) == 1,
            'Incomplete UI language dictionaries')
    for lang in LANGUAGES:
        html_path = DIST/'index.html' if lang == 'ko' else DIST/lang/'index.html'
        html = html_path.read_text(encoding='utf-8')
        require(f'<html lang="{lang}">' in html and ('<base href="../">' in html) == (lang != 'ko'), f'Locale path: {lang}')
        localdoc = Document()
        localdoc.feed(html)
        require(len(localdoc.ids) == len(set(localdoc.ids)), f'Duplicate HTML IDs: {lang}')
        require({'language-select', 'reader-language', 'reader-language-select', 'language-dialog',
                 'references-section', 'references-list'}.issubset(localdoc.ids), f'Missing controls: {lang}')
        require(len(re.findall(r'<option value="(?:ko|en|es|zh|ja|de)"', html)) == 12, f'Language selector: {lang}')
        for asset in localdoc.assets:
            require(not asset.startswith(('http:', 'https:', '//')), f'External runtime asset: {asset}')
            safe_path(DIST, asset)
        require(all(isinstance(value, str) and value for value in locales[lang].values()), f'Empty locale value: {lang}')
        if lang != 'ko':
            require(not re.search('[가-힣]', re.sub(r'<option\b.*?</option>', '', html, flags=re.S)), f'Untranslated static UI: {lang}')
    for key in re.findall(r"\bt\('([^']+)'", js):
        require(key in locales['ko'], f'Missing runtime locale key: {key}')
    generated_ids = set(re.findall(r'\bid="([a-z][a-z0-9-]*)"', js))
    for ident in re.findall(r"\$\('([^']+)'\)", js):
        require(ident in doc.ids or ident in generated_ids, f'Missing JavaScript target: {ident}')
    require('background:#000' in (DIST/'style.css').read_text(encoding='utf-8'), 'Black reader background changed')
    for path in DIST.rglob('*'):
        if path.is_file():
            require(path.suffix.lower() not in ['.jpg', '.jpeg', '.png', '.webp', '.woff', '.woff2', '.ttf', '.pdf'],
                    f'Unexpected third-party media/font in source: {path.name}')
            raw = path.read_bytes()
            require(b'C:\\Users\\' not in raw and b'C:/Users/' not in raw, f'Local path leaked: {path.name}')
            require(not re.search(rb'github_pat_[A-Za-z0-9_]+|gh[pousr]_[A-Za-z0-9_]{20,}', raw), f'Credential-like text: {path.name}')
    print(json.dumps({'pass': True, 'books': len(catalog), 'originalEnglishBooks': 12, 'koreanBooks': 10,
                      'externalReferences': len(references), 'sections': sections, 'textBlocks': paragraphs,
                      'englishWords': english_words, 'koreanEojeol': korean_eojeol, 'koreanCharacters': korean_characters,
                      'unchangedOriginalExports': 24, 'pinnedExportHashes': len(package['files']),
                      'pinnedScanPageRevisions': len(pages), 'translatedBooks': 0, 'languageRoutes': len(LANGUAGES),
                      'runtimeTranslationKeys': len(locales['ko'])}))


if __name__ == '__main__':
    validate()
