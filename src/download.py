import urllib.request
import shutil
import os
from tqdm import tqdm


SEMANTIC_SCHOLAR_URL = 'https://s3-us-west-2.amazonaws.com/ai2-s2-research-public/open-corpus/2021-04-01/'


def download_semantic_scholar_if_needed(semantic_scholar_path: str,
                                        default_count: int = 181) -> None:
    """
    Helper file for match semantic scholar. Downloads the whole corpus.
    """
    if not os.path.exists(semantic_scholar_path):
        os.makedirs(semantic_scholar_path)
        with urllib.request.urlopen(SEMANTIC_SCHOLAR_URL + "manifest.txt") as response:
            with open(semantic_scholar_path + "manifest.txt", 'wb') as fh:
                shutil.copyfileobj(response, fh)
        with open(semantic_scholar_path + "/manifest.txt", "r") as f:
            for line in tqdm(f, total=default_count):
                line = line.strip()
                with urllib.request.urlopen(SEMANTIC_SCHOLAR_URL + line) as response:
                    with open(semantic_scholar_path + line, 'wb') as fh:
                        shutil.copyfileobj(response, fh)


if __name__ == "__main__":
    download_semantic_scholar_if_needed("data/semantic_scholar/")
