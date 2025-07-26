from organiser.file_ops import list_files, create_folder, move_file, get_human_readable_folder
from organiser.duplicate import sha256_hash, ssdeep_hash
from organiser.ai_sort import get_text_embeddings, cluster_embeddings, AI_DEPENDENCIES_AVAILABLE
from organiser.folder_namer import generate_folder_name
from organiser.log import Stats
import os

# Main organiser workflow

def organise_files(source_folder, destination_folder, use_ai=False):
    stats = Stats()
    files = list_files(source_folder)
    hashes = {}
    ssdeep_hashes = {}
    clusters = None
    cluster_map = {}
    text_files = []
    text_file_paths = []

    # Step 1: Detect duplicates (SHA-256, then fuzzy via ssdeep if available)
    from organiser.duplicate import compare_ssdeep, SSDEEP_AVAILABLE
    FUZZY_THRESHOLD = 90  # similarity score (0-100)
    for file in files:
        h = sha256_hash(file)
        if h in hashes:
            stats.log_duplicate_detected()
            continue  # Skip duplicate
        # Fuzzy duplicate detection (optional, only if not SHA-256 duplicate)
        is_fuzzy_duplicate = False
        if SSDEEP_AVAILABLE:
            s_hash = ssdeep_hash(file)
            for prev_file, prev_s_hash in ssdeep_hashes.items():
                if prev_s_hash and s_hash:
                    score = compare_ssdeep(s_hash, prev_s_hash)
                    if score is not None and score >= FUZZY_THRESHOLD:
                        stats.log_duplicate_detected()
                        is_fuzzy_duplicate = True
                        break
            if is_fuzzy_duplicate:
                continue  # Skip fuzzy duplicate
            ssdeep_hashes[file] = s_hash
        hashes[h] = file
        # Collect text files for AI sorting
        if os.path.splitext(file)[1].lower() in ['.txt', '.md', '.doc', '.docx', '.pdf']:
            try:
                with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                    text_files.append(f.read())
                    text_file_paths.append(file)
            except Exception as e:
                # Log skipped file for debugging
                print(f"[DEBUG] Skipped non-text file: {file} ({e})")

    # Step 2: AI sorting (optional)
    if use_ai and AI_DEPENDENCIES_AVAILABLE and text_files:
        embeddings = get_text_embeddings(text_files)
        labels = cluster_embeddings(embeddings, n_clusters=min(5, len(text_files)))
        for idx, label in enumerate(labels):
            cluster_map[text_file_paths[idx]] = label

    # Step 3: Move files
    for file in hashes.values():
        if use_ai and file in cluster_map:
            folder_name = generate_folder_name([file]) + f"_{cluster_map[file]}"
        else:
            folder_name = get_human_readable_folder(file)
        target_folder = os.path.join(destination_folder, folder_name)
        create_folder(target_folder)
        move_file(file, os.path.join(target_folder, os.path.basename(file)))
        stats.log_file_sorted()

    return stats.get_stats()
