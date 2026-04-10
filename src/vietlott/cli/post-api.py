import os
import requests
import json
import pendulum
from pathlib import Path

from vietlott.config.map_class import map_class_name
from vietlott.config.products import product_config_map

WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
SECRET_TOKEN = os.environ.get("SECRET_TOKEN")

def main():
    if not WEBHOOK_URL:
        print("CẢNH BÁO: Chưa cấu hình WEBHOOK_URL")
        return

    products = ["keno", "bingo18", "power_655", "power_645", "power_535", "3d", "3d_pro"]
    
    run_date = pendulum.now(tz="Asia/Ho_Chi_Minh").to_date_string()
    
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
                    print(f"✅ OK {len(records)} records - status: {res.status_code}")
                else:
                    print("⚠️ Không có data mới.")
        except Exception as e:
            print(f"❌ Lỗi khi đồng bộ {product}: {e}")

if __name__ == "__main__":
    main()
