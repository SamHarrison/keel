"""Quality lints for changed-vs-corpus severity scoping (K-19), per
ISO 29148 §5.2.5–5.2.7 and the arkhive adversarial-writing harvest
(consolidation plan §2.4, §4a).

Language stance is the standard's, not BCP 14: requirements use 'shall'
(§5.2.7 warns *against* 'must'); 'will' states fact, 'should' preference,
'may' allowance — none of them binding. Negation binds to the modal
("X shall not …"), never the subject ("no X shall …") — the construction
that silently inverted five arkhive requirements.
"""
import re

SHALL_RE = re.compile(r"\bshall\b", re.I)
NON_BINDING_RE = re.compile(r"\b(should|may|will|must)\b", re.I)
INVERSION_RE = re.compile(r"\bno\s+(?:\w+\s+){0,4}?shall\b", re.I)
ABLE_TO_RE = re.compile(r"\bshall\s+be\s+able\s+to\b", re.I)
CODE_CLAIM_RE = re.compile(
    r"\b(currently|previously|used to|the old|as implemented|regression|"
    r"the code (now|already))\b", re.I)
PLACEHOLDER_RE = re.compile(r"<[a-z][^>]*>")


def compile_denylist(deny):
    """[(category, term, regex)] with word boundaries — 'must' must not
    match 'mustard'. An entry may be a plain string or
    {term: ..., unless_preceded_by: [words]} for precise-usage exceptions
    ('at most 200 MB' is a bound, not a superlative)."""
    out = []
    for cat, terms in (deny or {}).items():
        for t in terms or []:
            unless = []
            if isinstance(t, dict):
                unless = t.get("unless_preceded_by") or []
                t = t.get("term", "")
            t = t.strip()
            if not t:
                continue
            guard = "".join(r"(?<!\b" + re.escape(u) + r"\s)" for u in unless)
            out.append((cat, t, re.compile(guard + r"(?<![\w-])" +
                                           re.escape(t) + r"(?![\w-])", re.I)))
    return out


def check_row(kind, row, denylist):
    """Return [(code, message)] findings for one authored row.
    kind: prd | brd | stakeholder | constraint."""
    out = []
    text = row.get("text") or row.get("statement") or ""
    if PLACEHOLDER_RE.search(text):
        return out  # template placeholder rows lint clean by design
    rationale = row.get("rationale") or ""
    is_def = row.get("type") == "definition"
    if kind == "prd" and not is_def:
        if not SHALL_RE.search(text):
            out.append(("shall-missing", "requirement text has no 'shall'"))
        for m in NON_BINDING_RE.finditer(text):
            w = m.group(1).lower()
            hint = {"must": "use 'shall' (ISO 29148 §5.2.7 warns against 'must')",
                    "should": "'should' is a preference, not a requirement",
                    "may": "'may' is an allowance, not a requirement",
                    "will": "'will' states fact, not obligation"}[w]
            out.append(("non-binding-modal", f"'{w}' in requirement text — {hint}"))
        if INVERSION_RE.search(text):
            out.append(("subject-negation",
                        "negate the modal ('X shall not …'), never the "
                        "subject ('no X shall …')"))
        if ABLE_TO_RE.search(text):
            out.append(("able-to", "'shall be able to' is unverifiable — "
                        "state the behaviour itself (§5.2.7)"))
    if is_def and SHALL_RE.search(text):
        out.append(("keyword-in-definition",
                    "definitions are declarative rows, never shall-statements"))
    if kind == "brd" and SHALL_RE.search(text):
        out.append(("shall-in-brd", "BRD rows are outcome-shaped, not "
                    "shall-form — the obligation belongs in the PRD"))
    if kind == "prd":
        for cat, term, rx in denylist:
            if rx.search(text):
                out.append((f"denylist-{cat}", f"vague term '{term}'"))
    if SHALL_RE.search(rationale):
        out.append(("keyword-in-rationale",
                    "a guarantee is hiding in the rationale — move it to text"))
    if CODE_CLAIM_RE.search(rationale):
        out.append(("code-claim-in-rationale",
                    "rationale is timeless intent — never a claim about the "
                    "code or its history"))
    return out
