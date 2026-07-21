"""The one definition of keel's reference grammar (K-21, consolidation §3.2).

Forms, scanned in row text/statement/rationale, links targets, ADR bodies,
review documents, and test citations:

    [[alias]]              floating — "whatever this statement says now"
    [[alias@N]]            pinned — hard-errors when the target moves (K-17)
    [[HOLE "phrase" was:OLD-ID]]   unresolved — fails every gate until judged
    alias@N                bare pin (refs: lists, links targets, test names)
    section:name           links.yaml section target (non-normative grouping)

Anything else inside [[...]] is a MalformedReferenceError at load time —
typos are reported, never silently skipped.
"""
import re

ALIAS = r"[a-z]+[-._][a-z]+"
REF_RE = re.compile(r"\[\[(" + ALIAS + r")(?:@(\d+))?\]\]")
HOLE_RE = re.compile(r'\[\[HOLE "(?P<phrase>[^"]+)" was:(?P<was>[A-Za-z0-9._-]+)\]\]')
ANY_BRACKET_RE = re.compile(r"\[\[[^\]]*\]\]")
BARE_PIN_RE = re.compile(r"\b(" + ALIAS + r")@(\d+)\b")
SECTION_RE = re.compile(r"^section:([a-z][a-z0-9-]*)$")
# test-side citation in a test name/comment: alias@N with optional #method
TEST_CITE_RE = re.compile(r"\b(" + ALIAS + r")@(\d+)(?:\s*#([a-z][a-z-]*))?")


class MalformedReferenceError(ValueError):
    pass


def scan(text, where=""):
    """Return (refs, holes) in text; raise on malformed [[...]] tokens.

    refs: list of (alias, version|None, span); holes: list of (phrase, was, span).
    """
    refs, holes, claimed = [], [], []
    for m in HOLE_RE.finditer(text):
        holes.append((m.group("phrase"), m.group("was"), m.span()))
        claimed.append(m.span())
    for m in REF_RE.finditer(text):
        refs.append((m.group(1), int(m.group(2)) if m.group(2) else None, m.span()))
        claimed.append(m.span())
    for m in ANY_BRACKET_RE.finditer(text):
        if m.span() not in claimed:
            raise MalformedReferenceError(
                f"{where}: malformed reference {m.group(0)!r}")
    return refs, holes


def normalize(text):
    """Strip pin numbers before hashing, so re-pinning is not a content
    change and the version cascade terminates in one pass (K-17)."""
    text = REF_RE.sub(lambda m: f"[[{m.group(1)}]]", text)
    return BARE_PIN_RE.sub(lambda m: m.group(1), text).strip()


def render_pinned(alias, version):
    return f"[[{alias}@{version}]]"


def repin(text, alias, new_version):
    """Rewrite every pinned reference to alias (bracketed or bare) to
    new_version. Returns (new_text, hits)."""
    hits = 0

    def _brk(m):
        nonlocal hits
        if m.group(1) == alias and m.group(2) is not None:
            hits += 1
            return f"[[{alias}@{new_version}]]"
        return m.group(0)

    def _bare(m):
        nonlocal hits
        if m.group(1) == alias:
            hits += 1
            return f"{alias}@{new_version}"
        return m.group(0)

    text = REF_RE.sub(_brk, text)
    text = BARE_PIN_RE.sub(_bare, text)
    return text, hits
