# Test Cases

## Goals

Validate the pipeline on different source types and record where fallback or manual patch is needed.

## Source Types

1. Normal static HTML article
2. Long technical blog post
3. WeChat public article
4. Extraction failure sample

## What to check

### crawl
- raw json created
- title extracted
- content non-empty or failure recorded
- notes include adapter info

### normalize
- markdown file created
- source url preserved
- topic preserved

### preprocess
- processed note created for each source
- bundle generated
- repeated points merged reasonably

### writer
- article generated
- structure is readable
- review reduces empty wording
- prepublish check highlights risks when needed

## Failure Handling

- If crawl fails, ensure a failed raw json exists
- If extraction quality is poor, use manual patch json and rerun
