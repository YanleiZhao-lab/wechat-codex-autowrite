#!/usr/bin/env python3
import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from adapters import extract_generic


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r'[^a-z0-9\u4e00-\u9fff]+', '-', text)
    return text.strip('-') or 'source'


def fetch_url(url: str, timeout: int = 20) -> str:
    req = Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123 Safari/537.36'
    })
    with urlopen(req, timeout=timeout) as resp:
        charset = resp.headers.get_content_charset() or 'utf-8'
        return resp.read().decode(charset, errors='replace')


def build_record(url: str, topic: str, html: str, notes: str = '') -> dict:
    parsed = urlparse(url)
    source_name = parsed.netloc
    title, content, adapter_notes = extract_generic(url, html)
    merged_notes = ';'.join([x for x in [adapter_notes, notes] if x])
    return {
        'url': url,
        'source_name': source_name,
        'topic': topic,
        'fetched_at': datetime.now(timezone.utc).astimezone().isoformat(timespec='seconds'),
        'title': title,
        'content': content,
        'notes': merged_notes,
    }


def load_urls(job_or_list: Path):
    if job_or_list.suffix.lower() == '.json':
        data = json.loads(job_or_list.read_text(encoding='utf-8'))
        return data.get('topic', ''), data.get('urls', []), data.get('raw_dir')
    urls = [line.strip() for line in job_or_list.read_text(encoding='utf-8').splitlines() if line.strip()]
    return '', urls, None


def main():
    parser = argparse.ArgumentParser(description='Fetch URLs and save raw source JSON files.')
    parser.add_argument('--input', required=True, help='Path to a job json or plain text URL list')
    parser.add_argument('--raw-dir', help='Directory to save raw json files (overrides job raw_dir)')
    parser.add_argument('--topic', default='', help='Optional topic override')
    parser.add_argument('--timeout', type=int, default=20)
    args = parser.parse_args()

    input_path = Path(args.input).resolve()
    topic_from_file, urls, raw_dir_from_file = load_urls(input_path)
    topic = args.topic or topic_from_file or '未命名主题'
    raw_dir = Path(args.raw_dir or raw_dir_from_file or './raw').resolve()
    raw_dir.mkdir(parents=True, exist_ok=True)

    if not urls:
        raise ValueError('No URLs found.')

    success = 0
    failed = 0
    for i, url in enumerate(urls, start=1):
        try:
            html = fetch_url(url, timeout=args.timeout)
            record = build_record(url, topic, html)
            title_part = slugify(record.get('title') or f'source-{i}')[:80]
            out_path = raw_dir / f'{i:03d}-{title_part}.json'
            out_path.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding='utf-8')
            print(f'Saved: {out_path}')
            success += 1
        except Exception as exc:
            fail_record = {
                'url': url,
                'source_name': urlparse(url).netloc,
                'topic': topic,
                'fetched_at': datetime.now(timezone.utc).astimezone().isoformat(timespec='seconds'),
                'title': '',
                'content': '',
                'notes': f'fetch_failed: {exc}',
            }
            out_path = raw_dir / f'{i:03d}-failed.json'
            out_path.write_text(json.dumps(fail_record, ensure_ascii=False, indent=2), encoding='utf-8')
            print(f'Failed: {url} -> {exc}', file=sys.stderr)
            failed += 1

    print(f'Done. success={success} failed={failed} raw_dir={raw_dir}')


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f'Error: {exc}', file=sys.stderr)
        sys.exit(1)
