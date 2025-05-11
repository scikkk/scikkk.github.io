import os
import time
import json
import urllib3
import requests
from tqdm import tqdm
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

MIN_IDX = 42037 # 41929
MAX_IDX = 42137
url = "https://www.ganvana.com/auction/getItem/"
auction_root = "D:/_WangKe/scikkk.github.io/projects/ganvana/auction/getItem"
jsonl_file = "D:/_WangKe/scikkk.github.io/projects/ganvana/auction/getItem.jsonl"



for idx in tqdm(range(MIN_IDX, MAX_IDX+1), desc="Downloading"):
    print("Downloading:", idx)
    for _ in range(3):
        try:
            response = requests.get(url+str(idx), verify=False, timeout=60)
            new_line = response.json()["goods"]
            break
        except:
            print("error:", idx)
            print(response.status_code)
            print(response.text)
            time.sleep(3)
            new_line = {"id": idx}
    if "auction_id" in new_line:
        sub_dir = os.path.join(auction_root, str(new_line["auction_id"]))
        if not os.path.exists(os.path.join(auction_root, sub_dir)):
            os.makedirs(os.path.join(auction_root, sub_dir))
        with open(os.path.join(auction_root, sub_dir, str(idx)+".json"), "w", encoding="utf-8") as f:
            json.dump(new_line, f, ensure_ascii=False, indent=4)
        with open(jsonl_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(new_line, ensure_ascii=False) + "\n")
        time.sleep(0.1)


examples = []
pbar = tqdm(total=0, desc="Loading auction items")
for r, _, f in os.walk(auction_root):
    if "images" in r:
        continue
    for file in f:
        if file.endswith(".json"):
            pbar.update(1)
            file_path = os.path.join(r, file)
            with open(file_path, "r", encoding="utf-8") as f:
                line = json.loads(f.read())
                if len(line) > 1:
                    if not line["winner_price"]:
                        line["winner_price"] = 1
                    examples.append(line)
    

# 根据id去重并排序
examples_dict = {item["id"]: item for item in examples}
examples = sorted(examples_dict.values(), key=lambda x: x["id"])
with open(jsonl_file, "w", encoding="utf-8") as f:
    for line in examples:
        f.write(json.dumps(line, ensure_ascii=False) + "\n")




