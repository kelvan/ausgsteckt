import requests


def fetch_wikipedia_data(page_title: str, lang: str) -> tuple[str, list[str]]:
    base_url = f"https://{lang}.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "titles": page_title,
        "prop": "extracts|images",
        "exintro": True,
        "explaintext": True,
        "imlimit": 50,
        "format": "json",
    }
    resp = requests.get(base_url, params=params, timeout=10)
    resp.raise_for_status()
    pages = resp.json()["query"]["pages"]
    page = next(iter(pages.values()))
    summary = page.get("extract", "").strip()
    images = [img["title"].replace("File:", "") for img in page.get("images", [])]
    return summary, images
