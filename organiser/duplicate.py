import hashlib
try:
    import pyssdeep
    SSDEEP_AVAILABLE = True
except ImportError:
    SSDEEP_AVAILABLE = False

def sha256_hash(file_path):
    """Return SHA-256 hash of a file."""
    hash_sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()

def ssdeep_hash(file_path):
    """Return ssdeep hash of a file (if available)."""
    if SSDEEP_AVAILABLE:
        return pyssdeep.hash_from_file(file_path)
    else:
        return None

def compare_ssdeep(hash1, hash2):
    """Compare two ssdeep hashes (if available). Returns similarity score (0-100)."""
    if SSDEEP_AVAILABLE:
        return pyssdeep.compare(hash1, hash2)
    else:
        return None
