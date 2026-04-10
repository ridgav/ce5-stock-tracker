import time
import json
import random
from scraper import get_variants, check_stock_fast
from notifier import send

# 🔗 Base URL (main entry)
BASE_URL = "https://www.amazon.in/dp/B0FCMLCX46"

# ✅ ONLY VALID VERIFIED LINKS
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
    print("🚀 BOT STARTED\n")

    state = load_state()

    # ✅ Start with valid variants (fixes your issue)
    variants = KNOWN_VARIANTS.copy()

    last_full_scan = 0

    while True:
        now = time.time()

        # 🔄 Try detecting hidden variants every 5 min
        if now - last_full_scan > 300:
            print("🔄 Scanning hidden variants...")

            try:
                auto_variants = get_variants(BASE_URL)

                if auto_variants:
                    variants.update(auto_variants)
                    print(f"✅ Added {len(auto_variants)} detected variants")
                else:
                    print("⚠️ No hidden variants found")

            except Exception as e:
                print(f"❌ Scan error: {e}")

            # 🧾 Show all variants
            print("\n📦 Tracking variants:")
            for name, url in variants.items():
                print(f"{name} → {url}")

            last_full_scan = now

        # ⚡ Stock check
        print("\n🔍 Checking stock...")

        for name, url in variants.items():
            try:
                in_stock = check_stock_fast(url)
                prev = state.get(url, False)

                print(f"{name}: {'✅ IN STOCK' if in_stock else '❌ Out of stock'}")

                # 🔔 Alert only when stock appears
                if in_stock and not prev:
                    msg = f"🔥 IN STOCK:\n{name}\n{url}"
                    send(msg)
                    print("🚨 ALERT SENT!")

                state[url] = in_stock

            except Exception as e:
                print(f"❌ Error: {e}")

        save_state(state)

        sleep_time = 55 + random.randint(0, 15)
        print(f"\n⏱ Sleeping {sleep_time} sec...\n")
        time.sleep(sleep_time)


if __name__ == "__main__":
    run()
