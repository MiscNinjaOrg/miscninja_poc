from huggingface_hub import snapshot_download
import sys

if __name__ == "__main__":
    snapshot_download(sys.argv[1])