# Nocturne English-original text collection

Verified: 2026-10-26. **12 complete textual works within the explicit extraction scope; zero translated books.**

The collection contains 1,149,507 words, 397 main numbered chapters, 450 exported reading sections and 19,476 source text blocks. Reading time is an estimate at 220 words/minute. Counts include headings, front matter and retained notes. Main-chapter counts do not include dedications, epigraphs, letters or notes. The export JSON files total 6,678,901 bytes; the UTF-8/LF TXT files total 6,444,152 bytes.

## Inventory

| Work | Author | First publication | Death year | Main chapters | Export sections | Words |
|---|---|---:|---:|---:|---:|---:|
| The Great Gatsby | F. Scott Fitzgerald | 1925 | 1940 | 9 | 11 | 48,455 |
| Pride and Prejudice | Jane Austen | 1813 | 1817 | 61 | 61 | 121,971 |
| Frankenstein | Mary Shelley | 1818 | 1851 | 24 | 37 | 77,890 |
| Alice’s Adventures in Wonderland | Lewis Carroll | 1865 | 1898 | 12 | 13 | 26,743 |
| The Picture of Dorian Gray | Oscar Wilde | 1890 | 1900 | 20 | 21 | 79,061 |
| Jane Eyre | Charlotte Brontë | 1847 | 1855 | 38 | 40 | 186,910 |
| Wuthering Heights | Emily Brontë | 1847 | 1848 | 34 | 34 | 116,443 |
| Moby Dick | Herman Melville | 1851 | 1891 | 135 | 162 | 213,476 |
| Dracula | Bram Stoker | 1897 | 1912 | 27 | 30 | 161,113 |
| The Hound of the Baskervilles | Arthur Conan Doyle | 1902 | 1930 | 15 | 16 | 59,301 |
| The Time Machine | H. G. Wells | 1895 | 1946 | 12 | 15 | 32,462 |
| The Strange Case of Dr. Jekyll and Mr. Hyde | Robert Louis Stevenson | 1886 | 1894 | 10 | 10 | 25,682 |

`publishedYear` means first publication, following each official Standard Ebooks colophon. In particular, *The Picture of Dorian Gray* first appeared in 1890; the later expanded book appeared in 1891. The supplied *Frankenstein* textual source uses Shelley's revised 1831 edition, while the novel's first publication was 1818. This is a text extraction of the specified Standard Ebooks revisions, not a diplomatic transcription of the original printed first editions.

## Files and integration

- `exports/catalog.json`: schemaVersion 1 and 12 catalog entries.
- `exports/books/{id}.json`: original title/author/language and ordered `chapters[]`; each chapter has `id`, `title`, `paragraphs[]` of plain original-text strings.
- `exports/txt/{id}.txt`: title, author, ordered section titles and paragraphs, separated by blank lines; UTF-8 without BOM, LF line endings.
- `exports/sources.json`: official URLs, pinned commits, edition rights statements, full contributor-role credits, original transcription/scan URLs, author-death evidence, source and output SHA256 hashes, complete spine classification, exclusions and per-block extraction audits.
- `exports/verification.json`: collection totals.
- `exports/package-sha256.json`: relative-path SHA256 manifest for the export package (the manifest does not hash itself).
- `collection-lock.json`: immutable revisions collected for this handoff.
- `sources/`: local sparse checkouts of the 12 public official Standard Ebooks repositories; only text, OPF and LICENSE.md were requested.
- `collect.py`, `export.py`, `verify.py`, `document.py`: reproducible collection, extraction, independent integrity checks and report generation.
- `verification-result.json`: independently verified result.

## Preservation and exclusions

Every included file follows the **exact OPF spine order**. XML markup and indentation, styling, backlink arrows, illustrations and modern image alt descriptions are removed. Paragraph wording, spelling, Unicode punctuation, original non-English passages, table text, explicit poem line breaks, dedications, epigraphs, prefaces, letters and retained source notes are preserved. Inline style information and poetry indentation from CSS are not reproduced. Tables are flattened row by row with tab-separated cells. Headings are separate section titles; a file with no body heading receives its source `head/title` as a navigation label. Endnote list numbers become generated `Endnote N` section titles, without rewriting note prose.

Publisher title/half-title pages, imprint, colophon, uncopyright, illustration list and illustration-only frontispiece are omitted from the novel TXT. Their originals remain in local sources and all omitted spine items are recorded. No covers, fonts or other visual assets are exported.

*Jane Eyre*: the author's original preface and **Note to the Third Edition**, signed Currer Bell and dated April 13, 1848, are retained. The edition-added set of **52 English translation notes for original French/German passages** and their numeric reference anchors are omitted. The original foreign-language passages remain unchanged. This is not a translated or bilingual edition.

*Moby Dick*: Etymology, Extracts, dedication, epilogue, all 22 source endnotes and their reference numbers are retained. The inline Queequeg signature cross drawing in chapter 18 is omitted as an image; its surrounding text survives. *Alice's Adventures in Wonderland*: 42 illustrations, including the frontispiece, are omitted. The original poems remain textual with their explicit line breaks. These are complete **text-scope** exports, not complete illustrated facsimiles.

*Frankenstein*: original 1831 introduction, 1818 preface, four letters, epigraph, dedication, 24 main chapters and the three source notes are retained. The Time Machine's source editor note is retained as part of the supplied historical textual edition rather than silently discarded because it is called a note.

No novel text was translated, paraphrased, summarized or rewritten by an AI model. Korean catalog sentences are newly written, one-sentence reading recommendations, separate from the novel text. Any Standard Ebooks corrections, typography and spelling already in its source are preserved; this process does not reconstruct print-original typography.

## Validation

Independent `verify.py` passed for all 12 books:

- 506 local source files match their pinned Git commit blobs, with expected Git line-ending normalization, and match the recorded source SHA256 hashes.
- All source checkouts are clean and all current HEAD revisions match `collection-lock.json`.
- All OPF spine files are classified as included or explicitly excluded; unclassified files: 0.
- Exhaustive independent traversal verifies every included non-whitespace body character in order against the exported headings/paragraphs after the documented exclusions.
- All 19,476 extracted text blocks have recorded character counts and SHA256 hashes.
- Export SHA256 matches and exact JSON-to-TXT reconstruction pass for every work.
- UTF-8/LF, unique book/chapter identifiers, string paragraph types, English OPF language and absence of translator-role editions pass.

The validation proves faithful extraction from the chosen current editions. It does not establish historical first-edition textual identity, visual fidelity or a worldwide jurisdiction-independent legal opinion. Rights evidence and scope are in RIGHTS.md.

## Reproduce

From this directory, run `collect.py` only when collecting missing sources. It does not fetch/update existing revisions. Run `export.py`, then `verify.py`, then `document.py` with Python 3.12+; only the standard library is needed. `collect.py` uses the explicitly configured RTK executable for Git and `rtk bypass` for exact machine-readable output. All source endpoints are ordinary public GitHub URLs. No accounts, tokens or credentials are required or stored.
