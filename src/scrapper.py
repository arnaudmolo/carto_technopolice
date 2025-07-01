import pandas as pd
from urllib.parse import urlparse
from readability import Document
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


def is_valid_url(url):
    try:
        result = urlparse(url)
        return all(
            [
                result.scheme,
                result.netloc,
                not url.lower().endswith(".pdf"),
                "telecharger" not in url.lower(),
            ]
        )
    except:
        return False


def fetch_content(url):
    if not is_valid_url(url):
        print(f"Invalid or blocked URL: {url}")
        return None

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        content_type_container = {}

        def handle_response(response):
            if response.url == url:
                content_type = response.headers.get("content-type", "")
                content_type_container["value"] = content_type

        page.on("response", handle_response)

        try:
            page.goto(url, timeout=60000, wait_until="networkidle")
            content_type = content_type_container.get("value", "")
            if content_type.startswith("application/pdf"):
                print(f"pdf: {content_type} at {url}")
                return None

            html = page.content()
        except Exception as e:
            print(f"Failed to fetch {url}: {e}")
            return None
        finally:
            browser.close()

        doc = Document(html)
        summary_html = doc.summary()
        text = BeautifulSoup(summary_html, "html.parser").get_text()
        return text.strip()


df = pd.read_csv("../data/edges.csv")

urls = df["url"].to_list()
contents = [fetch_content(url) for url in urls]
df["content"] = contents

df.to_csv("../data/contents.csv")
