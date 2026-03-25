#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
TEMPLATE_PATH = BASE_DIR / 'templates' / 'normalized_source_template.md'


def read_text(path: Path) -> str:
    return path.read_text(encoding='utf-8')


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')


def load_raw(path: Path) -> dict:
    data = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(data, dict):
        raise ValueError(f'Invalid raw source json: {path}')
    return data


def normalize_markdown(data: dict) -> str:
    template = read_text(TEMPLATE_PATH)
    return (
        template.replace('来源名称：', f"来源名称：{data.get('source_name', '')}")
        .replace('来源 URL：', f"来源 URL：{data.get('url', '')}")
        .replace('抓取时间：', f"抓取时间：{data.get('fetched_at', '')}")
        .replace('主题：', f"主题：{data.get('topic', '')}")
        .replace('## 正文\n\n', f"## 正文\n\n{(data.get('content') or '').strip()}\n\n")
        .replace('可信度备注：', f"可信度备注：{data.get('notes', '')}")
    )


def collect_raw_files(path: Path):
    if path.is_file():
        return [path]
    return sorted([p for p in path.rglob('*.json') if p.is_file()])


def main():
    parser = argparse.ArgumentParser(description='Normalize raw fetched json sources into markdown files.')
    parser.add_argument('--input', required=True, help='Raw json file or directory')
    parser.add_argument('--output-dir', required=True, help='Directory to write normalized markdown files')
    args = parser.parse_args()

    input_path = Path(args.input).resolve()
    output_dir = Path(args.output_dir).resolve()

    files = collect_raw_files(input_path)
    if not files:
        raise ValueError('No raw json files found.')

    for file in files:
        data = load_raw(file)
        md = normalize_markdown(data)
        out_path = output_dir / f'{file.stem}.md'
        write_text(out_path, md.rstrip() + '\n')
        print(f'Normalized: {out_path}')


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f'Error: {exc}', file=sys.stderr)
        sys.exit(1)
