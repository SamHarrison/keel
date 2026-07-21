"""What "changed" means (K-17): 16-hex SHA-256 of pin-normalized normative
text. Rationale, witness, tags and pin numbers are deliberately outside the
hash — only the guarantee and its citation *targets* bump the version."""
import hashlib

from . import refs


def content_hash(text):
    return hashlib.sha256(refs.normalize(text).encode("utf-8")).hexdigest()[:16]
