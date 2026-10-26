# NOCTURNE · 밤의 서재

검은 배경과 흰 글자로 저작권 보호기간이 지난 영문 원작을 읽는 정적 전자책 앱입니다. 번역본을 수록하지 않습니다. 12권의 원작, 397개 본장과 헌사·전서문·원작 각주를 포함한 450개 읽기 섹션을 제공합니다.

## 기능

- 원문 독서, 목차와 이전/다음 섹션 이동
- 제목·작가 검색, 장르 필터
- 기기 내 책갈피·독서 위치·읽기 설정 저장
- 글자 크기·행간·문장 폭·명도·Serif/Sans 조절
- 집중 모드, 키보드 방향키 탐색
- UTF-8 TXT 저장과 작품별 원문·라이선스·수집 내역

독서 배경은 항상 `#000000`입니다. 기본 본문은 `rgb(240,240,240)`이며 밝기를 낮출 수 있습니다. 기록은 이 브라우저의 localStorage에 저장되므로 브라우저·기기 간 동기화되지 않습니다. 네트워크가 없을 때 앱 전체를 새로 여는 오프라인 기능은 제공하지 않습니다.

## 콘텐츠와 권리

원작의 한국·미국 보호기간과 Standard Ebooks 에디션 기여분의 CC0 1.0 조건을 확인했습니다. 전 세계 모든 국가에서 보호기간이 끝났다고 주장하지 않습니다. 상세한 원작·판본·출처·고정 커밋·SHA-256·제외 범위는 `dist/data/sources.json`, `research/RIGHTS.md`에 있습니다.

삽화·이미지·폰트를 가져오지 않았습니다. 타이포그래피 표지는 앱을 위해 직접 만든 CSS입니다. 원작에 포함된 다른 언어 구절도 번역하지 않았습니다. Jane Eyre 에디션의 추가 번역 각주 52개는 제외했고 원작의 외국어 구절과 1848년 작가 주는 보존했습니다. 따라서 삽화와 편집상 추가물을 포함하는 원본 전자책 전체의 시각적 복제본은 아닙니다.

## 로컬 실행·검증

```text
python -m http.server 8876 --bind 127.0.0.1 --directory dist
python scripts/validate.py
node --check dist/app.js
```

별도 설치·빌드 단계 없이 `dist/`를 정적 배포합니다. `.openai/hosting.json`의 기존 Site ID를 유지해야 합니다. Sites 비공개 검토용 배포이며 사용자의 공개 승인을 받기 전 공개 GitHub 저장소·공개 앱 목록에 등록하지 않습니다.

## 인터페이스 언어

한국어는 루트(`/`), 영어·스페인어·중국어·일본어·독일어는 각각 `/en/`, `/es/`, `/zh/`, `/ja/`, `/de/`에서 제공합니다. 서재의 언어 선택과 읽기 화면의 언어 버튼으로 전환할 수 있습니다. 전환할 때 열어 둔 책의 해시와 이 브라우저에 저장한 읽기 위치·설정을 유지합니다. 작품 본문·원래 책 제목·작가명·TXT 다운로드는 영어 원작 그대로입니다.

정적 페이지는 `scripts/index.template.html`과 `scripts/localize.py`에서 재생성합니다. `python scripts/localize.py`는 6개 HTML과 UI 전용 `dist/locales.js`만 생성하며 `dist/data/`를 수정하지 않습니다. `scripts/validate.py`는 27개 원문 패키지 해시와 6개 언어 경로·UI 키·언어 선택·로컬 에셋을 검사합니다.

## Public GitHub Pages release

Launch: https://nanalab.kr/nocturne-library/

Korean is at the root. English, Spanish, Chinese, Japanese and German use `/en/`, `/es/`, `/zh/`, `/ja/`, `/de/`.
GitHub Pages serves `main` → `/docs` using the branch build. No project CNAME is used.

Build: `node scripts/build-public.mjs`. The `dist/` snapshot and its original generators/tests are preserved as the application source. The public build adds metadata, six-locale sitemaps, original JPEG cards, More Apps styling and the existing NaNa publisher integrations. It does not upload selected user files.

Publisher integrations: AdSense, Google Tag Manager, Google Analytics and Cloudflare Web Analytics, with the same publisher settings as the NaNa Lab homepage. These scripts can make network requests independently of local file processing.

Original JPEG cards are rendered from original text and geometry using an installed system font; no font files are redistributed. Existing source references and third-party notices remain applicable.
