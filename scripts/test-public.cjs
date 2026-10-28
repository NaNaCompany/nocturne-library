const test=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const vm=require('node:vm');
const {pathToFileURL}=require('node:url');
const root=path.resolve(__dirname,'..'),out=path.join(root,'docs');
const cfg=JSON.parse(fs.readFileSync(path.join(root,'APP_PUBLIC.json'),'utf8'));
const catalog=JSON.parse(fs.readFileSync(path.join(out,'data/catalog.json'),'utf8'));
const read=p=>fs.readFileSync(path.join(out,p),'utf8');
const files=dir=>fs.readdirSync(dir,{withFileTypes:true}).flatMap(e=>e.isDirectory()?files(path.join(dir,e.name)):[path.join(dir,e.name)]);
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const ids=['G-2ZYSF0173P','GTM-NV2WWQXB','ca-pub-9767176956440077','9f3423bb0d034d91bbe1a12afeff2429'];
const expected=[...cfg.languages.map(l=>l==='ko'?'index.html':`${l}/index.html`),...catalog.books.map(b=>`book/${b.id}/index.html`)];
const urlFor=p=>cfg.url+(p==='index.html'?'':p.replace(/index.html$/,''));
const publisher=()=>import(pathToFileURL(path.join(__dirname,'publisher-tracking.mjs')));

for(const relative of expected){
 test(`HTML metadata, local assets and four guarded integrations: ${relative}`,()=>{
  const html=read(relative);
  assert.match(html,/<!doctype html>/i);
  assert.equal((html.match(/<link rel="canonical"/g)||[]).length,1);
  assert.ok(html.includes(`<link rel="canonical" href="${urlFor(relative)}">`));
  assert.match(html,/<meta name="robots" content="index,follow">/);
  assert.doesNotMatch(html,/noindex|NaNa Lab<\/title>|undefined|null<\/dd>/);
  for(const id of ids)assert.ok(html.includes(id),id);
  assert.equal((html.match(/data-publisher-bootstrap/g)||[]).length,1);
  assert.match(html,/<noscript data-publisher-gtm-fallback="GTM-NV2WWQXB">/);
  assert.doesNotMatch(html,/<iframe\b|<script\b[^>]*src=["']https?:/);
  const baseMatch=html.match(/<base href="([^"]+)"/),htmlDir=path.dirname(path.join(out,relative));
  const assetDir=baseMatch?path.resolve(htmlDir,baseMatch[1]):htmlDir;
  for(const m of html.matchAll(/<(?:script|link)\b[^>]*(?:src|href)="([^"]+)"[^>]*>/g)){
   const link=m[1];if(/^(?:https?:|#|data:)/.test(link))continue;
   assert.ok(fs.existsSync(path.resolve(assetDir,link)),relative+': '+link);
  }
  assert.match(html,/https:\/\/nanalab\.kr\/apps\//);
  for(const m of html.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g))assert.ok(JSON.parse(m[1]));
 });
}

test('every HTML file is covered and every library page links all book detail pages',()=>{
 const generated=files(out).filter(p=>p.endsWith('.html')).map(p=>path.relative(out,p).replaceAll('\\','/'));
 assert.deepEqual(generated.sort(),expected.slice().sort());
 for(const lang of cfg.languages){
  const relative=lang==='ko'?'index.html':`${lang}/index.html`,html=read(relative);
  for(const l of [...cfg.languages,'x-default'])assert.ok(html.includes(`hreflang="${l}"`));
  assert.equal((html.match(/<details class="edition-index shell">/g)||[]).length,1);
  for(const b of catalog.books)assert.ok(html.includes(`href="${cfg.url}book/${b.id}/"`),b.id);
 }
});

for(const b of catalog.books){
 test(`actual contents, reader, download and accurate schema: ${b.id}`,()=>{
  const html=read(`book/${b.id}/index.html`),book=JSON.parse(read('data/'+b.file));
  const schema=JSON.parse(html.match(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/)[1]);
  assert.equal(schema['@type'],'Book');assert.equal(schema.name,b.title);assert.equal(schema.author.name,b.author);
  assert.equal(schema.inLanguage,b.language);assert.equal(schema.url,`${cfg.url}book/${b.id}/`);
  assert.equal(schema.mainEntityOfPage['@id'],schema.url);assert.equal(schema.license,b.licenseUrl);
  assert.equal(schema.datePublished,Number.isInteger(b.publishedYear)?String(b.publishedYear):undefined);
  assert.equal(schema.dateCreated,Number.isInteger(b.createdYear)?String(b.createdYear):undefined);
  assert.equal(schema.numberOfPages,undefined);
  assert.ok(html.includes(`href="${cfg.url}#read/${b.id}"`));
  assert.ok(html.includes(`href="${esc(cfg.url+'data/'+b.txt)}" download`));
  assert.ok(fs.existsSync(path.join(out,'data',b.txt)));
  assert.ok(html.includes(esc(b.rightsNote)));
  assert.ok(html.includes(esc(new URL(b.sourceUrl).href)));
  assert.ok(html.includes(esc(new URL(b.licenseUrl).href)));
  if(b.attribution)assert.ok(html.includes(esc(b.attribution)));
  if(b.scanPageRevisionsUrl)assert.ok(html.includes('href="'+esc(new URL(b.scanPageRevisionsUrl).href)+'"'));
  for(const m of b.modifications||[])assert.ok(html.includes(esc(m)));
  assert.equal((html.match(/<ol>/g)||[]).length,1);
  const toc=html.match(/<ol>([\s\S]*?)<\/ol>/)[1];
  assert.equal((toc.match(/<li\b/g)||[]).length,book.chapters.length);
  for(const c of book.chapters)assert.ok(toc.includes(esc(c.title)),c.title);
 });
}

test('sitemap contains every public canonical route once and no fragments or query strings',()=>{
 const xml=read('sitemap.xml');
 assert.match(xml,/^<\?xml version="1.0" encoding="UTF-8"\?>\n<urlset xmlns="http:\/\/www.sitemaps.org\/schemas\/sitemap\/0.9">/);
 const matches=[...xml.matchAll(/<url><loc>([^<]+)<\/loc><\/url>/g)].map(m=>m[1]);
 assert.deepEqual(matches,expected.map(urlFor));assert.equal(new Set(matches).size,matches.length);
 assert.equal((xml.match(/<url>/g)||[]).length,matches.length);
 for(const url of matches){const u=new URL(url);assert.equal(u.search,'');assert.equal(u.hash,'');assert.ok(url.endsWith('/'));}
 assert.ok(read('robots.txt').includes(`Sitemap: ${cfg.url}sitemap.xml`));
 assert.ok(fs.existsSync(path.join(out,'.nojekyll')));
});

function browser(source,{protocol='https:',hostname='nanalab.kr',readyState='complete',edge=false}={}){
 const scripts=edge?[{src:'https://static.cloudflareinsights.com/beacon.min.js'}]:[],listeners={};
 const document={title:'NOCTURNE',readyState,head:{appendChild:s=>scripts.push(s)},createElement:()=>({attrs:{},setAttribute(k,v){this.attrs[k]=v;}}),querySelectorAll:()=>scripts,querySelector:()=>scripts.find(s=>s.src.includes('static.cloudflareinsights.com/beacon.min.js'))||null,addEventListener:(n,fn)=>listeners[n]=fn};
 const window={location:{protocol,hostname,origin:`${protocol}//${hostname}`,pathname:'/nocturne-library/',search:'?private=search-input',hash:'#private-input'}};
 const ctx=vm.createContext({window,document,Date,JSON,Object,String});
 return {scripts,listeners,window,run:()=>vm.runInContext(source,ctx)};
}

test('publisher helper is idempotent, removes old ungated integrations and preserves data scripts',async()=>{
 const {completeTracking}=await publisher();
 const html='<html><head><title>Test</title><script src="https://www.googletagmanager.com/gtag/js?id=G-OLDOLD"></script><script>gtag("config","G-OLDOLD")</script><link rel="preconnect" href="https://www.googletagmanager.com"></head><body><noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-OLD"></iframe></noscript><script type="application/ld+json">{"@type":"Book"}</script></body></html>';
 const once=completeTracking(html);assert.equal(completeTracking(once),once);
 assert.doesNotMatch(once,/G-OLDOLD|GTM-OLD|<iframe|preconnect/);assert.match(once,/application\/ld\+json/);
});

test('publisher creates zero requests and no tracking state on local, preview and HTTP hosts',async()=>{
 const {publisherHead}=await publisher(),source=publisherHead().match(/<script[^>]*>([\s\S]*?)<\/script>/)[1];
 for(const hostname of ['localhost','127.0.0.1','127.1.2.3','::1','[::1]','0.0.0.0','preview.test','nanalab.kr.evil.test','nanacompany.github.io.evil.test']){
  const b=browser(source,{hostname});b.run();assert.equal(b.scripts.length,0,hostname);assert.equal(b.window.dataLayer,undefined);
 }
 for(const protocol of ['http:','file:','about:']){const b=browser(source,{protocol});b.run();assert.equal(b.scripts.length,0);}
});

test('publisher creates exactly four scripts once on HTTPS production and excludes input from own page-view payload',async()=>{
 const {publisherHead}=await publisher(),source=publisherHead().match(/<script[^>]*>([\s\S]*?)<\/script>/)[1];
 for(const hostname of ['nanalab.kr','nanacompany.github.io','games.nanalab.kr']){
  const b=browser(source,{hostname});b.run();b.run();assert.equal(b.scripts.length,4);assert.equal(new Set(b.scripts.map(s=>s.src)).size,4);
  const views=b.window.dataLayer.filter(x=>x[0]==='event'&&x[1]==='page_view');assert.equal(views.length,1);
  assert.equal(views[0][2].page_location,`https://${hostname}/nocturne-library/`);assert.equal(views[0][2].page_referrer,'');
  assert.doesNotMatch(JSON.stringify(b.window.dataLayer),/private|search-input/);
 }
 for(const readyState of ['loading','complete']){
  const b=browser(source,{readyState,edge:true});b.run();if(readyState==='loading')b.listeners.DOMContentLoaded();
  assert.equal(b.scripts.length,4);assert.equal(b.scripts.filter(s=>s.src.includes('cloudflareinsights.com')).length,1);
 }
});
