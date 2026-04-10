import os
import sys
import requests
import json
import pendulum
from pathlib import Path

from vietlott.config.map_class import map_class_name
from vietlott.config.products import product_config_map

WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
SECRET_TOKEN = os.environ.get("SECRET_TOKEN")

def main():
    print(f"DEBUG: WEBHOOK_URL exists = {'WEBHOOK_URL' in os.environ}, length = {len(WEBHOOK_URL) if WEBHOOK_URL else 0}")
    if not WEBHOOK_URL:
        print("❌ LỖI: Chưa cấu hình WEBHOOK_URL")
        sys.exit(1)

    products = ["keno", "bingo18", "power_655", "power_645", "power_535", "3d", "3d_pro"]

    run_date = pendulum.now(tz="Asia/Ho_Chi_Minh").to_date_string()
    errors = []

    for product in products:
        print(f"--- Checking game: {product} ---")
        cfg = product_config_map[product]

        if cfg.raw_path.exists():
            cfg.raw_path.unlink()

        crawler_obj = map_class_name[product]()

        try:
            crawler_obj.crawl(run_date_str=run_date, index_from=0, index_to=1)

            if cfg.raw_path.exists():
                with open(cfg.raw_path, 'r', encoding='utf-8') as f:
                    records = [json.loads(line.strip()) for line in f if line.strip()]

                if records:
                    payload = {
                        "secret": SECRET_TOKEN,
                        "game": product,
                        "data": records
                    }

                    res = requests.post(WEBHOOK_URL, json=payload, timeout=15)
                    res.raise_for_status()
                    print(f"✅ OK {len(records)} records - status: {res.status_code}")
                else:
                    print("⚠️ Không có data mới.")
        except Exception as e:
            print(f"❌ Lỗi khi đồng bộ {product}: {e}")
            errors.append(product)

    if errors:
        print(f"\n❌ Có {len(errors)} game bị lỗi: {', '.join(errors)}")
        sys.exit(1)

    print("\n✅ Hoàn tất tất cả game.")

if __name__ == "__main__":
    main()
