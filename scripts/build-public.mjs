import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {completeTracking} from './publisher-tracking.mjs';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const cfg=JSON.parse(fs.readFileSync(path.join(root,'APP_PUBLIC.json'),'utf8'));
const src=path.join(root,'dist'), out=path.join(root,'docs');
const catalog=JSON.parse(fs.readFileSync(path.join(src,'data/catalog.json'),'utf8'));
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const safe=s=>{try{const u=new URL(s);return u.protocol==='https:'?u.href:null;}catch{return null;}};
const write=(p,s)=>{fs.mkdirSync(path.dirname(p),{recursive:true});fs.writeFileSync(p,s.trimEnd()+'\n');};
const bookPath=id=>{if(!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(id))throw new Error('Unsafe book id: '+id);return `book/${id}/`;};
const json=s=>JSON.stringify(s).replace(/</g,'\\u003c').replace(/\u2028/g,'\\u2028').replace(/\u2029/g,'\\u2029');
const checkedRead=relative=>{const p=path.resolve(src,'data',relative);if(!p.startsWith(path.join(src,'data')+path.sep))throw new Error('Unsafe data path');return JSON.parse(fs.readFileSync(p,'utf8'));};
const indexLabels={ko:'작품별 판본·출처·목차',en:'Editions, sources and contents',es:'Ediciones, fuentes e índices',zh:'版本、来源与目录',ja:'作品の版・出典・目次',de:'Ausgaben, Quellen und Inhalt'};

fs.mkdirSync(out,{recursive:true});
fs.cpSync(src,out,{recursive:true,filter:p=>!p.split(path.sep).includes('.openai')});
fs.cpSync(path.join(root,'public-assets'),out,{recursive:true});
// A base element must not move hash-only reader navigation out of a language route.
const appJs=path.join(out,'app.js');
let js=fs.readFileSync(appJs,'utf8');
js=js.replace("history.pushState({reader:id},'',`#read/${id}`)","history.pushState({reader:id},'',location.pathname+location.search+`#read/${id}`)");
fs.writeFileSync(appJs,js);
const links=cfg.languages.map(l=>`<link rel="alternate" hreflang="${esc(l)}" href="${esc(cfg.url+(l==='ko'?'':l+'/'))}">`).join('\n')+`\n<link rel="alternate" hreflang="x-default" href="${esc(cfg.url)}">`;
for(const lang of cfg.languages){
 const file=path.join(out,lang==='ko'?'index.html':lang+'/index.html');
 let html=fs.readFileSync(file,'utf8');
 html=html.replace(/<meta\b[^>]*\bname=["']robots["'][^>]*>/gi,'');
 html=html.replace(/<link\b[^>]*\brel=["'](?:canonical|alternate)["'][^>]*>/gi,'');
 html=html.replace(/<meta\b[^>]*(?:\bname=["'](?:description|twitter:[^"']+)["']|\bproperty=["']og:[^"']+["'])[^>]*>/gi,'');
 const text=cfg.locales[lang], url=cfg.url+(lang==='ko'?'':lang+'/');
 html=html.replace(/<title>[^]*?<\/title>/i,'<title>'+esc(text.name)+'</title>');
 const meta=`\n<meta name="robots" content="index,follow">\n<meta name="description" content="${esc(text.description)}">\n<link rel="canonical" href="${esc(url)}">\n${links}\n<meta property="og:type" content="website">\n<meta property="og:url" content="${esc(url)}">\n<meta property="og:title" content="${esc(text.name)}">\n<meta property="og:description" content="${esc(text.description)}">\n<meta property="og:image" content="${esc(cfg.url)}og/${lang}.jpg">\n<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n<meta name="twitter:card" content="summary_large_image">\n<meta name="twitter:title" content="${esc(text.name)}">\n<meta name="twitter:description" content="${esc(text.description)}">\n<meta name="twitter:image" content="${esc(cfg.url)}og/${lang}.jpg">\n<link rel="stylesheet" href="public.css">\n`;
 html=html.replace(/<\/head>/i,meta+'</head>');
 const editionIndex=`<details class="edition-index shell"><summary>${esc(indexLabels[lang]||indexLabels.en)}</summary><ul>${catalog.books.map(b=>`<li><a href="${esc(cfg.url+bookPath(b.id))}" lang="${esc(b.language)}">${esc(b.title)} · ${esc(b.author)}</a></li>`).join('')}</ul></details>`;
 html=html.replace(/<footer\b/i,editionIndex+'\n<footer');
 html=completeTracking(html);
 write(file,html.replace(/^[\t ]+$/gm,''));
}

const labels={
 ko:{library:'서재',read:'본문 읽기',txt:'TXT 다운로드',contents:'수록 목차',edition:'판본 및 수록 범위',source:'원문 제공 페이지',pinned:'확인한 판본·파일',history:'전사 이력·기여자',scanPages:'개별 전사 페이지 고정판·기여자',rights:'권리 및 출처',license:'이용 조건',credit:'판본 기여자',changes:'변환·수정 내역',records:'전체 출처·고정판 기록',year:'발표·출판 연도',unknown:'연도 미상',count:'절',download:'한국어 작품 TXT에는 출처·이용 조건·변경 내역이 포함됩니다. 영어 작품은 이 페이지와 전체 출처 자료를 함께 확인하세요.',language:'본문 언어',ko:'한국어',en:'영어',scope:'직접 수록한 판본의 목차입니다. 상편·경판본 등 표기된 수록 범위를 확인하세요.'},
 en:{library:'Library',read:'Read text',txt:'Download TXT',contents:'Included contents',edition:'Edition and scope',source:'Source edition',pinned:'Verified edition or file',history:'Transcription history and contributors',scanPages:'Pinned transcription pages and contributors',rights:'Rights and provenance',license:'Reuse terms',credit:'Edition contributors',changes:'Extraction and modification notices',records:'Complete sources and revision records',year:'First publication year',unknown:'Year unknown',count:'sections',download:'Korean TXT editions preserve source, reuse and modification notices. For English TXT editions, retain this page and the complete source records.',language:'Text language',ko:'Korean',en:'English',scope:'Contents of the included text edition. Volume and edition limits are stated in the title and edition notes.'}
};
const bookStyle=`.edition-index{padding:20px 0 34px;color:#aaa;font-size:12px}.edition-index summary{cursor:pointer;line-height:1.8}.edition-index ul{columns:2;padding-left:20px;line-height:2}.edition-index a{text-decoration:underline;text-underline-offset:4px}.book-page{max-width:840px;width:calc(100% - 40px);margin:0 auto;padding:32px 0 72px;line-height:1.8;overflow-wrap:anywhere}.book-page nav{font-size:13px;margin-bottom:32px}.book-page a{text-decoration:underline;text-underline-offset:4px}.book-page h1{font-size:clamp(28px,5vw,46px);font-weight:400;line-height:1.35;margin:12px 0}.book-page h2{font-size:20px;font-weight:400;border-top:1px solid #292929;padding-top:24px;margin-top:32px}.book-page p,.book-page li,.book-page dd{font-size:14px;color:#bcb7be}.book-page .byline{font-size:17px}.book-page .actions{display:flex;gap:16px;flex-wrap:wrap;margin:28px 0 8px}.book-page .actions a{display:inline-flex;align-items:center;border:1px solid #555;padding:10px 16px;min-height:44px;color:#eee}.book-page dl{display:grid;grid-template-columns:150px minmax(0,1fr);gap:8px 18px}.book-page dt{color:#999;font-size:13px}.book-page dd{margin:0}.book-page ol{padding-left:26px}.book-page .source-links{display:flex;gap:16px;flex-wrap:wrap}.book-page .source-links a{font-size:13px}.book-page .notice{font-size:12px;color:#999}.book-page [lang=ko]{word-break:keep-all;overflow-wrap:anywhere}@media(max-width:600px){.edition-index ul{columns:1}.book-page dl{grid-template-columns:1fr;gap:2px}.book-page dd{margin-bottom:10px}}`;
const publisherCss='a[href="https://nanalab.kr/apps/"]{position:fixed!important;right:14px!important;bottom:12px!important;z-index:30!important;color:#888!important;font:11px/1.4 system-ui,sans-serif!important;letter-spacing:0!important;text-decoration:none!important;background:none!important;border:0!important;padding:3px!important;box-shadow:none!important}a[href="https://nanalab.kr/apps/"]:focus-visible{outline:2px solid #888;outline-offset:3px}@media print{a[href="https://nanalab.kr/apps/"]{display:none!important}}';
write(path.join(out,'public.css'),publisherCss+'\n'+bookStyle);

for(const b of catalog.books){
 const book=checkedRead(b.file),lang=b.language==='ko'?'ko':'en',t=labels[lang];
 const metadataLanguage=b.metadataLanguage||'ko';
 const url=cfg.url+bookPath(b.id), reader=cfg.url+`#read/${b.id}`;
 const description=String(b.description||'');
 const license=safe(b.licenseUrl),source=safe(b.sourceUrl);
 const pinned=safe(b.pinnedSourceUrl)|| (safe(b.sourceRepository)&&/^[a-f0-9]{40}$/.test(b.sourceCommit||'')?b.sourceRepository+'/tree/'+b.sourceCommit:null);
 const history=safe(b.historyUrl),scanPages=safe(b.scanPageRevisionsUrl);
 const link=(href,label)=>href?`<a href="${esc(href)}" rel="noopener noreferrer">${esc(label)}</a>`:'';
 const credit=(b.sourceCredits||[]).map(c=>{const name=typeof c==='string'?c:c.name,roles=typeof c==='object'&&Array.isArray(c.roles)?` (${c.roles.join(', ')})`:'';return `<li>${safe(c.url)?link(safe(c.url),name):esc(name)}${esc(roles)}</li>`;}).join('');
 const sourceName=b.sourceInstitution||b.sourceOrganization||b.sourceName|| (b.sourceRepository?'Standard Ebooks':'');
 const year=b.publicationLabel??b.publishedYear??t.unknown;
 const schema={'@context':'https://schema.org','@type':'Book',name:b.title,url,mainEntityOfPage:{'@type':'WebPage','@id':url},author:{'@type':'Person',name:b.author},inLanguage:b.language,isAccessibleForFree:true,bookFormat:'https://schema.org/EBook'};
 if(Number.isInteger(b.publishedYear))schema.datePublished=String(b.publishedYear);
 if(Number.isInteger(b.createdYear))schema.dateCreated=String(b.createdYear);
 if(license)schema.license=license;
 if(source)schema.isBasedOn=source;
 if(b.editionNote)schema.bookEdition=b.editionNote;
 const html=`<!doctype html>
<html lang="${lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>${esc(b.title)} · NOCTURNE</title>
<meta name="robots" content="index,follow"><meta name="description" content="${esc(description)}"><link rel="canonical" href="${esc(url)}">
<meta property="og:type" content="book"><meta property="og:url" content="${esc(url)}"><meta property="og:title" content="${esc(b.title)}"><meta property="og:description" content="${esc(description)}"><meta property="og:image" content="${esc(cfg.url)}og/${lang}.jpg"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="${esc(b.title)}"><meta name="twitter:description" content="${esc(description)}"><meta name="twitter:image" content="${esc(cfg.url)}og/${lang}.jpg">
<link rel="stylesheet" href="../../style.css"><link rel="stylesheet" href="../../public.css"><link rel="icon" href="../../icon.svg" type="image/svg+xml"><script type="application/ld+json">${json(schema)}</script></head>
<body><main class="book-page"><nav><a href="${esc(cfg.url)}">${esc(t.library)}</a></nav><h1 lang="${esc(b.language)}">${esc(b.title)}</h1><p class="byline" lang="${esc(b.language)}">${esc(b.author)}</p>
<p lang="${esc(metadataLanguage)}">${esc(description)}</p><dl><dt>${esc(t.language)}</dt><dd>${esc(t[b.language]||b.language)}</dd><dt>${esc(t.year)}</dt><dd>${esc(year)}</dd><dt>${esc(t.contents)}</dt><dd>${book.chapters.length} ${esc(t.count)}</dd></dl>
<div class="actions"><a href="${esc(reader)}">${esc(t.read)}</a><a href="${esc(cfg.url+'data/'+b.txt)}" download>${esc(t.txt)}</a></div><p class="notice">${esc(t.download)}</p>
<h2>${esc(t.edition)}</h2><p lang="${esc(metadataLanguage)}">${esc(b.editionNote||b.rightsNote)}</p><p class="notice">${esc(t.scope)}</p>
<h2>${esc(t.contents)}</h2><ol>${book.chapters.map(c=>`<li lang="${esc(b.language)}">${esc(c.title)}</li>`).join('')}</ol>
<h2>${esc(t.rights)}</h2><p lang="${esc(metadataLanguage)}">${esc(b.rightsNote)}</p><p>${esc(sourceName)}</p><p>${esc(b.license)} ${link(license,t.license)}</p><div class="source-links">${link(source,t.source)}${link(pinned,t.pinned)}${link(history,t.history)}${link(scanPages,t.scanPages)}</div>
<p lang="${esc(metadataLanguage)}">${esc(b.attribution||'')}</p><p lang="${esc(metadataLanguage)}">${esc(b.sourceVersionNote||'')}</p>${Array.isArray(b.modifications)&&b.modifications.length?`<h2>${esc(t.changes)}</h2><ul>${b.modifications.map(m=>`<li>${esc(m)}</li>`).join('')}</ul>`:''}<p>${link(cfg.url+'data/sources.json',t.records)}</p>${credit?`<h2>${esc(t.credit)}</h2><ul>${credit}</ul>`:''}</main><a href="https://nanalab.kr/apps/">More Apps</a></body></html>`;
 write(path.join(out,bookPath(b.id),'index.html'),completeTracking(html));
}
const urls=[...cfg.languages.map(l=>cfg.url+(l==='ko'?'':l+'/')),...catalog.books.map(b=>cfg.url+bookPath(b.id))];
if(new Set(urls).size!==urls.length)throw new Error('Duplicate sitemap URL');
write(path.join(out,'sitemap.xml'),'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+urls.map(u=>'<url><loc>'+esc(u)+'</loc></url>').join('\n')+'\n</urlset>');
write(path.join(out,'robots.txt'),'User-agent: *\nAllow: /\nSitemap: '+cfg.url+'sitemap.xml');
fs.writeFileSync(path.join(out,'.nojekyll'),'');
console.log(JSON.stringify({slug:cfg.slug,languages:cfg.languages.length,books:catalog.books.length,sitemapUrls:urls.length,output:'docs'}));
