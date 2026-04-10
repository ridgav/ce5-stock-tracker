import time
import json
import random
from scraper import get_variants, check_stock_fast
from notifier import send

BASE_URL = "https://www.amazon.in/dp/B0FCMLCX46"

# ✅ VALID LINKS INCLUDED
KNOWN_VARIANTS = {
    "Black Infinity 8GB 128GB": "https://www.amazon.in/dp/B0FCMLCX46",
    "Nexus Blue 8GB 128GB": "https://www.amazon.in/dp/B0FC6XHHSV",
    "Marble Mist 8GB 256GB": "https://www.amazon.in/dp/B0FCMKSH2M",
}

STATE_FILE = "state.json"


def load_state():
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except:
        return {}


def save_state(data):
    with open(STATE_FILE, "w") as f:
        json.dump(data, f)


def run():
    state = load_state()
    variants = KNOWN_VARIANTS.copy()

    last_full_scan = 0

    while True:
        now = time.time()

        # 🔥 Detect hidden variants every 5 min
        if now - last_full_scan > 300:
            print("🔄 Scanning hidden variants...")
            try:
                auto_variants = get_variants(BASE_URL)
                variants.update(auto_variants)
            except:
                print("Variant scan failed, using known variants")

            last_full_scan = now

        # ⚡ Check stock every 60 sec
        for name, url in variants.items():
            try:
                in_stock = check_stock_fast(url)
                prev = state.get(url, False)

                if in_stock and not prev:
                    msg = f"🔥 IN STOCK:\n{name}\n{url}"
                    print(msg)
                    send(msg)

                state[url] = in_stock

            except Exception as e:
                print(f"Error: {e}")

        save_state(state)

        sleep_time = 55 + random.randint(0, 15)
        print(f"⏱ Sleeping {sleep_time} sec...\n")
        time.sleep(sleep_time)


if __name__ == "__main__":
    run()
