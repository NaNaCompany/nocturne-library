'use strict';
// Run the production reader in Node's VM with a minimal event-driven DOM.
// Fixture books are in memory; the English text and catalog come from dist/data.
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const vm=require('node:vm');
const root=path.resolve(__dirname,'..');
const read=rel=>fs.readFileSync(path.join(root,rel),'utf8');
const actualCatalog=JSON.parse(read('dist/data/catalog.json'));
const english=actualCatalog.books.find(book=>book.id==='great-gatsby');
const korean={id:'ko-test',title:'한국 <img src=x onerror=alert(1)> 소설',author:'작가 & 이름',language:'ko',publishedYear:null,publicationLabel:'1920년대 판본',authorDeathYear:null,genre:'korean-modern',description:'한글 소개문',sourceUrl:'https://example.org/source',pinnedSourceUrl:'https://example.org/revision/42',historyUrl:'https://example.org/history',license:'Public-domain',licenseUrl:'https://example.org/terms',rightsNote:'공유마당 공공저작물 <검증>',editionNote:'판본 전편 · 문단 분리',sourceInstitution:'출처 기관',sourceCredits:[{name:'공공 아카이브',url:'https://example.org/archive'}],wordCount:1200,wordCountUnit:'eojeol',readingMinutes:10,completeness:'complete',chapterCount:2,file:'books/ko-test.json',txt:'txt/ko-test.txt'};
const travel={...korean,id:'travel-test',title:'기행 시험',genre:'travel',license:'CC-BY-SA-4.0',licenseUrl:'https://creativecommons.org/licenses/by-sa/4.0/',file:'books/travel-test.json',txt:'txt/travel-test.txt'};
const unsafe={...korean,id:'unsafe-test',title:'악성 링크 시험',sourceUrl:'javascript:alert(1)',pinnedSourceUrl:'http://example.org/unsafe',historyUrl:'data:text/html,x',licenseUrl:'javascript:alert(2)',sourceCredits:[],txt:'../../evil.txt'};
const references=[{id:'dongmyeong-ilgi',title:'동명일기',author:'의유당 남씨(귀속 논의 있음)',language:'ko',notice:'본문 미수록 <주의>',sourceUrl:'https://example.org/dongmyeong',status:'external-reference'}];
function fixtureData(book){return {id:book.id,language:'ko',chapters:[{id:'first',title:'첫 장 <태그>',paragraphs:['첫 문단 <script>alert(1)</script>\n둘째 줄','둘째 문단']},{id:'second',title:'둘째 장',paragraphs:['끝 문장']}]};}
class Element{
  constructor(id='',tagName='DIV'){this.id=id;this.tagName=tagName;this.value='';this.children=[];this.dataset={};this.attributes={};this.events={};this.style={setProperty:(k,v)=>this.style[k]=v};this.hidden=false;this.open=false;this.scrollTop=0;this.scrollHeight=1000;this.clientHeight=500;this.offsetHeight=100;this.textContent='';this.innerHTML='';const classes=new Set();this.classList={add:c=>classes.add(c),remove:c=>classes.delete(c),toggle:(c,force)=>{const on=force===undefined?!classes.has(c):force;on?classes.add(c):classes.delete(c);return on;},contains:c=>classes.has(c)};}
  addEventListener(type,fn){(this.events[type]??=[]).push(fn);}
  emit(type,event={}){for(const fn of this.events[type]||[])fn({target:this,...event});}
  setAttribute(k,v){this.attributes[k]=String(v);}
  removeAttribute(k){delete this.attributes[k];}
  appendChild(child){this.children.push(child);}
  replaceChildren(fragment){this.children=fragment.children;this.children.forEach((child,i)=>child.index=i);}
  getBoundingClientRect(){const top=this.tagName==='P'?(this.index||0)*120:0;return {top,bottom:top+100,left:0,right:800};}
  showModal(){this.open=true;}
  close(){this.open=false;}
  focus(){this.focused=true;}
  scrollIntoView(){}
  querySelector(){return null;}
}
async function boot({locale='ko',books=[english,korean,travel,unsafe],refs=references,stored=null,initialHash='',failPath=null,deferPaths=[]}={}){
  const html=read(locale==='ko'?'dist/index.html':`dist/${locale}/index.html`);
  const ids=[...html.matchAll(/\bid="([^"]+)"/g)].map(m=>m[1]);
  const elements=new Map(ids.map(id=>[id,new Element(id)]));
  const get=id=>{assert.ok(elements.has(id),`missing DOM element ${id}`);return elements.get(id);};
  const filters=['all','classic','gothic','adventure','scifi','korean','travel'].map(filter=>{const el=new Element();el.dataset.filter=filter;return el;});
  const preview=new Element();
  const document={documentElement:{lang:locale},body:new Element(),baseURI:'https://reader.example/nocturne/',activeElement:null,hidden:false,title:'',events:{},getElementById:get,createElement:tag=>new Element('',tag.toUpperCase()),createDocumentFragment:()=>new Element(),querySelector:selector=>selector==='.type-preview'?preview:selector==='dialog[open]'?[...elements.values()].find(el=>el.open):null,querySelectorAll:selector=>selector==='.filter'?filters:selector==='dialog[open]'?[...elements.values()].filter(el=>el.open):[],addEventListener(type,fn){this.events[type]=fn;}};
  const location={hash:initialHash,pathname:'/nocturne/',search:'',assigned:null,assign(url){this.assigned=url;},reload(){this.reloaded=true;}};
  const history={entries:[initialHash],index:0,pushState(state,title,url){this.entries=this.entries.slice(0,this.index+1);this.entries.push(url);this.index++;location.hash=url.includes('#')?url.slice(url.indexOf('#')):'';}};
  let storage=stored?JSON.stringify(stored):null;
  const requests=[],errors=[],deferred=new Map();
  const window={events:{},addEventListener(type,fn){this.events[type]=fn;}};
  const context=vm.createContext({window,document,location,history,URL,AbortSignal,console:{error:(...args)=>errors.push(args.join(' '))},localStorage:{getItem:()=>storage,setItem:(key,value)=>{assert.equal(key,'nocturne.reader.v1');storage=value;}},setTimeout:()=>1,clearTimeout:()=>{},requestAnimationFrame:fn=>fn(),fetch:async url=>{requests.push(url);if(deferPaths.includes(url))await new Promise(resolve=>deferred.set(url,resolve));if(url===failPath)return {ok:false,status:503};if(url==='data/catalog.json')return {ok:true,json:async()=>({books,references:refs})};const found=books.find(book=>`data/${book.file}`===url);return {ok:true,json:async()=>found&&['ko-test','travel-test','unsafe-test'].includes(found.id)?fixtureData(found):JSON.parse(read(`dist/${url}`))};}});
  vm.runInContext(read('dist/locales.js'),context,{filename:'locales.js'});
  vm.runInContext(read('dist/app.js'),context,{filename:'app.js'});
  const settle=async()=>{for(let i=0;i<5;i++)await new Promise(resolve=>setImmediate(resolve));};
  const click=(id,dataset={})=>get(id).emit('click',{target:{dataset,closest:selector=>selector==='[data-book]'&&dataset.book?{dataset}:selector==='[data-filter]'&&dataset.filter?filters.find(f=>f.dataset.filter===dataset.filter):selector==='[data-open-bookmark]'&&dataset.openBookmark?{dataset}:selector==='[data-remove-bookmark]'&&dataset.removeBookmark?{dataset}:null}});
  const open=async id=>{click('book-grid',{book:id});await settle();};
  const search=value=>{get('search').value=value;get('search').emit('input');};
  const pop=async hash=>{location.hash=hash;window.events.popstate();await settle();};
  await settle();
  return {get,click,open,search,pop,settle,document,location,history,requests,errors,context,window,releaseFetch:url=>{assert.ok(deferred.has(url),`no pending fetch ${url}`);deferred.get(url)();deferred.delete(url);},saved:()=>JSON.parse(storage)};
}
(async()=>{
  let checks=0;
  for(const locale of ['ko','en','es','zh','ja','de']){
    const app=await boot({locale});const {get}=app;
    assert.equal(app.errors.length,0);
    assert.ok(get('shelf-count').textContent.includes('4'));
    assert.ok(get('result-count').textContent.includes('4'));
    assert.equal((get('book-grid').innerHTML.match(/class="book-card"/g)||[]).length,4);
    assert.match(get('book-grid').innerHTML,/lang="ko"/);
    assert.match(get('book-grid').innerHTML,/&lt;img/);
    assert.doesNotMatch(get('book-grid').innerHTML,/<img/);
    assert.equal(get('references-section').hidden,false);
    assert.match(get('references-list').innerHTML,/동명일기/);
    assert.doesNotMatch(get('references-list').innerHTML,/data-book=/);
    app.search('동명일기');assert.equal(get('book-grid').innerHTML,'');assert.ok(get('result-count').textContent.includes('0'));assert.equal(get('references-section').hidden,false);
    app.search('없음');assert.equal(get('references-section').hidden,true);app.search('');
    app.click('filters',{filter:'korean'});assert.ok(get('result-count').textContent.includes('2'));assert.doesNotMatch(get('book-grid').innerHTML,/data-book="travel-test"/);
    app.click('filters',{filter:'travel'});assert.match(get('book-grid').innerHTML,/data-book="travel-test"/);assert.ok(get('result-count').textContent.includes('1'));app.click('filters',{filter:'all'});
    await app.open('ko-test');assert.equal(get('reading-page').lang,'ko');assert.equal(get('reader-book-title').lang,'ko');assert.equal(get('chapter-text').children[0].textContent,'첫 문단 <script>alert(1)</script>\n둘째 줄');
    app.click('reader-bookmark');const saved=app.saved();assert.equal(saved.bookmarks.length,1);assert.equal(saved.bookmarks[0].bookId,'ko-test');
    app.click('library-bookmarks');assert.match(get('bookmarks-list').innerHTML,/<q lang="ko">첫 문단 &lt;script&gt;/);
    app.click('bookmarks-list',{openBookmark:saved.bookmarks[0].id});await app.settle();assert.equal(get('reading-page').lang,'ko');assert.equal(get('chapter-title').textContent,'첫 장 <태그>');
    app.click('reader-sources');const pd=get('sources-list').innerHTML;assert.match(pd,/https:\/\/example.org\/revision\/42/);assert.match(pd,/data\/txt\/ko-test.txt/);assert.match(pd,/lang="ko">공유마당 공공저작물 &lt;검증&gt;/);assert.doesNotMatch(pd,/CC0|Standard Ebooks|\/tree\//);assert.match(pd,/eojeol|어절|语节|語節|Eojeol/);
    app.click('next-chapter');assert.equal(get('chapter-title').textContent,'둘째 장');assert.equal(app.saved().positions['ko-test'].chapter,1);
    app.click('reader-language');assert.equal(get('reader-language-select').value,locale);
    get('reader-language-select').value='ja';get('reader-language-select').emit('change');assert.equal(app.location.assigned,'https://reader.example/nocturne/ja/#read/ko-test');assert.equal(app.saved().positions['ko-test'].chapter,1);
    await app.open('travel-test');app.click('reader-sources');assert.match(get('sources-list').innerHTML,/CC BY-SA 4.0/);assert.doesNotMatch(get('sources-list').innerHTML,/CC0/);
    await app.open('great-gatsby');assert.equal(get('reading-page').lang,'en');app.click('reader-sources');assert.match(get('sources-list').innerHTML,/CC0 1.0/);assert.match(get('sources-list').innerHTML,/github.com\/standardebooks\/.+\/tree\//);
    app.click('back-library');assert.equal(get('reader-view').hidden,true);assert.equal(app.location.hash,'');await app.pop('#read/ko-test');assert.equal(get('reading-page').lang,'ko');assert.equal(get('chapter-title').textContent,'둘째 장');await app.pop('');assert.equal(get('reader-view').hidden,true);await app.pop('#read/great-gatsby');assert.equal(get('reading-page').lang,'en');
    assert.equal(app.requests.filter(url=>url==='data/books/ko-test.json').length,1,'book cache should avoid duplicate fetches');
    await app.open('unsafe-test');app.click('reader-sources');assert.doesNotMatch(get('sources-list').innerHTML,/href="(?:javascript:|http:|data:)|\.\.\/\.\.\/evil/);assert.doesNotMatch(get('sources-list').innerHTML,/undefined|NaN/);
    const font=get('font-size');font.value=28;font.emit('input');assert.equal(app.saved().settings.size,28);assert.equal(get('reader-view').style['--reading-size'],'28px');
    app.click('library-bookmarks');app.click('bookmarks-list',{removeBookmark:saved.bookmarks[0].id});assert.equal(app.saved().bookmarks.length,0);
    checks+=33;
  }
  // Changing history must never leave rights or contents for the previous book visible.
  const delayed=await boot({deferPaths:['data/books/ko-test.json','data/books/travel-test.json']});
  await delayed.open('great-gatsby');delayed.click('reader-sources');assert.equal(delayed.get('sources-dialog').open,true);assert.match(delayed.get('sources-list').innerHTML,/The Great Gatsby/);
  await delayed.pop('#read/ko-test');assert.equal(delayed.get('sources-dialog').open,false);assert.equal(delayed.get('reader-sources').disabled,true);assert.equal(delayed.get('reader-toc').disabled,true);assert.equal(delayed.get('footer-toc').disabled,true);assert.equal(delayed.get('reader-book-title').textContent,'The Great Gatsby');
  delayed.click('reader-sources');delayed.click('library-sources');delayed.click('reader-toc');delayed.click('footer-toc');assert.equal(delayed.get('sources-dialog').open,false);assert.equal(delayed.get('contents-dialog').open,false);
  delayed.click('reader-settings');assert.equal(delayed.get('settings-dialog').open,true);delayed.releaseFetch('data/books/ko-test.json');await delayed.settle();assert.equal(delayed.get('settings-dialog').open,false);assert.equal(delayed.get('reader-book-title').textContent,korean.title);assert.equal(delayed.get('reader-sources').disabled,false);assert.equal(delayed.get('reader-toc').disabled,false);assert.equal(delayed.get('footer-toc').disabled,false);assert.equal(delayed.get('library-main').attributes['aria-busy'],undefined);
  delayed.click('reader-sources');assert.equal(delayed.get('sources-dialog').open,true);assert.match(delayed.get('sources-list').innerHTML,/data\/txt\/ko-test.txt/);assert.doesNotMatch(delayed.get('sources-list').innerHTML,/The Great Gatsby/);delayed.click('reader-toc');assert.equal(delayed.get('contents-book').textContent,korean.title);
  await delayed.pop('#read/great-gatsby');assert.equal(delayed.get('sources-dialog').open,false);assert.equal(delayed.get('contents-dialog').open,false);delayed.click('reader-sources');assert.match(delayed.get('sources-list').innerHTML,/The Great Gatsby/);assert.equal(delayed.requests.filter(url=>url==='data/books/great-gatsby.json').length,1);
  await delayed.pop('#read/travel-test');await delayed.pop('');assert.equal(delayed.get('reader-view').hidden,true);assert.equal(delayed.get('reader-sources').disabled,false);delayed.releaseFetch('data/books/travel-test.json');await delayed.settle();assert.equal(delayed.get('reader-view').hidden,true);assert.equal(delayed.location.hash,'');assert.equal(delayed.get('library-main').attributes['aria-busy'],undefined);
  // An older request's finally must not enable controls for a newer pending request.
  const overlap=await boot({deferPaths:['data/books/ko-test.json','data/books/travel-test.json']});await overlap.open('great-gatsby');await overlap.pop('#read/ko-test');await overlap.pop('#read/travel-test');overlap.releaseFetch('data/books/ko-test.json');await overlap.settle();assert.equal(overlap.get('reader-sources').disabled,true);assert.equal(overlap.get('library-main').attributes['aria-busy'],'true');assert.equal(overlap.get('reader-book-title').textContent,'The Great Gatsby');overlap.releaseFetch('data/books/travel-test.json');await overlap.settle();assert.equal(overlap.get('reader-book-title').textContent,travel.title);assert.equal(overlap.get('reader-sources').disabled,false);assert.equal(overlap.location.hash,'#read/travel-test');
  // Going back to the current cached book cancels a different pending book.
  const revert=await boot({deferPaths:['data/books/ko-test.json']});await revert.open('great-gatsby');await revert.pop('#read/ko-test');await revert.pop('#read/great-gatsby');assert.equal(revert.get('reader-sources').disabled,false);revert.releaseFetch('data/books/ko-test.json');await revert.settle();assert.equal(revert.get('reader-book-title').textContent,'The Great Gatsby');assert.equal(revert.location.hash,'#read/great-gatsby');
  checks+=40;
  const noRefs=await boot({refs:[]});assert.equal(noRefs.get('references-section').hidden,true);
  const onlyKorean=await boot({books:[korean],refs:[]});assert.match(onlyKorean.get('featured').innerHTML,/한글 소개문/);assert.match(onlyKorean.get('featured').innerHTML,/featured-description" lang="ko"/);assert.doesNotMatch(onlyKorean.get('featured').innerHTML,/undefined/);
  const resume=await boot({initialHash:'#read/ko-test',stored:{settings:{font:'sans',size:27},positions:{'ko-test':{chapter:1,paragraph:0,atTop:true,percent:50}},bookmarks:[{id:'old',bookId:'great-gatsby',chapter:0,paragraph:0,quote:'Old bookmark'}],lastBookId:'ko-test'}});assert.equal(resume.get('chapter-title').textContent,'둘째 장');assert.equal(resume.saved().bookmarks[0].id,'old');assert.equal(resume.get('reader-view').style['--reading-size'],'27px');
  const failure=await boot({failPath:'data/books/ko-test.json'});await failure.open('ko-test');assert.ok(failure.get('toast').textContent.includes('책을 열지 못했어요'));assert.equal(failure.get('library-main').attributes['aria-busy'],undefined);assert.equal(failure.errors.length,1);
  const actual=await boot({books:actualCatalog.books,refs:actualCatalog.references||[]});assert.equal(actual.errors.length,0);assert.ok(actual.get('shelf-count').textContent.includes(String(actualCatalog.books.length)));
  for(const book of actualCatalog.books.filter(book=>book.language==='ko')){await actual.open(book.id);assert.equal(actual.get('reading-page').lang,'ko');assert.ok(actual.get('chapter-text').children.length);actual.click('reader-sources');assert.doesNotMatch(actual.get('sources-list').innerHTML,/undefined|NaN/);}
  assert.equal(actual.errors.length,0);
  assert.match(read('dist/style.css'),/white-space:pre-line/);
  console.log(JSON.stringify({passed:true,locales:6,minimumAssertions:checks+15,actualBooks:actualCatalog.books.length,actualKoreanBooks:actualCatalog.books.filter(book=>book.language==='ko').length,coverage:'catalog counts, separate references, genres/search, escaped text, dynamic reading lang, source/license URLs, eojeol, cache, history, chapter/bookmark/settings restore, language switch, load failure, LF preservation, deferred source/TOC modal isolation, overlap token recovery, cancellation'}));
})().catch(error=>{console.error(error);process.exitCode=1;});
