from pathlib import Path
import hashlib
import json
import re
from html.parser import HTMLParser

ROOT=Path(__file__).resolve().parents[1]
DIST=ROOT/'dist'
DATA=DIST/'data'
h=lambda b:hashlib.sha256(b).hexdigest()
catalog=json.loads((DATA/'catalog.json').read_bytes())['books']
assert len(catalog)==12 and len({b['id'] for b in catalog})==12
package=json.loads((DATA/'package-sha256.json').read_bytes())
for relative,expected in package['files'].items():
    p=DATA/relative
    assert p.resolve().is_relative_to(DATA.resolve()) and p.is_file()
    assert h(p.read_bytes())==expected,relative
sections=0;words=0;paragraphs=0;group_headings=[]
for meta in catalog:
    assert meta['language']=='en' and meta['license']=='CC0-1.0'
    assert meta['authorDeathYear']<=1946 and meta['publishedYear']<=1925
    assert meta['sourceRepository'].startswith('https://github.com/standardebooks/')
    assert re.fullmatch('[a-f0-9]{40}',meta['sourceCommit'])
    for key in ['sourceUrl','sourceRepository','licenseUrl']:assert meta[key].startswith('https://')
    book=json.loads((DATA/meta['file']).read_bytes())
    assert book['id']==meta['id'] and len(book['chapters'])==meta['chapterCount']
    assert len({c['id'] for c in book['chapters']})==len(book['chapters'])
    for chapter in book['chapters']:
        assert chapter['title'] and isinstance(chapter['paragraphs'],list)
        if not chapter['paragraphs']:
            group_headings.append((meta['id'],chapter['id'],chapter['title']))
        assert all(isinstance(p,str) and p.strip() for p in chapter['paragraphs'])
        paragraphs+=len(chapter['paragraphs'])
    raw=(DATA/meta['txt']).read_bytes()
    assert not raw.startswith(b'\xef\xbb\xbf') and b'\r' not in raw
    raw.decode('utf-8')
    sections+=len(book['chapters']);words+=meta['wordCount']
verification=json.loads((DATA/'verification.json').read_bytes())
assert verification['sourceToExportBodyIntegrity'] is True and verification['translatedBooks']==0
assert sections==450 and words==1149507 and paragraphs==verification['verifiedTextBlocks']
assert set(group_headings)=={(b,'endnotes','Endnotes') for b in ['frankenstein','moby-dick','time-machine']}
class Document(HTMLParser):
    def __init__(self):super().__init__();self.ids=[];self.assets=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id'in a:self.ids.append(a['id'])
        if tag=='script' and a.get('src'):self.assets.append(a['src'])
        if tag=='link' and a.get('rel')in ['stylesheet','icon']:self.assets.append(a['href'])
doc=Document();doc.feed((DIST/'index.html').read_text(encoding='utf-8'))
assert len(doc.ids)==len(set(doc.ids))
for asset in doc.assets:assert not asset.startswith(('http:','https:','//')) and (DIST/asset).is_file()
js=(DIST/'app.js').read_text(encoding='utf-8')
languages=['ko','en','es','zh','ja','de']
locale_source=(DIST/'locales.js').read_text(encoding='utf-8')
locales=json.loads(locale_source.split('window.NOCTURNE_I18N = ',1)[1].rstrip().removesuffix(';'))
assert set(locales)==set(languages)
assert len({frozenset(v) for v in locales.values()})==1
for lang in languages:
    page=DIST/'index.html' if lang=='ko' else DIST/lang/'index.html'
    html=page.read_text(encoding='utf-8')
    assert f'<html lang="{lang}">' in html
    assert ('<base href="../">' in html)==(lang!='ko')
    localdoc=Document();localdoc.feed(html)
    assert len(localdoc.ids)==len(set(localdoc.ids))
    assert {'language-select','reader-language','reader-language-select','language-dialog'}.issubset(localdoc.ids)
    assert len(re.findall(r'<option value="(?:ko|en|es|zh|ja|de)"',html))==12
    for asset in localdoc.assets:assert not asset.startswith(('http:','https:','//')) and (DIST/asset).is_file()
    assert all(isinstance(v,str) and v for v in locales[lang].values())
    if lang!='ko':
        no_options=re.sub(r'<option\b.*?</option>','',html,flags=re.S)
        assert not re.search('[가-힣]',no_options),lang
for key in re.findall(r"\bt\('([^']+)'",js):assert key in locales['ko'],key
generated_ids=set(re.findall(r'\bid="([a-z][a-z0-9-]*)"',js))
for ident in re.findall(r"\$\('([^']+)'\)",js):assert ident in doc.ids or ident in generated_ids,ident
assert 'background:#000' in (DIST/'style.css').read_text(encoding='utf-8')
for p in DIST.rglob('*'):
    if p.is_file():
        assert p.suffix.lower() not in ['.jpg','.jpeg','.png','.webp','.woff','.woff2','.ttf','.pdf']
        assert b'C:\\Users\\' not in p.read_bytes() and b'C:/Users/' not in p.read_bytes()
print(json.dumps({'pass':True,'books':len(catalog),'sections':sections,'groupHeadings':len(group_headings),'textBlocks':paragraphs,'words':words,
                  'translatedBooks':0,'pinnedExportHashes':len(package['files']),'htmlIds':len(doc.ids),
                  'externalImagesFontsAndLibraries':0,'languageRoutes':len(languages),'runtimeTranslationKeys':len(locales['ko'])}))
