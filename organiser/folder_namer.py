def generate_folder_name(cluster_texts, model="llama3"):
    """Generate a human-readable folder name using local LLM (Ollama)."""
    try:
        import ollama
        prompt = (
            "Given the following file summaries, suggest a short, human-readable folder name "
            "(max 3 words, no punctuation, no quotes, no special characters, no numbers):\n"
            + "\n".join(cluster_texts)
        )
        response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
        folder_name = response['message']['content'].strip().split('\n')[0]
        # Clean up folder name: remove unwanted characters
        folder_name = folder_name.replace('"', '').replace("'", '').replace("/", '').replace("\\", '').strip()
        print("\n[SUMMARY] Folder Naming Preview:")
        print("  Cluster texts:")
        for t in cluster_texts:
            print(f"    - {t}")
        print(f"  Suggested folder name: {folder_name}\n")
        if not folder_name:
            raise ValueError("Empty folder name from LLM")
        print(f"[INFO] LLM folder name: {folder_name}")
        return folder_name
    except Exception as e:
        print(f"[INFO] LLM folder naming failed ({e}). Using default name.")
        return "AI_Sorted_Folder"
