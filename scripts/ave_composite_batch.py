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


def build_prompt(job):
    role = job["role"]
    ui_priority = job["ui_priority"]
    hardware_note = job.get("hardware_note", "premium product realism")
    screen_present = bool(job.get("screen"))
    if screen_present:
        return f"""Reference image 1 is the exact AVE hardware base plate and must remain dominant. Reference image 2 is the exact AVE UI screen to composite into the device display. Create a premium realistic product composite still for the AVE handheld AI trading terminal. Preserve the hardware identity from image 1 exactly: transparent shell, visible purple internal layers, white-capped thumb joystick with pale green base ring on the left, right-side clustered buttons, bezel depth, camera angle, framing, lighting, reflections, and material layering. Do not redesign the hardware. Replace only the green display area in image 1 with the interface from image 2. The screen content must faithfully match the layout, information hierarchy, color logic, and real trading-terminal feel of image 2, naturally transformed into the device perspective. Keep the UI readable, sharp, and believable under real display glass with subtle reflections and slight screen depth. Intended screen role: {role}. Screen priority: {ui_priority}. Hardware mood: {hardware_note}. Avoid sci-fi HUD graphics, extra floating overlays, fake holograms, new controls, toy-like proportions, altered device geometry, distorted bezel, washed-out UI, oversaturated neon effects, or replacing the transparent-shell design."""
    return f"""Reference image 1 is the exact AVE hardware base plate and must remain dominant. Create a premium realistic hardware still for the AVE handheld AI trading terminal. Preserve the hardware identity from image 1 exactly: transparent shell, visible purple internal layers, white-capped thumb joystick with pale green base ring on the left, right-side clustered buttons, bezel depth, camera angle, framing, lighting, reflections, and material layering. Do not redesign the hardware. Clean up any temporary greenscreen or technical placeholder feel inside the display area and replace it with a believable dark inactive display glass or a minimal neutral system-dark screen treatment, depending on what best supports the shot. Remove any distracting technical annotation text from the asset if present. Intended role: {role}. Screen priority: {ui_priority}. Hardware mood: {hardware_note}. Keep the image premium, restrained, manufacturable, and ad-ready. Avoid sci-fi HUD graphics, extra floating overlays, toy-like proportions, altered device geometry, distorted bezel, cheap plastic feel, or noisy engineering clutter."""


def run_job(api_key, api_url, model, job, output_dir, timeout):
    plate = Path(job["plate"])
    screen_value = job.get("screen")
    screen = Path(screen_value) if screen_value else None
    out = output_dir / job["output_name"]
    prompt_txt = output_dir / f"{out.stem}_prompt.txt"
    prompt = build_prompt(job)

    prompt_txt.write_text(
        f"id: {job['id']}\n"
        f"plate: {plate}\n"
        f"screen: {screen if screen else '(none)'}\n"
        f"output: {out}\n\n"
        f"prompt:\n{prompt}\n",
        encoding="utf-8",
    )

    refs = [str(plate)]
    if screen:
        refs.append(str(screen))
    img = generate_image(api_key, api_url, model, prompt, reference_images=refs, timeout=timeout)
    if not img:
        return {"id": job["id"], "status": "failed", "output": str(out)}

    out.write_bytes(img)
    return {
        "id": job["id"],
        "status": "ok",
        "output": str(out),
        "bytes": len(img),
    }


def main():
    parser = argparse.ArgumentParser(description="Run AVE composite image batch")
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
