# wechat-codex-autowrite

A practical pipeline for **auto-writing WeChat-style articles with Codex CLI**.

This project turns article generation into a layered workflow instead of a single prompt:

1. **crawl** URLs into raw source JSON
2. **extract/adapter** source-specific title and body
3. **normalize** sources into markdown
4. **preprocess** sources into structured notes and a writing bundle
5. **write** the article with Codex
6. **review / format / prepublish-check** before human approval

## Status

Current release: **v0.1.0**

This is an MVP with a usable architecture:
- URL crawler skeleton
- adapter layer
- preprocessing layer
- writing + review layer
- fallback and manual patch strategy

## Why this project exists

Most “AI article writing” setups fail because they skip the upstream steps.
They throw messy, duplicated, overlong raw material directly into the model.

This repo uses a more stable pattern:

**URLs / notes -> raw sources -> normalized markdown -> processed notes -> bundle -> final article**

That makes the workflow easier to debug, extend, and automate with OpenClaw.

## Project structure

```text
wechat-codex-autowrite/
├─ crawl_urls.py
├─ adapters.py
├─ normalize_sources.py
├─ preprocess.py
├─ writer.py
├─ run_job.py
├─ run_full_flow.py
├─ run_pipeline_from_urls.py
├─ jobs/
├─ prompts/
├─ templates/
├─ samples/
├─ README.md
├─ CHANGELOG.md
├─ TEST_CASES.md
├─ ADAPTERS.md
├─ FALLBACKS.md
├─ MANUAL_PATCH.md
└─ LICENSE
```

## Core pipeline

### Option A: run from URL list

```bash
python3 run_pipeline_from_urls.py --job ./jobs/example_full_pipeline_from_urls.json
```

### Option B: run step by step

#### 1. Crawl URLs to raw JSON
```bash
python3 crawl_urls.py \
  --input ./jobs/example_url_list.txt \
  --raw-dir ./samples/output/raw \
  --topic "AI Agent article workflow"
```

#### 2. Normalize raw JSON into markdown
```bash
python3 normalize_sources.py \
  --input ./samples/output/raw \
  --output-dir ./samples/output/normalized
```

#### 3. Preprocess sources into bundle
```bash
python3 preprocess.py \
  --input ./samples/output/normalized \
  --processed-dir ./samples/output/processed \
  --bundle-output ./samples/output/bundle.md \
  --topic "AI Agent article workflow"
```

#### 4. Write the article
```bash
python3 writer.py \
  --topic "AI Agent article workflow" \
  --refs ./samples/output/bundle.md \
  --mode full \
  --output ./samples/output/article.md \
  --check-output ./samples/output/check.md
```

## Current adapters

### generic
- default extractor for normal HTML pages

### wechat
- specialized extractor for `mp.weixin.qq.com`
- prefers `og:title` and `#js_content`
- falls back to basic extraction when needed

## Fallback strategy

- crawl failure -> save failed raw JSON
- extractor failure -> fall back to generic/basic extraction
- poor content quality -> use manual patch JSON and rerun downstream steps

See also:
- `ADAPTERS.md`
- `FALLBACKS.md`
- `MANUAL_PATCH.md`

## Current limitations

- crawler is still lightweight
- dynamic pages may not extract well
- WeChat pages may still be unstable
- no fact-checking layer yet
- no direct publishing integration yet

## Suggested next steps

1. stronger content extraction
2. more adapters (Zhihu, SSPAI, Medium, etc.)
3. search-to-URL stage
4. fact-check/risk annotation layer
5. OpenClaw message-triggered entrypoint

## License

MIT
