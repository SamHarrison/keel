"""Hash-lock versioning and the diff-anchored ledger audit (docs/process.md §§1–2).

ledger/versions.lock is a *ledger*: machine-written, committed, never
hand-edited. `reconcile()` bumps versions on normative-text change and
cascades every inbound pin in one pass (the content hash excludes pin
numbers, so re-pinning is not itself a change). `check()` fails the gate on
any drift. `audit()` closes the trust hole the lock alone leaves open: every
lock delta must be entailed by an authored-text delta in the same change,
verified against a git base — hand-editing the lock fails CI instead of
silently redefining what alias@N means.
"""
import json
import re
import subprocess

from . import hashing, refs


def lock_path(root):
    return root / "ledger" / "versions.lock"


def load_lock(root):
    p = lock_path(root)
    return json.loads(p.read_text()) if p.exists() else {}


def save_lock(root, lock):
    p = lock_path(root)
    p.parent.mkdir(exist_ok=True)
    p.write_text(json.dumps(lock, indent=1, sort_keys=True) + "\n")


def reconcile(items, lock):
    """items: {key: {"version": int, "text": str}} for every real identity.
    Returns (new_lock, bumped {key: (old,new)}, added [key], orphaned [key]).
    Lock is authoritative for unchanged text; changed text bumps lock+1."""
    new_lock, bumped, added = {}, {}, []
    for key, it in sorted(items.items()):
        h = hashing.content_hash(it["text"])
        if key in lock:
            if lock[key]["hash"] == h:
                new_lock[key] = dict(lock[key])
            else:
                v = lock[key]["version"] + 1
                new_lock[key] = {"version": v, "hash": h}
                bumped[key] = (lock[key]["version"], v)
        else:
            new_lock[key] = {"version": it["version"], "hash": h}
            added.append(key)
    orphaned = [k for k in lock if k not in items]
    return new_lock, bumped, added, orphaned


def drift(items, lock):
    """Gate check: list of error strings when the tree and lock disagree."""
    errs = []
    for key, it in sorted(items.items()):
        h = hashing.content_hash(it["text"])
        if key not in lock:
            errs.append(f"{key}: not in versions.lock (run `req version`)")
        elif lock[key]["hash"] != h:
            errs.append(f"{key}: text changed but version not reconciled "
                        f"(run `req version`)")
        elif lock[key]["version"] != it["version"]:
            errs.append(f"{key}: version {it['version']} in tree, "
                        f"{lock[key]['version']} in versions.lock")
    for key in sorted(set(lock) - set(items)):
        errs.append(f"{key}: in versions.lock but not in the tree "
                    f"(identities retire; ledger entries never delete — "
                    f"run `req version` to mark, never hand-edit)")
    return errs


def cascade_file(text, bumped):
    """Rewrite pins to every bumped identity in one file's raw text.
    Textual, so authored comments and formatting survive. Returns
    (new_text, hits)."""
    total = 0
    for alias, (_, new) in bumped.items():
        text, hits = refs.repin(text, alias, new)
        total += hits
    return text, total


def _git(root, *args):
    r = subprocess.run(["git", *args], capture_output=True, text=True, cwd=root)
    return r.returncode, r.stdout


def audit(root, items, base="HEAD"):
    """Diff-anchored ledger audit (Ring 2/3). Compares the working tree's
    lock against the lock at `base`: every entry change must correspond to a
    real text change, versions move by exactly +1, and no entry disappears.
    Returns (errors, note). Outside a git repo returns a note only — Ring 1
    runs drift(); the audit belongs to push/CI rings, which are always git.
    """
    code, out = _git(root, "rev-parse", "--is-inside-work-tree")
    if code != 0 or out.strip() != "true":
        return [], "audit: not a git repository — skipped (Rings 2/3 only)"
    code, out = _git(root, "show", f"{base}:ledger/versions.lock")
    base_lock = json.loads(out) if code == 0 and out.strip() else {}
    lock = load_lock(root)
    errs = []
    for key in sorted(set(base_lock) - set(lock)):
        errs.append(f"audit: ledger entry {key} deleted (entries never delete)")
    for key in sorted(lock):
        cur, old = lock[key], base_lock.get(key)
        it = items.get(key)
        if it is None:
            continue  # retirement bookkeeping handled by drift()
        expect_hash = hashing.content_hash(it["text"])
        if cur["hash"] != expect_hash:
            errs.append(f"audit: {key} lock hash does not match the tree")
        if old is None:
            continue
        if cur["hash"] == old["hash"] and cur["version"] != old["version"]:
            errs.append(f"audit: {key} version moved {old['version']}→"
                        f"{cur['version']} with no text change")
        if cur["hash"] != old["hash"] and cur["version"] != old["version"] + 1:
            errs.append(f"audit: {key} text changed but version moved "
                        f"{old['version']}→{cur['version']} (expected "
                        f"{old['version'] + 1})")
    return errs, None


def changed_keys(root, base="HEAD"):
    """Aliases whose rows are new or textually changed vs base — the changed-row
    severity scope. Compares parsed rows, not diff lines (a text-only edit
    leaves the alias line in unchanged context). Returns None outside git
    (caller treats everything as corpus-wide)."""
    import yaml

    def rows_of(text):
        out = {}
        try:
            data = yaml.safe_load(text) or {}
        except yaml.YAMLError:
            return out
        for key in ("requirements", "stakeholders", "constraints"):
            for row in (data.get(key) or []):
                if isinstance(row, dict) and "alias" in row:
                    out[str(row["alias"])] = (
                        row.get("text") or row.get("statement") or
                        row.get("role") or "",
                        row.get("rationale") or "")
        return out

    code, out = _git(root, "rev-parse", "--is-inside-work-tree")
    if code != 0 or out.strip() != "true":
        return None
    code, names = _git(root, "diff", "--name-only", base, "--", "docs")
    if code != 0:
        return None
    changed = set()
    for name in names.split():
        p = root / name
        cur = rows_of(p.read_text()) if p.exists() else {}
        code, old_text = _git(root, "show", f"{base}:{name}")
        old = rows_of(old_text) if code == 0 else {}
        for alias, body in cur.items():
            if old.get(alias) != body:
                changed.add(alias)
    return changed
