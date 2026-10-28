# NOCTURNE · 밤의 서재

한국어 10편과 영어 원작 12권을 검은 배경과 흰 글자로 읽는 정적 전자책 앱입니다. 개화기 신소설·고전소설·기행 가사를 추가했습니다. 새 번역·각색을 만들지 않으며 공식 제공 전사본에 현대 표기가 있는 경우 해당 판본을 명시합니다. 총 22편·481개 읽기 섹션을 제공합니다.

| 추가 작품 | 저자 | 판본·수록 범위 |
|---|---|---|
| 혈의 누 | 이인직 | 상편 원철자 전사 전체 |
| 치악산 | 이인직 | 상편 원철자 전사 전체 |
| 자유종·구마검 | 이해조 | 공유마당 제공 현대 표기 전사 |
| 빈상설·화의 혈 | 이해조 | 공유마당 제공 옛 표기 전사 |
| 공진회·금수회의록 | 안국선 | 공유마당 제공 전사 |
| 홍길동전 | 허균 전칭 | 30장 경판본 옛 표기 전사, 간행연도 미상 |
| 관동별곡 | 정철 | 고어 기행 가사 146행, 소설 아님; 1580년은 창작연도 |

혈의 누·치악산의 하편은 포함하지 않습니다. 홍길동전의 ‘30장’은 판본 장수이며 읽기 장 수가 아닙니다. 동명일기는 확보한 현대 표기층의 저본·권리 경로를 확인하지 못해 앱 본문·TXT에서 제외하고 **외부 원문 안내**만 제공합니다. 이 안내는 22편에 포함하지 않습니다. 성산별곡의 제공본은 실제 누락이 확인되어 제외했습니다.

## 기능

- 원문 독서, 목차와 이전/다음 섹션 이동
- 제목·작가 검색, 장르 필터
- 기기 내 책갈피·독서 위치·읽기 설정 저장
- 글자 크기·행간·문장 폭·명도·Serif/Sans 조절
- 집중 모드, 키보드 방향키 탐색
- UTF-8 TXT 저장과 작품별 원문·라이선스·수집 내역

독서 배경은 항상 `#000000`입니다. 기본 본문은 `rgb(240,240,240)`이며 밝기를 낮출 수 있습니다. 기록은 이 브라우저의 localStorage에 저장되므로 브라우저·기기 간 동기화되지 않습니다. 네트워크가 없을 때 앱 전체를 새로 여는 오프라인 기능은 제공하지 않습니다.

## 콘텐츠와 권리

원작의 보호기간과 전자 판본의 이용 조건을 따로 확인합니다. 영어 12권은 Standard Ebooks 고정 커밋과 판본 기여분 CC0 1.0을 유지합니다. 한국어 7편은 한국저작권위원회 공유마당이 해당 TXT에 표시한 자유이용 만료 조건을 확인했습니다. 한국어 위키문헌 전사 3편(혈의 누 상편·치악산 상편·홍길동전 경판본)은 CC BY-SA 4.0으로 제공하며 출처·기여 이력·고정판·변경 내역을 JSON·TXT에도 포함합니다. 이 라이선스를 다른 책이나 앱 코드 전체에 적용하지 않습니다.

전 세계 모든 국가에서 보호기간이 끝났다고 주장하지 않습니다. 상세 근거는 `dist/data/sources.json`, `research/RIGHTS.md`, `research/korean-editions/manifest.json`, `research/korean-editions/RIGHTS-REVIEW.md`에 있습니다. 1968년 전집 저본 표기는 보존하며 다른 현대 출판물 전체의 권리 만료를 주장하지 않습니다. 원본 스캔의 모든 글자를 수작업으로 교정한 판본은 아닙니다. 이해조 고어 전사본의 PUA는 ISC 라이선스 `hypua-unicoder@1.0.0`의 공개 매핑으로 표준 유니코드 자모로 변환했고 도구 라이선스·변경 내역을 보존합니다.

삽화·이미지·폰트를 가져오지 않았습니다. 타이포그래피 표지는 앱을 위해 직접 만든 CSS입니다. 원작에 포함된 다른 언어 구절도 번역하지 않았습니다. Jane Eyre 에디션의 추가 번역 각주 52개는 제외했고 원작의 외국어 구절과 1848년 작가 주는 보존했습니다. 따라서 삽화와 편집상 추가물을 포함하는 원본 전자책 전체의 시각적 복제본은 아닙니다.

## 로컬 실행·검증

```text
python -m http.server 8876 --bind 127.0.0.1 --directory dist
python scripts/import-korean.py
python scripts/localize.py
python scripts/validate.py
node scripts/test-reader.cjs
node scripts/build-public.mjs
node scripts/test-public.cjs
```

GitHub Pages는 `main`의 `/docs`를 배포합니다. `dist/`는 앱 소스, `docs/`는 공개 빌드 출력입니다. Sites 배포를 사용하지 않습니다. `import-korean.py`는 검토·고정한 스냅샷의 해시를 확인하고 신규 책·출처·카탈로그를 재생성합니다. 네트워크의 최신 판본을 임의로 가져오지 않습니다.

## 인터페이스 언어

한국어는 루트(`/`), 영어·스페인어·중국어·일본어·독일어는 각각 `/en/`, `/es/`, `/zh/`, `/ja/`, `/de/`에서 제공합니다. 서재의 언어 선택과 읽기 화면의 언어 버튼으로 전환할 수 있습니다. 전환할 때 열어 둔 책의 해시와 이 브라우저에 저장한 읽기 위치·설정을 유지합니다. 작품 본문·제목·작가명·TXT 다운로드는 해당 판본의 한국어·영어를 유지합니다. 한국어 어절 수와 읽기 시간은 인쇄 줄바꿈을 포함한 공백 단위 추산입니다.

정적 페이지는 `scripts/index.template.html`과 `scripts/localize.py`에서 재생성합니다. `python scripts/localize.py`는 6개 HTML과 UI 전용 `dist/locales.js`만 생성하며 `dist/data/`를 수정하지 않습니다. 기존 영어 JSON/TXT 24개는 2026-10-26 패키지 해시와 바이트가 같습니다. 검증기는 원래 본문·신규 10편·출처·독립 TXT 권리 고지·고정 전사 페이지 목록·언어 경로·UI를 검사합니다.

## Public GitHub Pages release

Launch: https://nanalab.kr/nocturne-library/

Korean is at the root. English, Spanish, Chinese, Japanese and German use `/en/`, `/es/`, `/zh/`, `/ja/`, `/de/`.
GitHub Pages serves `main` → `/docs` using the branch build. No project CNAME is used.

Build: `node scripts/build-public.mjs`. The public build adds six interface routes, 22 static book detail/contents/source pages, canonical URLs, Book structured data, a 28-URL sitemap and publisher integrations. Original book text and the existing visual design are preserved.

Publisher integrations: AdSense, Google Tag Manager, Google Analytics and Cloudflare Web Analytics. Requests load only on the production HTTPS allowlist. Local previews do not request publisher services. Reading positions and bookmarks stay in this browser. Current verification and release results are recorded in `UPDATE.md`.

Original JPEG cards are rendered from original text and geometry using an installed system font; no font files are redistributed. Existing source references and third-party notices remain applicable.
