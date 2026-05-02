#!/usr/bin/env python3
import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.generate_image import generate_image, load_image_api_config


def run_job(api_key, api_url, model, job, output_dir, timeout):
    out = output_dir / job["output_name"]
    prompt_txt = output_dir / f"{out.stem}_prompt.txt"
    refs = job.get("refs", [])
    prompt = job["prompt"]

    prompt_txt.write_text(
        f"id: {job['id']}\n"
        f"refs:\n" + "\n".join(f"- {r}" for r in refs) + "\n\n"
        f"output: {out}\n\n"
        f"prompt:\n{prompt}\n",
        encoding="utf-8",
    )

    img = generate_image(api_key, api_url, model, prompt, reference_images=refs if refs else None, timeout=timeout)
    if not img:
        return {"id": job["id"], "status": "failed", "output": str(out)}

    out.write_bytes(img)
    return {"id": job["id"], "status": "ok", "output": str(out), "bytes": len(img)}


def main():
    parser = argparse.ArgumentParser(description="Run generic AVE still batch")
    parser.add_argument("--jobs", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--max-workers", type=int, default=2)
    parser.add_argument("--timeout", type=int, default=420)
    parser.add_argument("--skip-existing", action="store_true")
    args = parser.parse_args()

    api_key, api_url, model = load_image_api_config()
    jobs_path = Path(args.jobs)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    jobs = json.loads(jobs_path.read_text(encoding="utf-8"))
    runnable = []
    for job in jobs:
        out = output_dir / job["output_name"]
        if args.skip_existing and out.exists() and out.stat().st_size > 0:
            print(f"skip existing: {out.name}")
            continue
        runnable.append(job)

    print(f"running {len(runnable)} jobs with max_workers={args.max_workers}")
    results = []
    with ThreadPoolExecutor(max_workers=args.max_workers) as ex:
        futs = {ex.submit(run_job, api_key, api_url, model, job, output_dir, args.timeout): job for job in runnable}
        for fut in as_completed(futs):
            job = futs[fut]
            try:
                result = fut.result()
            except Exception as e:
                result = {"id": job["id"], "status": "failed", "output": str(output_dir / job["output_name"]), "error": str(e)}
            results.append(result)
            print(json.dumps(result, ensure_ascii=False))

    results_path = output_dir / "results.json"
    results_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    ok = sum(1 for r in results if r.get("status") == "ok")
    fail = len(results) - ok
    print(f"done: ok={ok}, fail={fail}, results={results_path}")


if __name__ == "__main__":
    main()
