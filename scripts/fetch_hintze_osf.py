"""Download an untouched copy of Hintze et al.'s OSF project (WGDQ4) into hintze_osf/.

Walks the osfstorage tree through the OSF v2 API, preserves paths, skips files already present
with the same size, and writes hintze_osf/MANIFEST.tsv (path, size, md5, sha256, date_modified).
"""
import hashlib, json, pathlib, sys, time, urllib.request

NODE = "wgdq4"
OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "hintze_osf")


def get_json(url):
    for attempt in range(5):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "ai_to_ai_loops/0.1"}), timeout=120) as r:
                return json.load(r)
        except Exception as e:  # noqa: BLE001
            print("retry", attempt, url, e, file=sys.stderr); time.sleep(5 * (attempt + 1))
    raise SystemExit(f"failed: {url}")


def walk(url):
    while url:
        page = get_json(url)
        for item in page["data"]:
            a = item["attributes"]
            if a["kind"] == "folder":
                yield from walk(item["relationships"]["files"]["links"]["related"]["href"])
            else:
                yield a, item["links"]["download"]
        url = page["links"].get("next")


def download(url, dest, size):
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    for attempt in range(5):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "ai_to_ai_loops/0.1"}), timeout=600) as r, open(tmp, "wb") as f:
                while True:
                    chunk = r.read(1 << 20)
                    if not chunk:
                        break
                    f.write(chunk)
            if size is not None and tmp.stat().st_size != size:
                raise IOError(f"size mismatch {tmp.stat().st_size} != {size}")
            tmp.rename(dest)
            return
        except Exception as e:  # noqa: BLE001
            print("retry", attempt, dest, e, file=sys.stderr); time.sleep(5 * (attempt + 1))
    raise SystemExit(f"failed: {dest}")


def main():
    rows = []
    for a, dl in walk(f"https://api.osf.io/v2/nodes/{NODE}/files/osfstorage/?page%5Bsize%5D=100"):
        rel = a["materialized_path"].lstrip("/")
        dest = OUT / rel
        if dest.exists() and a["size"] is not None and dest.stat().st_size == a["size"]:
            status = "kept"
        else:
            download(dl, dest, a["size"]); status = "downloaded"
        sha = hashlib.sha256(dest.read_bytes()).hexdigest()
        h = a["extra"]["hashes"]
        if h.get("sha256") and h["sha256"] != sha:
            raise SystemExit(f"sha256 mismatch for {rel}")
        rows.append((rel, dest.stat().st_size, h.get("md5") or "", sha, a.get("date_modified") or ""))
        print(f"{status:10s} {dest.stat().st_size:>12,}  {rel}")
    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / "MANIFEST.tsv", "w") as f:
        f.write("path\tsize\tmd5\tsha256\tdate_modified\n")
        for r in rows:
            f.write("\t".join(map(str, r)) + "\n")
    print(f"{len(rows)} files, {sum(r[1] for r in rows):,} bytes -> {OUT}")


if __name__ == "__main__":
    main()
