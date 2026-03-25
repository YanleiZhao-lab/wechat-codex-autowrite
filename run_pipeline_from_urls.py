#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CRAWL = BASE_DIR / 'crawl_urls.py'
FULL_FLOW = BASE_DIR / 'run_full_flow.py'


def load_job(path: Path) -> dict:
    data = json.loads(path.read_text(encoding='utf-8'))
    required = ['topic', 'urls_input', 'raw_dir', 'normalized_dir', 'processed_dir', 'bundle_output', 'article_output']
    missing = [k for k in required if not data.get(k)]
    if missing:
        raise ValueError(f'Missing required fields in pipeline job: {", ".join(missing)}')
    return data


def resolve(base: Path, value: str) -> str:
    p = Path(value)
    return str((base / p).resolve() if not p.is_absolute() else p.resolve())


def main():
    parser = argparse.ArgumentParser(description='Run crawl -> normalize -> preprocess -> write pipeline from URLs.')
    parser.add_argument('--job', required=True, help='Path to pipeline job json')
    args = parser.parse_args()

    job_path = Path(args.job).resolve()
    job = load_job(job_path)
    base = job_path.parent

    crawl_cmd = [
        sys.executable,
        str(CRAWL),
        '--input', resolve(base, job['urls_input']),
        '--raw-dir', resolve(base, job['raw_dir']),
        '--topic', str(job['topic']),
    ]

    flow_job_path = base / '.tmp_full_flow_job.json'
    flow_job = {
        'topic': job['topic'],
        'raw_input': job['raw_dir'],
        'normalized_dir': job['normalized_dir'],
        'processed_dir': job['processed_dir'],
        'bundle_output': job['bundle_output'],
        'article_output': job['article_output'],
        'check_output': job.get('check_output'),
        'audience': job.get('audience', '对该主题感兴趣的公众号读者'),
        'style': job.get('style', '专业、直接、少空话、信息密度高'),
        'length': job.get('length', 1800),
        'mode': job.get('mode', 'full'),
        'save_prompt_dir': job.get('save_prompt_dir'),
    }
    flow_job_path.write_text(json.dumps(flow_job, ensure_ascii=False, indent=2), encoding='utf-8')

    full_flow_cmd = [
        sys.executable,
        str(FULL_FLOW),
        '--job', str(flow_job_path.resolve()),
    ]

    for label, cmd in [('crawl', crawl_cmd), ('full_flow', full_flow_cmd)]:
        print(f'Running step: {label}')
        result = subprocess.run(cmd)
        if result.returncode != 0:
            print(f'Step failed: {label}', file=sys.stderr)
            sys.exit(result.returncode)

    print('Pipeline completed.')


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f'Error: {exc}', file=sys.stderr)
        sys.exit(1)
