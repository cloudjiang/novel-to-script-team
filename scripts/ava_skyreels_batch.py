#!/usr/bin/env python3
import argparse
import json
import os
import time
from pathlib import Path
from urllib.parse import urlparse

import requests

SUBMIT_URL = "https://api-gateway.skyreels.ai/api/v1/video/image2video/submit"
TASK_URL = "https://api-gateway.skyreels.ai/api/v1/video/image2video/task/{task_id}"
TMPFILES_UPLOAD_URL = "https://tmpfiles.org/api/v1/upload"
CATBOX_UPLOAD_URL = "https://catbox.moe/user/api.php"


def load_env_key(name: str) -> str:
    env_path = Path('.env')
    if env_path.exists():
        for line in env_path.read_text(encoding='utf-8').splitlines():
            if '=' not in line or line.strip().startswith('#'):
                continue
            k, v = line.split('=', 1)
            if k.strip() == name:
                return v.strip()
    val = os.getenv(name)
    if val:
        return val
    raise SystemExit(f"missing env key: {name}")


def to_tmpfiles_dl(url: str) -> str:
    url = url.replace('http://', 'https://')
    if '/dl/' in url:
        return url
    parsed = urlparse(url)
    path = parsed.path
    if not path.startswith('/'):
        path = '/' + path
    return f"https://{parsed.netloc}/dl{path}"


def upload_tmpfiles(path: str, timeout: int = 120) -> str:
    with open(path, 'rb') as f:
        resp = requests.post(TMPFILES_UPLOAD_URL, files={'file': f}, timeout=timeout)
    resp.raise_for_status()
    data = resp.json()
    if data.get('status') != 'success':
        raise RuntimeError(f"tmpfiles upload failed: {data}")
    return to_tmpfiles_dl(data['data']['url'])


def upload_catbox(path: str, timeout: int = 120) -> str:
    with open(path, 'rb') as f:
        resp = requests.post(CATBOX_UPLOAD_URL, data={'reqtype': 'fileupload'}, files={'fileToUpload': f}, timeout=timeout)
    resp.raise_for_status()
    url = resp.text.strip()
    if not url.startswith('http'):
        raise RuntimeError(f"catbox upload failed: {url}")
    return url.replace('http://', 'https://')


def upload_image(path: str, timeout: int = 120) -> str:
    last_err = None
    for _ in range(3):
        try:
            return upload_tmpfiles(path, timeout=timeout)
        except Exception as e:
            last_err = e
            time.sleep(2)
    try:
        return upload_catbox(path, timeout=timeout)
    except Exception as e:
        last_err = e
    raise last_err


def submit_shot(api_key: str, shot: dict) -> dict:
    payload = {
        'api_key': api_key,
        'prompt': shot['prompt'],
        'first_frame_image': shot['first'],
        'duration': shot['duration'],
        'sound': False,
        'prompt_optimizer': True,
        'resolution': '1080p',
        'mode': 'std',
    }
    if shot.get('end'):
        payload['end_frame_image'] = shot['end']
    resp = requests.post(SUBMIT_URL, json=payload, timeout=120)
    if resp.status_code >= 400:
        raise RuntimeError(f'submit failed status={resp.status_code} body={resp.text}')
    return resp.json()


def query_task(task_id: str) -> dict:
    resp = requests.get(TASK_URL.format(task_id=task_id), timeout=120)
    resp.raise_for_status()
    return resp.json()


def download_file(url: str, outpath: Path):
    resp = requests.get(url, timeout=240)
    resp.raise_for_status()
    outpath.write_bytes(resp.content)


def log(log_path: Path, msg: str):
    ts = time.strftime('%Y-%m-%d %H:%M:%S')
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    with log_path.open('a', encoding='utf-8') as f:
        f.write(line + '\n')


def main():
    parser = argparse.ArgumentParser(description='Run SkyReels image2video batch for AVA')
    parser.add_argument('--jobs', required=True)
    parser.add_argument('--output-dir', required=True)
    parser.add_argument('--max-active', type=int, default=4)
    parser.add_argument('--poll-interval', type=int, default=25)
    args = parser.parse_args()

    api_key = load_env_key('SKYREELS_API_KEY')
    jobs = json.loads(Path(args.jobs).read_text(encoding='utf-8'))
    outdir = Path(args.output_dir)
    outdir.mkdir(parents=True, exist_ok=True)
    log_path = outdir / 'run.log'
    asset_urls_path = outdir / 'asset-urls.json'
    tasks_path = outdir / 'tasks.json'
    results_path = outdir / 'results.json'

    asset_urls = {}
    if asset_urls_path.exists():
        try:
            asset_urls = json.loads(asset_urls_path.read_text(encoding='utf-8'))
        except Exception:
            asset_urls = {}
    unique_paths = []
    for shot in jobs:
        for k in ('first_local', 'end_local'):
            p = shot.get(k)
            if p and p not in unique_paths:
                unique_paths.append(p)

    for path in unique_paths:
        if path in asset_urls:
            log(log_path, f'upload skip {path} -> {asset_urls[path]}')
            continue
        log(log_path, f'upload start {path}')
        url = upload_image(path)
        asset_urls[path] = url
        log(log_path, f'upload ok {path} -> {url}')
        asset_urls_path.write_text(json.dumps(asset_urls, ensure_ascii=False, indent=2), encoding='utf-8')

    pending = []
    for shot in jobs:
        s = dict(shot)
        s['first'] = asset_urls[s['first_local']]
        if s.get('end_local'):
            s['end'] = asset_urls[s['end_local']]
        pending.append(s)

    tasks = {}
    if tasks_path.exists():
        try:
            tasks = json.loads(tasks_path.read_text(encoding='utf-8'))
        except Exception:
            tasks = {}

    completed = {}
    failed = {}
    remaining_from_results = []
    if results_path.exists():
        try:
            prev = json.loads(results_path.read_text(encoding='utf-8'))
            completed = prev.get('completed', {}) or {}
            failed = prev.get('failed', {}) or {}
            remaining_from_results = prev.get('remaining', []) or []
        except Exception:
            completed = {}
            failed = {}
            remaining_from_results = []

    completed_ids = set(completed.keys())
    failed_ids = set(failed.keys())
    active = {}

    jobs_by_id = {shot['id']: shot for shot in pending}
    pending = [shot for shot in pending if shot['id'] not in completed_ids and shot['id'] not in failed_ids and shot['id'] not in tasks]

    for shot_id, rec in tasks.items():
        if shot_id in completed_ids or shot_id in failed_ids:
            continue
        shot = jobs_by_id.get(shot_id)
        if not shot:
            continue
        active[shot_id] = {'task_id': rec['task_id'], 'shot': shot}

    def submit_more():
        while pending and len(active) < args.max_active:
            shot = pending.pop(0)
            submit_response = submit_shot(api_key, shot)
            task_id = submit_response['task_id']
            active[shot['id']] = {'task_id': task_id, 'shot': shot}
            tasks[shot['id']] = {'task_id': task_id, 'shot': {'id': shot['id'], 'first': shot['first'], 'prompt': shot['prompt'], 'duration': shot['duration']}}
            if shot.get('end'):
                tasks[shot['id']]['shot']['end'] = shot['end']
            tasks[shot['id']]['submit_response'] = submit_response
            tasks_path.write_text(json.dumps(tasks, ensure_ascii=False, indent=2), encoding='utf-8')
            log(log_path, f"submit ok {shot['id']} task_id={task_id}")
            time.sleep(1)

    submit_more()

    while active:
        time.sleep(args.poll_interval)
        for shot_id in list(active.keys()):
            task_id = active[shot_id]['task_id']
            shot = active[shot_id]['shot']
            q = query_task(task_id)
            status = q.get('status', '')
            msg = q.get('msg', '')
            log(log_path, f"poll {shot_id} task_id={task_id} status={status} msg={msg}")
            if status == 'success':
                video_url = q['data']['video_url']
                outpath = outdir / shot['output_name']
                download_file(video_url, outpath)
                log(log_path, f"download ok {shot_id} -> {outpath}")
                completed[shot_id] = {
                    'task_id': task_id,
                    'video_url': video_url,
                    'local_path': str(outpath),
                    'duration': q['data'].get('duration'),
                    'resolution': q['data'].get('resolution'),
                    'raw': q,
                }
                del active[shot_id]
                results_path.write_text(json.dumps({'completed': completed, 'failed': failed, 'remaining': list(active.keys()) + [s['id'] for s in pending]}, ensure_ascii=False, indent=2), encoding='utf-8')
                submit_more()
            elif status in ('failed', 'unknown'):
                failed[shot_id] = {'task_id': task_id, 'raw': q}
                del active[shot_id]
                results_path.write_text(json.dumps({'completed': completed, 'failed': failed, 'remaining': list(active.keys()) + [s['id'] for s in pending]}, ensure_ascii=False, indent=2), encoding='utf-8')
                submit_more()

    results_path.write_text(json.dumps({'completed': completed, 'failed': failed, 'remaining': []}, ensure_ascii=False, indent=2), encoding='utf-8')
    log(log_path, f"batch done: completed={len(completed)} failed={len(failed)}")


if __name__ == '__main__':
    main()
