#!/usr/bin/env python3
import argparse
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PROMPTS_DIR = BASE_DIR / 'prompts'
TEMPLATES_DIR = BASE_DIR / 'templates'
SYSTEM_PROMPT_FILE = PROMPTS_DIR / 'article_system_prompt.md'
REVIEW_PROMPT_FILE = PROMPTS_DIR / 'article_review_prompt.md'
FORMAT_PROMPT_FILE = PROMPTS_DIR / 'format_wechat_prompt.md'
PREPUBLISH_CHECK_PROMPT_FILE = PROMPTS_DIR / 'prepublish_check_prompt.md'
TEMPLATE_FILE = TEMPLATES_DIR / 'article_request_template.md'


def read_text(path: Path) -> str:
    return path.read_text(encoding='utf-8')


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')


def collect_references(ref_path: Path) -> str:
    if not ref_path.exists():
        raise FileNotFoundError(f'Reference path not found: {ref_path}')

    if ref_path.is_file():
        files = [ref_path]
    else:
        files = sorted([
            p for p in ref_path.rglob('*')
            if p.is_file() and p.suffix.lower() in {'.txt', '.md'}
        ])

    if not files:
        raise ValueError('No .txt or .md reference files found.')

    chunks = []
    for file in files:
        chunks.append(f'\n---\n[来源文件] {file.name}\n')
        chunks.append(read_text(file).strip())
    return '\n'.join(chunks).strip()


def build_generate_prompt(topic: str, audience: str, style: str, length: int, references: str) -> str:
    system_prompt = read_text(SYSTEM_PROMPT_FILE).strip()
    template = read_text(TEMPLATE_FILE)
    request_body = (
        template.replace('{{topic}}', topic)
        .replace('{{audience}}', audience)
        .replace('{{style}}', style)
        .replace('{{length}}', str(length))
        .replace('{{references}}', references)
    )
    return f"{system_prompt}\n\n{request_body}".strip()


def build_review_prompt(article: str) -> str:
    review_prompt = read_text(REVIEW_PROMPT_FILE).strip()
    return f"{review_prompt}\n\n# 待审稿文章\n\n{article}".strip()


def build_format_prompt(article: str) -> str:
    format_prompt = read_text(FORMAT_PROMPT_FILE).strip()
    return f"{format_prompt}\n\n# 待整理文章\n\n{article}".strip()


def build_prepublish_check_prompt(article: str) -> str:
    check_prompt = read_text(PREPUBLISH_CHECK_PROMPT_FILE).strip()
    return f"{check_prompt}\n\n# 待检查文章\n\n{article}".strip()


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


def main():
    parser = argparse.ArgumentParser(description='Generate WeChat article drafts with Codex CLI.')
    parser.add_argument('--topic', required=True, help='Article topic')
    parser.add_argument('--refs', required=True, help='Reference file or directory (.md/.txt)')
    parser.add_argument('--audience', default='对该主题感兴趣的公众号读者', help='Target audience')
    parser.add_argument('--style', default='专业、直接、少空话、信息密度高', help='Writing style')
    parser.add_argument('--length', type=int, default=1800, help='Approx target length in Chinese characters')
    parser.add_argument('--output', required=True, help='Output markdown file path')
    parser.add_argument('--mode', choices=['draft', 'full'], default='full', help='draft=仅生成初稿, full=生成+审稿+格式整理')
    parser.add_argument('--save-prompt-dir', help='Optional directory to save compiled prompts for debugging')
    parser.add_argument('--check-output', help='Optional path to save prepublish check result')
    args = parser.parse_args()

    references = collect_references(Path(args.refs).resolve())
    generate_prompt = build_generate_prompt(args.topic, args.audience, args.style, args.length, references)

    save_prompt_dir = Path(args.save_prompt_dir).resolve() if args.save_prompt_dir else None
    if save_prompt_dir:
        write_text(save_prompt_dir / '01_generate_prompt.md', generate_prompt)

    draft_article = run_codex(generate_prompt)

    final_article = draft_article
    if args.mode == 'full':
        review_prompt = build_review_prompt(draft_article)
        if save_prompt_dir:
            write_text(save_prompt_dir / '02_review_prompt.md', review_prompt)
        reviewed_article = run_codex(review_prompt)

        format_prompt = build_format_prompt(reviewed_article)
        if save_prompt_dir:
            write_text(save_prompt_dir / '03_format_prompt.md', format_prompt)
        final_article = run_codex(format_prompt)

    output_path = Path(args.output).resolve()
    write_text(output_path, final_article.rstrip() + '\n')

    if args.check_output:
        check_prompt = build_prepublish_check_prompt(final_article)
        if save_prompt_dir:
            write_text(save_prompt_dir / '04_prepublish_check_prompt.md', check_prompt)
        check_result = run_codex(check_prompt)
        write_text(Path(args.check_output).resolve(), check_result.rstrip() + '\n')

    print(f'Article written to: {output_path}')
    print(f'Mode: {args.mode}')
    if args.check_output:
        print(f'Check report written to: {Path(args.check_output).resolve()}')


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f'Error: {exc}', file=sys.stderr)
        sys.exit(1)
