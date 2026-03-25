#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
WRITER = BASE_DIR / 'writer.py'


def load_job(path: Path) -> dict:
    data = json.loads(path.read_text(encoding='utf-8'))
    required = ['topic', 'refs', 'output']
    missing = [k for k in required if not data.get(k)]
    if missing:
        raise ValueError(f'Missing required fields in job file: {", ".join(missing)}')
    return data


def main():
    parser = argparse.ArgumentParser(description='Run article generation job from JSON spec.')
    parser.add_argument('--job', required=True, help='Path to job json file')
    args = parser.parse_args()

    job_path = Path(args.job).resolve()
    job = load_job(job_path)

    cmd = [
        sys.executable,
        str(WRITER),
        '--topic', str(job['topic']),
        '--refs', str((job_path.parent / job['refs']).resolve() if not Path(job['refs']).is_absolute() else Path(job['refs']).resolve()),
        '--output', str((job_path.parent / job['output']).resolve() if not Path(job['output']).is_absolute() else Path(job['output']).resolve()),
        '--audience', str(job.get('audience', '对该主题感兴趣的公众号读者')),
        '--style', str(job.get('style', '专业、直接、少空话、信息密度高')),
        '--length', str(job.get('length', 1800)),
        '--mode', str(job.get('mode', 'full')),
    ]

    save_prompt_dir = job.get('save_prompt_dir')
    if save_prompt_dir:
        resolved_prompt_dir = (job_path.parent / save_prompt_dir).resolve() if not Path(save_prompt_dir).is_absolute() else Path(save_prompt_dir).resolve()
        cmd.extend(['--save-prompt-dir', str(resolved_prompt_dir)])

    check_output = job.get('check_output')
    if check_output:
        resolved_check_output = (job_path.parent / check_output).resolve() if not Path(check_output).is_absolute() else Path(check_output).resolve()
        cmd.extend(['--check-output', str(resolved_check_output)])

    result = subprocess.run(cmd)
    sys.exit(result.returncode)


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f'Error: {exc}', file=sys.stderr)
        sys.exit(1)
