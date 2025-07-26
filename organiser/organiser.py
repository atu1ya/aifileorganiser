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

    # Step 2: AI sorting (optional, group by cluster)
    cluster_to_files = {}
    cluster_to_texts = {}
    file_to_cluster = {}
    if use_ai and AI_DEPENDENCIES_AVAILABLE and text_files:
        embeddings = get_text_embeddings(text_files)
        labels = cluster_embeddings(embeddings, n_clusters=min(5, len(text_files)))
        for idx, label in enumerate(labels):
            file = text_file_paths[idx]
            file_to_cluster[file] = label
            cluster_to_files.setdefault(label, []).append(file)
            cluster_to_texts.setdefault(label, []).append(text_files[idx])

    # Step 3: Move files
    used_files = set()
    # Move AI-clustered files
    if use_ai and AI_DEPENDENCIES_AVAILABLE and cluster_to_files:
        for label, files_in_cluster in cluster_to_files.items():
            texts_in_cluster = cluster_to_texts[label]
            folder_name = generate_folder_name(texts_in_cluster)
            target_folder = os.path.join(destination_folder, folder_name)
            create_folder(target_folder)
            for file in files_in_cluster:
                move_file(file, os.path.join(target_folder, os.path.basename(file)))
                stats.log_file_sorted()
                used_files.add(file)
    # Move remaining files (non-AI or non-text)
    for file in hashes.values():
        if file in used_files:
            continue
        folder_name = get_human_readable_folder(file)
        target_folder = os.path.join(destination_folder, folder_name)
        create_folder(target_folder)
        move_file(file, os.path.join(target_folder, os.path.basename(file)))
        stats.log_file_sorted()

    return stats.get_stats()
