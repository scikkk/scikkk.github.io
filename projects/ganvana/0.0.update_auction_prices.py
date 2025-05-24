import json
import gzip
import shutil
import urllib3
import requests
from tqdm import tqdm
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



auction_jsonl_file = "D:/_WangKe/scikkk.github.io/projects/ganvana/auction/getItem.jsonl"
auction_data = []
with open(auction_jsonl_file, "r", encoding="utf-8") as f:
    for line in tqdm(f, desc="Loading auction JSONL"):
        if len(line) > 1:
            new_line = json.loads(line)
            auction_data.append(new_line)
auction_data_dict = {int(item["id"]): item for item in auction_data}

response = requests.get("https://ganvana.com/auction/getList", verify=False, timeout=60)
print(response.json())

for item in response.json()["list"]:
    if "id" in item and item["id"] in auction_data_dict:
        print(f"Updating item {item['id']}:{item['goods_name']}: {auction_data_dict[item['id']]['winner_price']} --> {item['winner_price']}")
        auction_data_dict[item["id"]]["winner_price"] = item["winner_price"]


# 根据id去重并排序
auction_data = sorted(auction_data_dict.values(), key=lambda x: x["id"])
with open(auction_jsonl_file, "w", encoding="utf-8") as f:
    for line in tqdm(auction_data, desc="Saving auction items"):
        f.write(json.dumps(line, ensure_ascii=False) + "\n")

print("Compressing auction JSONL files...")
with open(auction_jsonl_file, 'rb') as f_in, gzip.open(auction_jsonl_file.replace('.jsonl', '.jsonl.gz'), 'wb') as f_out:
    shutil.copyfileobj(f_in, f_out)