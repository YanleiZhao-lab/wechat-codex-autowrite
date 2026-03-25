#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
NORMALIZE = BASE_DIR / 'normalize_sources.py'
PREPROCESS = BASE_DIR / 'preprocess.py'
WRITER = BASE_DIR / 'writer.py'


def load_job(path: Path) -> dict:
    data = json.loads(path.read_text(encoding='utf-8'))
    required = ['topic', 'raw_input', 'normalized_dir', 'processed_dir', 'bundle_output', 'article_output']
    missing = [k for k in required if not data.get(k)]
    if missing:
        raise ValueError(f'Missing required fields in flow job: {", ".join(missing)}')
    return data


def resolve(base: Path, value: str) -> str:
    p = Path(value)
    return str((base / p).resolve() if not p.is_absolute() else p.resolve())


def main():
    parser = argparse.ArgumentParser(description='Run normalize -> preprocess -> write full article flow from a JSON job.')
    parser.add_argument('--job', required=True, help='Path to full flow job json')
    args = parser.parse_args()

    job_path = Path(args.job).resolve()
    job = load_job(job_path)
    base = job_path.parent

    normalize_cmd = [
        sys.executable,
        str(NORMALIZE),
        '--input', resolve(base, job['raw_input']),
        '--output-dir', resolve(base, job['normalized_dir']),
    ]

    preprocess_cmd = [
        sys.executable,
        str(PREPROCESS),
        '--input', resolve(base, job['normalized_dir']),
        '--processed-dir', resolve(base, job['processed_dir']),
        '--bundle-output', resolve(base, job['bundle_output']),
        '--topic', str(job['topic']),
        '--audience', str(job.get('audience', '对该主题感兴趣的公众号读者')),
        '--style', str(job.get('style', '专业、直接、少空话、信息密度高')),
        '--length', str(job.get('length', 1800)),
    ]

    writer_cmd = [
        sys.executable,
        str(WRITER),
        '--topic', str(job['topic']),
        '--refs', resolve(base, job['bundle_output']),
        '--mode', str(job.get('mode', 'full')),
        '--output', resolve(base, job['article_output']),
        '--audience', str(job.get('audience', '对该主题感兴趣的公众号读者')),
        '--style', str(job.get('style', '专业、直接、少空话、信息密度高')),
        '--length', str(job.get('length', 1800)),
    ]

    if job.get('check_output'):
        writer_cmd.extend(['--check-output', resolve(base, job['check_output'])])
    if job.get('save_prompt_dir'):
        writer_cmd.extend(['--save-prompt-dir', resolve(base, job['save_prompt_dir'])])

    for label, cmd in [
        ('normalize', normalize_cmd),
        ('preprocess', preprocess_cmd),
        ('writer', writer_cmd),
    ]:
        print(f'Running step: {label}')
        result = subprocess.run(cmd)
        if result.returncode != 0:
            print(f'Step failed: {label}', file=sys.stderr)
            sys.exit(result.returncode)

    print('Full flow completed.')


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f'Error: {exc}', file=sys.stderr)
        sys.exit(1)
