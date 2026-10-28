# NOCTURNE 문학 자료 권리·출처 기록

수집일: 2026-10-28. 이 폴더는 로컬 수집·검증 자료이며 앱 수정, Git 작업, 배포를 하지 않았다.

## 최종 수록 후보

| 작품 | 사용할 파일 | 원작과 전자전사의 권리 | 완전성 범위 |
|---|---|---|---|
| 공진회 | gongjinhoe.book.json / gongjinhoe.txt | 안국선 원작은 만료. 한국저작권위원회 공식 전자전사 제공 파일도 개별 페이지에서 자유이용 만료로 표시 | 제공 TXT 전체. 서문·독자에게 주는 글·기생·인력거꾼·시골 노인 이야기·말미 6절 |
| 금수회의록 | geumsuhoeuirok.book.json / geumsuhoeuirok.txt | 안국선 원작은 만료. 한국저작권위원회 공식 전자전사 제공 파일도 개별 페이지에서 자유이용 만료로 표시 | 제공 TXT 전체. 서언·8개 동물 연설·폐회 10절 |
| 홍길동전 (30장 경판본) | honggildong-30.book.json / honggildong-30.txt | 고전 경판본 원작은 만료. 위키문헌의 저작권이 발생하는 전사·편집 기여는 CC BY-SA 4.0 | 고정 판 전사 첫 문장부터 최종 종결까지. 초판 스캔 독립 대조는 하지 않음 |

## 안국선 원작

안국선은 1926년 7월 8일 사망했다. 금수회의록은 1908년, 공진회는 1915년에 발표됐다. 한국학중앙연구원 한국민족문화대백과사전의 [안국선 항목](https://encykorea.aks.ac.kr/Article/E0034542), [공진회 항목](https://encykorea.aks.ac.kr/Article/E0004522)에서 저자·사망·발표를 확인했다. 안성시 문화관광의 [문인 소개](https://www.anseong.go.kr/tourPortal/munhak/contents.do?mId=0800000000)도 1878–1926 및 발표 1908/1915를 확인한다. 사실 확인에만 사용했으며 백과사전 해설 본문을 수록하지 않았다.

금수회의록의 번안 저본 저자 사토 구라타로(佐藤蔵太郎, 필명 菊亭香水)의 사망년 1942년은 [일본 국립국회도서관 레퍼런스 협동 DB의 시립도서관 공식 사례](https://crd.ndl.go.jp/reference/entry/reference/show?id=1000276199&page=ref_view)에서 확인했다. 저본 원문을 별도로 수록하지 않는다.

## 안국선 전자전사: 위키문헌판과 분리

최종 JSON은 위키문헌의 현대정서판을 복제하지 않는다. 아래 한국저작권위원회 공유마당 직접 제공 TXT를 사용한다.

- [공진회 개별 제공·이용조건 페이지](https://gongu.copyright.or.kr/gongu/wrt/wrt/view.do?menuNo=200019&wrtSn=9000634)
- [공진회 TXT 파일](https://gongu.copyright.or.kr/gongu/wrt/cmmn/wrtFileDownload.do?wrtSn=9000634&fileSn=4)
- [금수회의록 개별 제공·이용조건 페이지](https://gongu.copyright.or.kr/gongu/wrt/wrt/view.do?menuNo=200019&wrtSn=9000635)
- [금수회의록 TXT 파일](https://gongu.copyright.or.kr/gongu/wrt/cmmn/wrtFileDownload.do?wrtSn=9000635&fileSn=4)
- [공유마당 만료저작물 이용 안내](https://gongu.copyright.or.kr/gongu/main/contents.do?menuNo=200091)

개별 페이지의 이용조건은 `img_license97.png`, `alt="자유이용 만료"`로 표시된다. 해당 안내는 저작재산권 보호기간이 끝난 자료를 별도 허락·승인 없이 자유롭게 이용할 수 있다고 설명한다. 원작 만료만으로 현대 출판물 전체가 자유이용이라는 추론을 하지 않았다. 이번에 내려받은 공식 전사 TXT 자체가 개별 만료 표시와 함께 제공되는 점을 확인했다. 별도 현대 역자·해설자 표시나 교과서 주석은 이 TXT에 없다. 전사자의 법적 지위를 임의로 창작하지 않는다.

원시 `*.gongu.original.bin`은 서버 응답 bytes 그대로다. UTF-8 BOM이 있는 TXT이며 확장자 `.bin`은 원시 보존을 뜻한다. 다운로드 팝업에서 제공된 원 파일명과 hash는 metadata.json에 기록했다. 파일에 revision ID가 없으므로 SHA-256으로 수집본을 고정한다. 당시 원시 제공·다운로드·만료 안내 HTML도 이 폴더에 보존한다.

제공 파일은 이미 현대표기로 전사되어 있다. 초판 원철자 재현본이나 새로 번역한 현대역으로 표시하지 않는다. 가공은 BOM 제거, 줄바꿈, 장·문단 구조화뿐이다. 오식처럼 보이는 부분도 임의 고치지 않았다. 출처 고지는 `안국선 원작 / 한국저작권위원회 공유마당 전자전사 제공본` 및 각 제공·이용조건 URL을 사용한다. 특정 현대 출판사의 편집·해설은 넣지 않았다.

공진회 실제 출간본은 3편이다. 검열로 삭제된 계획작 `탐정순사`, `외국인의 화`는 현존 제공본에 없고 이번에 만들어 보충하지 않았다. 이를 불완전 발췌로 오해하지 않도록 출간본 수록작과 당초 계획작을 구별한다. 초판 스캔을 페이지마다 육안 대조했다는 주장은 하지 않는다.

## 홍길동전 원작·전자전사

저자 표시는 `허균 (전칭)`이다. 위키문헌 해당 판본 머리말의 지은이란은 비어 있다. [한국학중앙연구원 홍길동전 항목](https://encykorea.aks.ac.kr/Article/E0063994)과 [허균 항목](https://encykorea.aks.ac.kr/Article/E0063030)은 작품 전통과 허균의 사망 1618년을 확인하는 자료다. 특정 30장 경판본의 초간연도는 확인하지 못하여 미상으로 유지한다. 이 판본을 1612년 초판이라고 표시하지 않는다. 고전 경판본 원작의 만료와 현대 전사의 이용허락을 별개로 기록한다.

- [원문 페이지](https://ko.wikisource.org/wiki/홍길동전_(30장_경판본))
- [고정 revision 460078](https://ko.wikisource.org/w/index.php?oldid=460078)
- [기여자 이력](https://ko.wikisource.org/w/index.php?title=홍길동전%20%2830장%20경판본%29&action=history)
- [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
- [위키미디어 이용약관](https://foundation.wikimedia.org/wiki/Policy:Terms_of_Use/ko)

고정 revision 원시 wikitext와 HTML을 보존했고, HTML footer의 CC BY-SA 4.0 링크를 확인했다. 기명 기여자 9명은 Sotiale, Caffelice~kowikisource, Theoteryi, Mineralsab, Thebot~kowikisource, Hojelei, Huzzlet the bot, Aspere, Asperebot이다. 익명 기여자 3명도 있으며 상세 이력은 위 history 링크로 연결한다. API 원시 응답 `honggildong-contributors.json`과 metadata의 사용자 링크를 함께 보존한다. 전사 이용 시 원저자 전칭·위키문헌 기여자·고정 출처·이력·라이선스·변경사항을 표시해야 한다. CC BY-SA가 허용하는 링크 방식의 기여자 표시는 접근 가능한 원문·이력 링크를 유지해야 한다.

상업 이용·복제·배포·개작은 CC BY-SA 4.0 조건 아래 허용된다. 전사를 개작하면 해당 전사에 동일 라이선스를 유지하고 추가적인 법적 제한이나 DRM을 붙이지 않는다. 별도 앱 코드 및 다른 독립 작품에 이 라이선스를 자동 확장하지 않는다. TXT는 고지를 자체 포함한다. 앱이 JSON만 사용하면 metadata/RIGHTS의 고지를 독자가 볼 수 있게 별도 표시해야 한다.

위키 머리말·판본 안내·폰트 안내·탐색·저작권 도구영역은 본문에서 제외했다. 옛한글과 본문의 표기는 보존했다. 현대어 번역·김유정 개작본·교과서 해설은 사용하지 않는다.

## 비교 자료와 검증 경계

`*.wikisource-comparison.*` 및 `geumsu-pages-*.json`은 권리·완전성 조사 중 수집한 비교 자료다. 공진회 위키 정서판은 외부 원출처 미해결로 최종 수록에서 제외했다. 금수회의록 위키 옛한글 전사는 56개 페이지를 확보했으나 본문 대부분의 pagequality가 1(미교정)이다. 별도 보존한 해당 파일을 공식 전사본과 섞거나 교정 완료라고 표시하지 않는다.

`validation.json`은 제공 TXT의 공백을 제외한 문자 보존, JSON 구조, 모든 장의 비어 있지 않은 본문, U+FFFD/PUA/위키 미처리 문법 부재, 본문량을 검증한다. `SHA256SUMS.json`은 원시 응답과 최종 산출물의 수집 상태 hash manifest다. 브라우저 앱 표시·배포·초판 스캔 전수대조는 범위 밖이다.
