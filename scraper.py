import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# 🔥 Detect hidden variants (every 5 min)
def get_variants(url):
    variants = {}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(url, timeout=60000)
        page.wait_for_timeout(3000)

        html = page.content()
        soup = BeautifulSoup(html, "html.parser")

        items = soup.select("li[data-asin]")

        for item in items:
            asin = item.get("data-asin")
            text = item.get_text(strip=True)

            if asin and text:
                link = f"https://www.amazon.in/dp/{asin}"
                variants[text] = link

        browser.close()

    return variants


# ⚡ FAST stock check (every 60 sec)
def check_stock_fast(url):
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)

        if "In stock" in res.text:
            return True

        return False

    except:
        return False
