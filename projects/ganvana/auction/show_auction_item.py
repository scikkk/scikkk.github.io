import os
import time
import json
import urllib3
import requests
from tqdm import tqdm
import shutil
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


url = "https://www.ganvana.com/auction/getItem/"
dir = "D:/_WangKe/scikkk.github.io/projects/ganvana/auction/getItem"
jsonl_file = "D:/_WangKe/scikkk.github.io/projects/ganvana/auction/getItem.jsonl"

# get last idx
with open(jsonl_file, "r", encoding="utf-8") as f:
    last_idx = json.loads(f.readlines()[-1])["id"]
    print("last idx:", last_idx)

    
for r, _, f in os.walk(dir):
    for file in f:
        if file.endswith(".json"):
            with open(os.path.join(r, file), "r", encoding="utf-8") as f:
                line = json.loads(f.read())
                file_path = os.path.join(r, file)
                # print(file_path)
                # print(file_path.split("\\")[-2])
                if len(file_path.split("\\")[-2]) == 5:
                    if "auction_id" not in line:
                        print(json.dumps(line, ensure_ascii=False, indent=4))
                        print("no auction_id:", file_path)
                        continue 
                    new_file_path = os.path.join(dir, str(line["auction_id"]), file)
                    if not os.path.exists(os.path.join(dir, str(line["auction_id"]))):
                        os.makedirs(os.path.join(dir, str(line["auction_id"])))
                    print(file_path, new_file_path)
                    shutil.copy2(file_path, new_file_path)
                    # os.remove(file_path)