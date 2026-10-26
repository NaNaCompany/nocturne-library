"""Build six UI routes without touching original book exports."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
LANGS = ['ko', 'en', 'es', 'zh', 'ja', 'de']
STATIC = r'''
밤의 서재¦The night library¦La biblioteca nocturna¦夜间书房¦夜の書斎¦Die Nachtbibliothek
검은 화면, 흰 글자. 저작권이 만료된 소설의 원문을 조용히 읽는 밤의 서재.¦A black screen, white words. Read original classic novels in a quiet night library.¦Pantalla negra, letras blancas. Lee novelas clásicas en su idioma original.¦黑色屏幕，白色文字。在安静的夜间书房阅读经典小说原文。¦黒い画面、白い文字。静かな夜の書斎で古典小説の原文を読む。¦Schwarzer Bildschirm, weiße Schrift. Klassische Romane im Original lesen.
본문으로 이동¦Skip to content¦Saltar al contenido¦跳至正文¦本文へ移動¦Zum Inhalt springen
NOCTURNE 서재¦NOCTURNE library¦Biblioteca NOCTURNE¦NOCTURNE 书房¦NOCTURNE 書斎¦NOCTURNE Bibliothek
서재 메뉴¦Library navigation¦Navegación de la biblioteca¦书房导航¦書斎メニュー¦Bibliotheksnavigation
서재¦Library¦Biblioteca¦书房¦書斎¦Bibliothek
책갈피 ¦Bookmarks ¦Marcadores ¦书签 ¦しおり ¦Lesezeichen
밤은 깊게,<br>이야기는 <em>더 깊게.</em>¦The night deepens.<br>The story goes <em>deeper.</em>¦La noche avanza.<br>La historia llega <em>más hondo.</em>¦夜色渐深，<br>故事<em>更深。</em>¦夜は深く、<br>物語は<em>さらに深く。</em>¦Die Nacht wird tief.<br>Die Geschichte <em>noch tiefer.</em>
화면의 빛은 낮추고, 문장의 여운은 길게.<br>번역하지 않은 고전의 원문을 만나는 시간.¦Dim the screen. Let the words linger.<br>Time for classics in their original language.¦Baja la luz. Deja que las palabras perduren.<br>Un momento para los clásicos en su idioma original.¦调暗屏幕，让文字余韵悠长。<br>此刻，遇见未经翻译的经典原文。¦画面の光を抑え、言葉の余韻を長く。<br>翻訳されていない古典の原文に出会う時間。¦Weniger Licht. Mehr Nachklang.<br>Zeit für Klassiker in ihrer Originalsprache.
서재를 열고 있어요¦Opening the library¦Abriendo la biblioteca¦正在打开书房¦書斎を開いています¦Bibliothek wird geöffnet
읽던 이야기¦Continue your story¦Continúa tu historia¦继续上次的故事¦読みかけの物語¦Geschichte fortsetzen
오늘 밤의 책¦Tonight’s book¦El libro de esta noche¦今夜之书¦今夜の一冊¦Das Buch für heute Nacht
책을 불러오는 중입니다.¦Loading books.¦Cargando libros.¦正在加载图书。¦本を読み込んでいます。¦Bücher werden geladen.
당신의 밤에 놓을 책¦Books for your night¦Libros para tu noche¦陪伴夜晚的书¦あなたの夜に置く本¦Bücher für deine Nacht
제목이나 작가로 찾기¦Search by title or author¦Buscar por título o autor¦按书名或作者搜索¦書名や著者で検索¦Nach Titel oder Autor suchen
장르 필터¦Genre filters¦Filtros de género¦类型筛选¦ジャンル絞り込み¦Genrefilter
고전·드라마¦Classics · Drama¦Clásicos · Drama¦经典·剧情¦古典・ドラマ¦Klassik · Drama
고딕·미스터리¦Gothic · Mystery¦Gótico · Misterio¦哥特·推理¦ゴシック・ミステリー¦Gotik · Krimi
모험·판타지¦Adventure · Fantasy¦Aventura · Fantasía¦冒险·奇幻¦冒険・ファンタジー¦Abenteuer · Fantasy
전체¦All¦Todos¦全部¦すべて¦Alle
일치하는 책이 없어요. 다른 제목이나 작가를 찾아보세요.¦No books found. Try another title or author.¦No se encontraron libros. Prueba otro título o autor.¦未找到匹配图书。请尝试其他书名或作者。¦一致する本がありません。別の書名や著者で検索してください。¦Keine Bücher gefunden. Versuche einen anderen Titel oder Autor.
한 문장 더, 그리고 좋은 밤.¦One more line, then good night.¦Una frase más y buenas noches.¦再读一句，然后晚安。¦あと一文、そしておやすみなさい。¦Noch ein Satz, dann gute Nacht.
원작 그대로 · 기록은 이 기기에¦Original texts · Reading saved on this device¦Textos originales · Progreso en este dispositivo¦保留原文 · 记录存于此设备¦原文のまま・記録はこの端末に¦Originaltexte · Lesestand auf diesem Gerät
원문·저작권·사용 내역 ↗¦Texts, rights & credits ↗¦Textos, derechos y créditos ↗¦原文、版权与使用说明 ↗¦原文・著作権・利用内容 ↗¦Texte, Rechte & Nachweise ↗
More Apps ↗¦More Apps ↗¦Más aplicaciones ↗¦更多应用 ↗¦ほかのアプリ ↗¦Weitere Apps ↗
전자책 뷰어¦Ebook reader¦Lector de libros¦电子书阅读器¦電子書籍リーダー¦E-Book-Leser
서재로 돌아가기¦Back to library¦Volver a la biblioteca¦返回书房¦書斎に戻る¦Zur Bibliothek
목차 열기¦Open contents¦Abrir índice¦打开目录¦目次を開く¦Inhaltsverzeichnis öffnen
현재 위치 책갈피 저장¦Bookmark this position¦Marcar esta posición¦为当前位置添加书签¦現在位置にしおりを追加¦Diese Stelle merken
읽기 설정 닫기¦Close reading settings¦Cerrar ajustes de lectura¦关闭阅读设置¦読書設定を閉じる¦Leseeinstellungen schließen
읽기 설정¦Reading settings¦Ajustes de lectura¦阅读设置¦読書設定¦Leseeinstellungen
집중 모드 시작¦Enter focus mode¦Activar modo concentración¦进入专注模式¦集中モードを開始¦Fokusmodus starten
집중 모드 끝내기¦Exit focus mode¦Salir del modo concentración¦退出专注模式¦集中モードを終了¦Fokusmodus beenden
장 이동¦Chapter navigation¦Navegación por capítulos¦章节导航¦章の移動¦Kapitelnavigation
← 이전¦← Previous¦← Anterior¦← 上一节¦← 前へ¦← Zurück
다음 →¦Next →¦Siguiente →¦下一节 →¦次へ →¦Weiter →
마지막 문장까지 함께한 밤.¦A night shared to the very last line.¦Una noche compartida hasta la última línea.¦与你共读，直到最后一句。¦最後の一文まで共に過ごした夜。¦Eine gemeinsame Nacht bis zum letzten Satz.
다른 이야기 만나기 ↗¦Find another story ↗¦Descubre otra historia ↗¦邂逅下一个故事 ↗¦別の物語に出会う ↗¦Eine andere Geschichte finden ↗
이 책의 원문·출처¦Original text & sources¦Texto original y fuentes¦本书原文与来源¦この本の原文・出典¦Originaltext & Quellen
밤에 맞추는 글자¦Words made for your night¦Letras a tu medida¦适合夜晚的文字¦夜に合わせる文字¦Schrift für deine Nacht
글꼴¦Typeface¦Tipografía¦字体¦書体¦Schriftart
문학의 결¦A literary touch¦Toque literario¦文学质感¦文学の趣¦Literarischer Charakter
또렷한 문장¦Crisp and clear¦Letras claras¦清晰易读¦くっきりした文字¦Klar und deutlich
글자 크기 ¦Font size ¦Tamaño de letra ¦字号 ¦文字サイズ ¦Schriftgröße
행간 ¦Line spacing ¦Interlineado ¦行距 ¦行間 ¦Zeilenabstand
문장 폭 ¦Text width ¦Ancho del texto ¦文本宽度 ¦本文の幅 ¦Textbreite
글자 밝기 ¦Text brightness ¦Brillo del texto ¦文字亮度 ¦文字の明るさ ¦Schrifthelligkeit
배경은 언제나 검정. 설정과 읽던 위치는 이 브라우저에 저장돼요.¦The background stays black. Settings and reading position are saved in this browser.¦El fondo siempre es negro. Los ajustes y la posición se guardan en este navegador.¦背景始终为黑色。设置与阅读位置保存在此浏览器中。¦背景はいつも黒。設定と読書位置はこのブラウザに保存されます。¦Der Hintergrund bleibt schwarz. Einstellungen und Lesestand werden in diesem Browser gespeichert.
기본 설정으로¦Reset settings¦Restablecer ajustes¦恢复默认设置¦初期設定に戻す¦Einstellungen zurücksetzen
목차 닫기¦Close contents¦Cerrar índice¦关闭目录¦目次を閉じる¦Inhaltsverzeichnis schließen
목차¦Contents¦Índice¦目录¦目次¦Inhaltsverzeichnis
나의 책갈피¦My bookmarks¦Mis marcadores¦我的书签¦自分のしおり¦Meine Lesezeichen
책갈피 닫기¦Close bookmarks¦Cerrar marcadores¦关闭书签¦しおりを閉じる¦Lesezeichen schließen
원문과 출처¦Originals & sources¦Originales y fuentes¦原文与来源¦原文と出典¦Originale & Quellen
출처 닫기¦Close sources¦Cerrar fuentes¦关闭来源¦出典を閉じる¦Quellen schließen
번역본을 수록하지 않았습니다. 원작의 문장을 읽기 화면에 맞춰 나누었으며, 원작 안의 다른 언어 구절은 그대로 보존합니다.¦No translations are included. Original texts are divided for reading on screen; passages in other languages remain unchanged.¦No se incluyen traducciones. Los textos originales se dividen para la lectura en pantalla; los pasajes en otros idiomas se conservan.¦本应用不收录译本。原文按阅读界面分段，作品中其他语言的文字保持不变。¦翻訳版は収録していません。原文を画面で読みやすく区切り、原作中の他言語の文章もそのまま保存しています。¦Es sind keine Übersetzungen enthalten. Originaltexte werden für den Bildschirm gegliedert; anderssprachige Passagen bleiben unverändert.
화면·소프트웨어¦Interface & software¦Interfaz y software¦界面与软件¦画面・ソフトウェア¦Oberfläche & Software
인터페이스와 타이포그래피 표지는 이 앱을 위해 직접 제작했습니다. 외부 이미지·웹폰트·JavaScript 라이브러리를 사용하지 않습니다. 독서 기록은 서버로 전송하지 않습니다.¦The interface and typographic covers were created for this app. No external images, web fonts or JavaScript libraries are used. Reading records are not sent to a server.¦La interfaz y las portadas tipográficas se crearon para esta aplicación. No se usan imágenes, fuentes web ni bibliotecas JavaScript externas. Los registros de lectura no se envían a un servidor.¦界面和文字封面为本应用原创。不使用外部图片、网络字体或 JavaScript 库。阅读记录不会发送至服务器。¦インターフェースと文字による表紙は本アプリ用に制作しました。外部画像・ウェブフォント・JavaScript ライブラリは使用せず、読書記録をサーバーに送信しません。¦Oberfläche und typografische Cover wurden für diese App erstellt. Externe Bilder, Webfonts und JavaScript-Bibliotheken werden nicht verwendet. Lesedaten werden nicht an einen Server gesendet.
원작은 한국·미국의 보호기간을 확인했습니다. 수집 에디션의 편집 기여분은 CC0 1.0입니다. 작품별 원문·권리 근거와 변환 내역은 아래 자료에서 확인할 수 있습니다.¦Copyright terms for the originals were checked for Korea and the United States. Editorial contributions in these editions are CC0 1.0. The records below document each text, its rights and its conversion. This is not a claim of worldwide public-domain status.¦Se comprobaron los plazos de protección en Corea y Estados Unidos. Las aportaciones editoriales de estas ediciones son CC0 1.0. Los registros siguientes documentan los textos, derechos y conversiones. No se afirma que sean de dominio público en todo el mundo.¦已核查原作在韩国与美国的保护期限。所收录版本的编辑贡献采用 CC0 1.0。各作品原文、权利依据及转换记录见下方资料。这不代表作品在全球均属公有领域。¦原作の保護期間は韓国と米国について確認しています。収録版の編集上の貢献は CC0 1.0 です。作品ごとの原文・権利根拠・変換記録は下記資料をご覧ください。世界中での保護期間終了を主張するものではありません。¦Die Schutzfristen der Originale wurden für Korea und die USA geprüft. Redaktionelle Beiträge dieser Ausgaben stehen unter CC0 1.0. Die folgenden Nachweise dokumentieren Texte, Rechte und Umwandlung. Eine weltweite Gemeinfreiheit wird nicht behauptet.
전체 출처·권리 자료 ↗¦Complete sources & rights records ↗¦Fuentes y derechos completos ↗¦完整来源与权利资料 ↗¦すべての出典・権利資料 ↗¦Vollständige Quellen- und Rechtenachweise ↗
A QUIETER PLACE TO READ¦A QUIETER PLACE TO READ¦UN LUGAR TRANQUILO PARA LEER¦静心阅读之处¦静かに読める場所¦EIN RUHIGER ORT ZUM LESEN
AFTER HOURS, BETWEEN PAGES.¦AFTER HOURS, BETWEEN PAGES.¦AL CAER LA NOCHE, ENTRE PÁGINAS.¦夜深时分，书页之间。¦夜更け、ページのあいだに。¦ZU SPÄTER STUNDE, ZWISCHEN SEITEN.
BLACK SCREEN.<br>WHITE WORDS.<br>JUST YOU & THE STORY.¦BLACK SCREEN.<br>WHITE WORDS.<br>JUST YOU & THE STORY.¦PANTALLA NEGRA.<br>LETRAS BLANCAS.<br>TÚ Y LA HISTORIA.¦黑色屏幕。<br>白色文字。<br>只有你与故事。¦黒い画面。<br>白い文字。<br>あなたと物語だけ。¦SCHWARZER BILDSCHIRM.<br>WEISSE SCHRIFT.<br>DU UND DIE GESCHICHTE.
RIGHT WHERE YOU LEFT OFF¦RIGHT WHERE YOU LEFT OFF¦JUSTO DONDE LO DEJASTE¦从上次停下的地方¦前回の続きから¦GENAU DORT, WO DU WARST
THE ORIGINALS COLLECTION¦THE ORIGINALS COLLECTION¦LA COLECCIÓN ORIGINAL¦原作典藏¦原作コレクション¦DIE ORIGINALSAMMLUNG
MAKE YOURSELF COMFORTABLE¦MAKE YOURSELF COMFORTABLE¦PONTE A GUSTO¦让阅读更舒适¦心地よい読書のために¦MACH ES DIR BEQUEM
FIND YOUR CHAPTER¦FIND YOUR CHAPTER¦ENCUENTRA TU CAPÍTULO¦找到你的章节¦読みたい章を探す¦FINDE DEIN KAPITEL
A LINE TO RETURN TO¦A LINE TO RETURN TO¦UNA LÍNEA A LA QUE VOLVER¦值得重读的一句¦また読みたい一文¦EIN SATZ ZUM WIEDERKEHREN
WORDS THAT BELONG TO EVERYONE¦WORDS THAT BELONG TO EVERYONE¦PALABRAS PARA COMPARTIR¦文字的来处¦言葉の出典をたどる¦WOHER DIE WORTE KOMMEN
Serif <span>¦Serif <span>¦Con serifa <span>¦衬线 <span>¦セリフ <span>¦Serifen <span>
Sans <span>¦Sans <span>¦Sin serifa <span>¦无衬线 <span>¦サンセリフ <span>¦Serifenlos <span>
'''
DYNAMIC = r'''
storageError¦이 브라우저에서는 독서 기록을 저장할 수 없어요.¦This browser cannot save reading records.¦Este navegador no puede guardar el progreso.¦此浏览器无法保存阅读记录。¦このブラウザでは読書記録を保存できません。¦Dieser Browser kann keine Lesedaten speichern.
hour¦{n}시간¦{n} hr¦{n} h¦{n}小时¦{n}時間¦{n} Std.
minute¦{n}분¦{n} min¦{n} min¦{n}分钟¦{n}分¦{n} Min.
books¦{n}권¦{n} books¦{n} libros¦{n}本¦{n}冊¦{n} Bücher
readLabel¦{title} 원문 읽기¦Read {title} in the original¦Leer {title} en su idioma original¦阅读 {title} 原文¦{title} の原文を読む¦{title} im Original lesen
readPercent¦{n}% 읽음¦{n}% read¦{n}% leído¦已读 {n}%¦{n}% 読了¦{n}% gelesen
classic¦고전¦Classic¦Clásico¦经典¦古典¦Klassik
literary¦문학¦Literature¦Literatura¦文学¦文学¦Literatur
romance¦로맨스¦Romance¦Romance¦爱情¦ロマンス¦Liebesroman
gothic¦고딕¦Gothic¦Gótico¦哥特¦ゴシック¦Gotik
fantasy¦판타지¦Fantasy¦Fantasía¦奇幻¦ファンタジー¦Fantasy
adventure¦모험¦Adventure¦Aventura¦冒险¦冒険¦Abenteuer
horror¦호러¦Horror¦Terror¦恐怖¦ホラー¦Horror
mystery¦미스터리¦Mystery¦Misterio¦推理¦ミステリー¦Krimi
science-fiction¦SF¦Science fiction¦Ciencia ficción¦科幻¦SF¦Science-Fiction
about¦약 {time}¦About {time}¦Unas {time}¦约 {time}¦約 {time}¦Etwa {time}
continue¦계속 읽기¦Continue reading¦Seguir leyendo¦继续阅读¦続きを読む¦Weiterlesen
featured¦오늘 밤의 첫 장¦TONIGHT’S OPENING CHAPTER¦EL PRIMER CAPÍTULO DE ESTA NOCHE¦今夜的开篇¦今夜の最初の一章¦DAS ERSTE KAPITEL DER NACHT
description¦재즈 시대의 부와 욕망을 따라 읽는 미국 고전.¦An American classic tracing wealth and desire in the Jazz Age.¦Un clásico estadounidense sobre la riqueza y el deseo en la era del jazz.¦一部追寻爵士时代财富与欲望的美国经典。¦ジャズ時代の富と欲望をたどるアメリカ文学の古典。¦Ein amerikanischer Klassiker über Reichtum und Sehnsucht im Jazz-Zeitalter.
englishOriginal¦영어 원작¦ENGLISH ORIGINAL¦ORIGINAL EN INGLÉS¦英语原作¦英語原作¦ENGLISCHES ORIGINAL
chapters¦{n}개 장 · {time}¦{n} chapters · {time}¦{n} capítulos · {time}¦{n}章 · {time}¦{n}章 · {time}¦{n} Kapitel · {time}
readOriginal¦원문 읽기¦Read original¦Leer original¦阅读原文¦原文を読む¦Original lesen
loadBookError¦책을 열지 못했어요. 연결 상태를 확인하고 다시 눌러 주세요.¦Could not open this book. Check your connection and try again.¦No se pudo abrir el libro. Comprueba la conexión e inténtalo de nuevo.¦无法打开此书。请检查网络连接后重试。¦本を開けませんでした。接続を確認して、もう一度お試しください。¦Das Buch konnte nicht geöffnet werden. Prüfe die Verbindung und versuche es erneut.
originalText¦원문¦ORIGINAL TEXT¦TEXTO ORIGINAL¦原文¦原文¦ORIGINALTEXT
progress¦전체 읽기 진행률 약 {n}퍼센트¦Overall reading progress: about {n} percent¦Progreso total: aproximadamente {n} por ciento¦整体阅读进度约为百分之{n}¦全体の読書進捗は約 {n} パーセント¦Lesefortschritt insgesamt: etwa {n} Prozent
remaining¦약 {time} 남음¦About {time} left¦Quedan unas {time}¦约剩 {time}¦残り約 {time}¦Noch etwa {time}
title¦NOCTURNE · 밤의 서재¦NOCTURNE · The night library¦NOCTURNE · Biblioteca nocturna¦NOCTURNE · 夜间书房¦NOCTURNE · 夜の書斎¦NOCTURNE · Die Nachtbibliothek
focusOff¦집중 모드 끝내기¦Exit focus mode¦Salir del modo concentración¦退出专注模式¦集中モードを終了¦Fokusmodus beenden
focusOn¦집중 모드 시작¦Enter focus mode¦Activar modo concentración¦进入专注模式¦集中モードを開始¦Fokusmodus starten
unbookmark¦현재 위치 책갈피 해제¦Remove bookmark at this position¦Quitar marcador de esta posición¦移除当前位置的书签¦現在位置のしおりを解除¦Lesezeichen an dieser Stelle entfernen
bookmark¦현재 위치 책갈피 저장¦Bookmark this position¦Marcar esta posición¦为当前位置添加书签¦現在位置にしおりを追加¦Diese Stelle merken
bookmarkRemoved¦책갈피를 해제했어요.¦Bookmark removed.¦Marcador eliminado.¦书签已移除。¦しおりを解除しました。¦Lesezeichen entfernt.
bookmarkAdded¦이 문장에 책갈피를 남겼어요.¦This passage is bookmarked.¦Se ha marcado este pasaje.¦已为此段添加书签。¦この文章にしおりを付けました。¦Diese Textstelle wurde gemerkt.
section¦{n}번째 섹션¦Section {n}¦Sección {n}¦第{n}节¦セクション {n}¦Abschnitt {n}
removeBookmark¦{title} 책갈피 삭제¦Delete bookmark for {title}¦Eliminar marcador de {title}¦删除 {title} 的书签¦{title} のしおりを削除¦Lesezeichen für {title} löschen
emptyBookmarks¦다시 만나고 싶은 문장을 남겨 보세요.<br>읽기 화면 위쪽의 책갈피 버튼으로 저장할 수 있어요.¦Keep a passage you want to return to.<br>Use the bookmark button at the top of the reader.¦Guarda un pasaje al que quieras volver.<br>Usa el botón de marcador en la parte superior del lector.¦保存想再读一次的文字。<br>点击阅读器顶部的书签按钮即可保存。¦また読みたい文章を残しましょう。<br>読書画面上部のしおりボタンで保存できます。¦Merke dir eine Textstelle zum Wiederlesen.<br>Nutze die Lesezeichentaste oben im Lesefenster.
originalLanguage¦원작 언어 {language}¦Original language: {language}¦Idioma original: {language}¦原作语言：{language}¦原作の言語：{language}¦Originalsprache: {language}
sourceInfo¦저자 사망 {year}년. 원작 보호기간과 에디션의 CC0 1.0 이용 조건을 확인했습니다. XHTML 본문을 UTF-8 TXT와 문단 데이터로 변환했으며 문장을 번역하거나 재작성하지 않았습니다.¦The author died in {year}. Copyright terms and the edition’s CC0 1.0 terms were checked. XHTML text was converted to UTF-8 TXT and paragraph data without translation or rewriting.¦El autor falleció en {year}. Se comprobaron la protección del original y las condiciones CC0 1.0 de la edición. El XHTML se convirtió a TXT UTF-8 y datos por párrafos sin traducir ni reescribir.¦作者于{year}年去世。已核查原作保护期限与该版本的 CC0 1.0 使用条件。XHTML 正文已转换为 UTF-8 TXT 及段落数据，未经翻译或改写。¦著者は {year} 年没。原作の保護期間と版の CC0 1.0 条件を確認しました。XHTML 本文を UTF-8 TXT と段落データに変換し、翻訳や書き換えはしていません。¦Der Autor starb {year}. Schutzfrist und CC0-1.0-Bedingungen der Ausgabe wurden geprüft. XHTML wurde ohne Übersetzung oder Umschreiben in UTF-8-TXT und Absatzdaten umgewandelt.
rightsInfo¦한국의 보수적 사후 70년 계산은 {end}년 말 종료. Standard Ebooks 판본 기여분은 CC0 1.0이며 해당 판본은 원문을 미국 퍼블릭 도메인으로 명시합니다. 원작 안의 다른 언어 구절은 보존했습니다. 전 세계 보호기간 종료를 주장하지 않습니다.¦Under a conservative life-plus-70 calculation for Korea, the term ended at the close of {end}. Standard Ebooks edition contributions are CC0 1.0; the edition identifies the source text as U.S. public domain. Passages in other languages are preserved. No worldwide expiry is claimed.¦Según el cálculo conservador de vida más 70 años en Corea, el plazo terminó a finales de {end}. Las aportaciones de Standard Ebooks son CC0 1.0; la edición identifica el original como dominio público en EE. UU. Se conservan los pasajes en otros idiomas. No se afirma una expiración mundial.¦按韩国保守的作者终身加70年计算，保护期于{end}年末结束。Standard Ebooks 版本贡献采用 CC0 1.0；该版本将原文列为美国公有领域作品。其他语言段落保持不变。不主张全球保护期均已结束。¦韓国で保守的に没後70年を適用すると、保護期間は {end} 年末に終了。Standard Ebooks の版への貢献は CC0 1.0 で、同版は原文を米国のパブリックドメインと明記しています。他言語の文章も保存しています。世界中での保護期間終了を主張しません。¦Nach einer vorsichtigen Berechnung mit 70 Jahren nach dem Tod endete die Frist in Korea Ende {end}. Beiträge zur Standard-Ebooks-Ausgabe stehen unter CC0 1.0; sie bezeichnet den Ausgangstext als in den USA gemeinfrei. Anderssprachige Passagen bleiben erhalten. Eine weltweite Gemeinfreiheit wird nicht behauptet.
edition¦원문 에디션 ↗¦Original edition ↗¦Edición original ↗¦原文版本 ↗¦原文の版 ↗¦Originalausgabe ↗
pinnedSource¦고정된 원문 소스 ↗¦Pinned source revision ↗¦Revisión de origen fijada ↗¦固定版本原文源码 ↗¦固定版の原文ソース ↗¦Fixierter Quellstand ↗
download¦TXT 저장 ↓¦Download TXT ↓¦Descargar TXT ↓¦下载 TXT ↓¦TXT を保存 ↓¦TXT herunterladen ↓
shelfCount¦영어 원작 {n}권 · EN¦{n} ORIGINAL BOOKS · EN¦{n} LIBROS ORIGINALES · EN¦{n}部英语原作 · EN¦英語原作 {n}冊 · EN¦{n} ORIGINALBÜCHER · EN
loadLibraryError¦서재를 불러오지 못했어요.¦Could not load the library.¦No se pudo cargar la biblioteca.¦无法加载书房。¦書斎を読み込めませんでした。¦Die Bibliothek konnte nicht geladen werden.
retry¦다시 불러오기 ↗¦Try again ↗¦Reintentar ↗¦重新加载 ↗¦再読み込み ↗¦Erneut versuchen ↗
checkConnection¦연결 상태를 확인해 주세요¦Please check your connection¦Comprueba tu conexión¦请检查网络连接¦接続状態を確認してください¦Bitte prüfe deine Verbindung
language¦언어¦Language¦Idioma¦语言¦言語¦Sprache
closeLanguage¦언어 선택 닫기¦Close language selection¦Cerrar selección de idioma¦关闭语言选择¦言語選択を閉じる¦Sprachauswahl schließen
'''

def parse_rows(raw, dynamic=False):
    result = {}
    for row in raw.strip('\n').splitlines():
        cells = row.split('¦')
        assert len(cells) == (7 if dynamic else 6), (cells[0], len(cells))
        result[cells[0]] = cells[1:] if dynamic else [cells[0], *cells[1:]]
    return result

def build():
    static = parse_rows(STATIC)
    dynamic = parse_rows(DYNAMIC, True)
    template = (ROOT/'scripts/index.template.html').read_text(encoding='utf-8')
    labels = {'ko':'한국어','en':'English','es':'Español','zh':'中文','ja':'日本語','de':'Deutsch'}
    for i, lang in enumerate(LANGS):
        # One pass avoids translating fragments of an already translated phrase.
        pattern = '|'.join(re.escape(k) for k in sorted(static, key=len, reverse=True))
        html = re.sub(pattern, lambda m:static[m[0]][i], template)
        html = html.replace('<html lang="ko">',f'<html lang="{lang}">')
        html = html.replace('<head>', '<head>' + ('' if lang=='ko' else '\n  <base href="../">'))
        html = html.replace('<script src="app.js" defer></script>', '<script src="locales.js" defer></script>\n  <script src="app.js" defer></script>')
        route = './' if lang=='ko' else lang+'/'
        html = html.replace('href="#library-main"',f'href="{route}#library-main"').replace('href="#"',f'href="{route}#"')
        options = ''.join(f'<option value="{code}" lang="{code}"'+(' selected' if code==lang else '')+f'>{label}</option>' for code,label in labels.items())
        switch = f'<label class="language-control"><span>{dynamic["language"][i]}</span><select id="language-select" aria-label="{dynamic["language"][i]}">{options}</select></label>'
        html = html.replace('<span class="header-note">',switch+'<span class="header-note">')
        # Reader-level access keeps language selection available while reading.
        html = html.replace('<div class="reader-actions">','<div class="reader-actions"><button id="reader-language" class="icon-button language-button" aria-label="'+dynamic['language'][i]+'">文</button>')
        dialog = f'<dialog id="language-dialog" class="panel" aria-labelledby="language-heading"><header class="panel-header"><h2 id="language-heading">{dynamic["language"][i]}</h2><button class="close-dialog icon-button" aria-label="{dynamic["closeLanguage"][i]}">×</button></header><label class="language-dialog-label" for="reader-language-select">{dynamic["language"][i]}</label><select id="reader-language-select">{options}</select></dialog>'
        html = html.replace('<div id="toast"',dialog+'<div id="toast"')
        html = html.replace('<nav class="chapter-navigation"','<nav lang="'+lang+'" class="chapter-navigation"')
        html = html.replace('<p id="book-finished"','<p lang="'+lang+'" id="book-finished"')
        html = html.replace('<button id="reader-sources"','<button lang="'+lang+'" id="reader-sources"')
        path = DIST/'index.html' if lang=='ko' else DIST/lang/'index.html'
        path.parent.mkdir(exist_ok=True)
        path.write_text(html,encoding='utf-8')
    catalog = {lang:{key:values[i] for key,values in dynamic.items()} for i,lang in enumerate(LANGS)}
    (DIST/'locales.js').write_text("'use strict';\nwindow.NOCTURNE_I18N = "+json.dumps(catalog,ensure_ascii=False,indent=2)+';\n',encoding='utf-8')
    print(json.dumps({'routes':len(LANGS),'staticPhrases':len(static),'runtimeKeys':len(dynamic)}))

if __name__=='__main__':build()
