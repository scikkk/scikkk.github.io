import os
import json
import time
import requests
from tqdm import tqdm

url = "https://www.ganvana.com/mall/getGoodsInfo"
"""POST /mall/getGoodsInfo HTTP/1.1,"""
headers = {"Accept": "*/*",
"Accept-Encoding": "gzip, deflate, br, zstd",
"Accept-Language": "zh,zh-CN;q=0.9,en;q=0.8",
"Connection": "keep-alive",
"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
"Cookie": "TouchStone20181129=eyJuaWNrbmFtZSI6InNjaWtrayIsIndobyI6IjE3NDUzOTg1NzI3MDczMGFlMmU0Njc3MzQyYjA5NGNhZmYzMDUyNzU4ZWFiMSIsIl9leHBpcmUiOjE3NDgxODE2MTY4NDIsIl9tYXhBZ2UiOjI1OTIwMDAwMDB9; TouchStone20181129.sig=_SVoewtC3xjDrtyRjmCo2wIhUYo",
"Host": "www.ganvana.com",
"Origin": "https://www.ganvana.com",
"Referer": "https://www.ganvana.com/mall/goods/<|goods_id|>",
"Sec-Fetch-Dest": "empty",
"Sec-Fetch-Mode": "cors",
"Sec-Fetch-Site": "same-origin",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
"X-Requested-With": "XMLHttpRequest",
"sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
"sec-ch-ua-mobile": "?0",
"sec-ch-ua-platform": "Windows"
}
    
MIN_IDX = 152049
MIN_IDX = 152262
MAX_IDX = 152262
dir = "D:/_WangKe/scikkk.github.io/projects/ganvana/mall/getGoodsInfo"
jsonl_file = "D:/_WangKe/scikkk.github.io/projects/ganvana/mall/getGoodsInfo.jsonl"


for idx in tqdm(range(MIN_IDX, MAX_IDX+1), desc="Downloading"):
    data = {"goods_id": str(idx)}
    headers["Referer"] = headers["Referer"].replace("<|goods_id|>", str(idx))
    for _ in range(1):
        try:
            response = requests.post(url, headers=headers, data=data, timeout=60)
            new_line = response.json()
            break
        except:
            print("error:", idx)
            print(response.status_code)
            print(response.text)
            time.sleep(0.1)
            new_line = {"id": idx}
    sub_dir = os.path.join(dir, f"{idx//10000:05d}")
    if not os.path.exists(os.path.join(dir, sub_dir)):
        os.makedirs(os.path.join(dir, sub_dir))
    with open(os.path.join(dir, sub_dir, str(idx)+".json"), "w", encoding="utf-8") as f:
        json.dump(new_line, f, ensure_ascii=False, indent=4)
    with open(jsonl_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(new_line, ensure_ascii=False) + "\n")
    time.sleep(0.1)



def load_jsonl(file_path):
    data = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in tqdm(f, desc="Loading JSONL"):
            if len(line) > 1:
                new_line = json.loads(line)
                data.append(new_line)
    return data
examples = load_jsonl(jsonl_file)
# 根据id去重并排序
examples_dict = {int(item["id"]): item for item in examples}
examples = sorted(examples_dict.values(), key=lambda x: x["id"])
with open(jsonl_file, "w", encoding="utf-8") as f:
    for line in tqdm(examples, desc="Saving mall items"):
        f.write(json.dumps(line, ensure_ascii=False) + "\n")