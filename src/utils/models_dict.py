from huggingface_hub import list_repo_files

llm_models_dict = {
    "Mistral-7B": {
        "repo_name": "TheBloke/Mistral-7B-v0.1-GGUF",
        "variants": [variant_name for variant_name in list_repo_files("TheBloke/Mistral-7B-v0.1-GGUF") if ".gguf" in variant_name],
        "chat_format": "mistrallite"
    },
    "Mistral-7B-Instruct": {
        "repo_name": "TheBloke/Mistral-7B-Instruct-v0.1-GGUF",
        "variants": [variant_name for variant_name in list_repo_files("TheBloke/Mistral-7B-Instruct-v0.1-GGUF") if ".gguf" in variant_name],
        "chat_format": "llama-2"
    },
    "Llama-2-7B-Chat": {
        "repo_name": "TheBloke/Llama-2-7B-Chat-GGUF",
        "variants": [variant_name for variant_name in list_repo_files("TheBloke/Llama-2-7B-Chat-GGUF") if ".gguf" in variant_name],
        "chat_format": "llama-2"
    },
    "Mistral-7B-OpenOrca": {
        "repo_name": "TheBloke/Mistral-7B-OpenOrca-GGUF",
        "variants": [variant_name for variant_name in list_repo_files("TheBloke/Mistral-7B-OpenOrca-GGUF") if ".gguf" in variant_name],
        "chat_format": "chatml"
    },
    "Chupacabra-7B-V3": {
        "repo_name": "TheBloke/Chupacabra-7B-v3-GGUF",
        "variants": [variant_name for variant_name in list_repo_files("TheBloke/Chupacabra-7B-v3-GGUF") if ".gguf" in variant_name],
        "chat_format": "alpaca"
    },
    "CodeLlama-7B-Instruct": {
        "repo_name": "TheBloke/CodeLlama-7B-Instruct-GGUF",
        "variants": [variant_name for variant_name in list_repo_files("TheBloke/CodeLlama-7B-Instruct-GGUF") if ".gguf" in variant_name],
        "chat_format": "llama-2"
    },
    "Zephyr-7B-Alpha": {
        "repo_name": "TheBloke/zephyr-7B-alpha-GGUF",
        "variants": [variant_name for variant_name in list_repo_files("TheBloke/zephyr-7B-alpha-GGUF") if ".gguf" in variant_name],
        "chat_format": "zephyr"
    },
}