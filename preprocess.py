#!/usr/bin/env python3
import argparse
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PROMPTS_DIR = BASE_DIR / 'prompts'
SUMMARY_PROMPT = PROMPTS_DIR / 'preprocess_summary_prompt.md'
BUNDLE_PROMPT = PROMPTS_DIR / 'bundle_prompt.md'


def read_text(path: Path) -> str:
    return path.read_text(encoding='utf-8')


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')


def collect_files(path: Path):
    if path.is_file():
        return [path]
    return sorted([p for p in path.rglob('*') if p.is_file() and p.suffix.lower() in {'.md', '.txt'}])


def run_codex(prompt: str) -> str:
    cmd = ['codex', 'exec', '--full-auto', prompt]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    except FileNotFoundError:
        raise RuntimeError('codex CLI not found. Please install Codex and ensure it is on PATH.')
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(
            'codex execution failed.\n'
            f'Exit code: {exc.returncode}\n'
            f'STDOUT:\n{exc.stdout}\n\nSTDERR:\n{exc.stderr}'
        )
    output = (result.stdout or '').strip()
    if not output:
        raise RuntimeError('codex returned empty output.')
    return output


def build_summary_prompt(text: str, source_name: str) -> str:
    p = read_text(SUMMARY_PROMPT).strip()
    return f"{p}\n\n# 来源文件\n{source_name}\n\n# 待处理内容\n\n{text}".strip()


def build_bundle_prompt(topic: str, processed_docs: str, audience: str, style: str, length: int) -> str:
    p = read_text(BUNDLE_PROMPT).strip()
    return (
        f"{p}\n\n# 写作主题\n{topic}\n\n# 目标读者\n{audience}\n\n# 建议风格\n{style}\n\n# 目标字数\n{length}\n\n# 已处理素材\n\n{processed_docs}"
    ).strip()


def main():
    parser = argparse.ArgumentParser(description='Preprocess collected sources into a writing bundle using Codex CLI.')
    parser.add_argument('--input', required=True, help='Raw or normalized source file/dir')
    parser.add_argument('--processed-dir', required=True, help='Directory to save processed notes')
    parser.add_argument('--bundle-output', required=True, help='Output path for final writing bundle')
    parser.add_argument('--topic', required=True, help='Topic for the final article')
    parser.add_argument('--audience', default='对该主题感兴趣的公众号读者')
    parser.add_argument('--style', default='专业、直接、少空话、信息密度高')
    parser.add_argument('--length', type=int, default=1800)
    args = parser.parse_args()

    input_path = Path(args.input).resolve()
    processed_dir = Path(args.processed_dir).resolve()
    bundle_output = Path(args.bundle_output).resolve()

    files = collect_files(input_path)
    if not files:
        raise ValueError('No source files found for preprocessing.')

    processed_chunks = []
    for file in files:
        content = read_text(file)
        prompt = build_summary_prompt(content, file.name)
        processed = run_codex(prompt)
        out_path = processed_dir / f'{file.stem}.processed.md'
        write_text(out_path, processed.rstrip() + '\n')
        processed_chunks.append(f'\n---\n[处理结果] {out_path.name}\n\n{processed}')

    bundle_prompt = build_bundle_prompt(args.topic, '\n'.join(processed_chunks), args.audience, args.style, args.length)
    bundle = run_codex(bundle_prompt)
    write_text(bundle_output, bundle.rstrip() + '\n')

    print(f'Processed notes saved to: {processed_dir}')
    print(f'Bundle written to: {bundle_output}')


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f'Error: {exc}', file=sys.stderr)
        sys.exit(1)
