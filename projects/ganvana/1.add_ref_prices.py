import os
import time
import json
import urllib3
import requests
from tqdm import tqdm


auction_jsonl_file = "D:/_WangKe/scikkk.github.io/projects/ganvana/auction/getItem.jsonl"
mall_jsonl_file = "D:/_WangKe/scikkk.github.io/projects/ganvana/mall/getGoodsInfo.jsonl"
name_changes_file = "D:/_WangKe/scikkk.github.io/projects/ganvana/auction/name_changes.txt"

def load_jsonl(file_path):
    data = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in tqdm(f, desc="Loading JSONL"):
            if len(line) > 1:
                new_line = json.loads(line)
                data.append(new_line)
    return data

SPECICE_ENDS = ["螺", "蛤", "贝", "鲍", "蜗牛", "涡牛", "蛸", "蚶", "蚌", "蛎", "蜊", "海胆", "蜷", "乌贼", "蛏", "蚬", "动物", "鱼"]
IGNORE_KEYS = ["+", "x", "×"]

name_changes = []
auction_data = load_jsonl(auction_jsonl_file)
mall_data = load_jsonl(mall_jsonl_file)
mall_data_dict = {}
for item in tqdm(mall_data, desc="Loading mall data"):
    if "name" in item:
        item_name = item["name"].replace("cf.", "").replace("aff.", "").strip()
        if not item_name:
            continue
        if len(item_name.split()) > 1 and not any([key in item_name for key in IGNORE_KEYS]):
            if any([item_name.split()[0].endswith(end) for end in SPECICE_ENDS]):
                item_name = item_name.split()[0].strip()
                name_changes.append(f"{item['name']}\t->\t{item_name}")
                # print(name_changes[-1])
            else:
                print(item["name"])
        if item_name not in mall_data_dict:
            mall_data_dict[item_name] = {'prices': [], 'usd_prices': [], 'sizes': []}
        mall_data_dict[item_name]['prices'].append(item["price"])
        mall_data_dict[item_name]['usd_prices'].append(item["usd_price"])
        sizes = item['size'].lower().replace('about', '').replace('up', '').replace('mm', '')
        if sizes and 'micro' not in sizes and 'small' not in sizes:
            try:
                for split_ch in [',', '，', '、', '-', '~', ';', '；']:
                    sizes = sizes.replace(split_ch, '|').strip('|')
                for size in sizes.split("|"):
                    mall_data_dict[item_name]['sizes'].append(float(size))
            except:
                print(f"Error parsing size for item: {item['name']}: {item['size']}: {sizes}")
        else:
            mall_data_dict[item_name]['sizes'].append(sizes)

for item in tqdm(mall_data, desc="Adding mall prices"):
    if "name" in item:
        item_name = item["name"].replace("cf.", "").replace("aff.", "").strip()
        if not item_name:
            continue
        if len(item_name.split()) > 1 and not any([key in item_name for key in IGNORE_KEYS]):
            if any([item_name.split()[0].endswith(end) for end in SPECICE_ENDS]):
                item_name = item_name.split()[0].strip()
                name_changes.append(f"{item['name']}\t->\t{item_name}")
                # print(name_changes[-1])
            else:
                print(item["name"])
        if item_name and item_name in mall_data_dict:
            item["num"] = len(mall_data_dict[item_name]['prices'])
            item["average_mall_price"] = round(sum(mall_data_dict[item_name]['prices']) / len(mall_data_dict[item_name]['prices']), 0)
            item["min_mall_price"] = round(min(mall_data_dict[item_name]['prices']), 0)
            item["max_mall_price"] = round(max(mall_data_dict[item_name]['prices']), 0)
            item["average_mall_usd_price"] = round(sum(mall_data_dict[item_name]['usd_prices']) / len(mall_data_dict[item_name]['usd_prices']), 0)
            item["min_mall_usd_price"] = round(min(mall_data_dict[item_name]['usd_prices']), 0)
            item["max_mall_usd_price"] = round(max(mall_data_dict[item_name]['usd_prices']), 0)
            try:
                item["average_mall_size"] = round(sum(mall_data_dict[item_name]['sizes']) / len(mall_data_dict[item_name]['sizes']), 1)
                item["min_mall_size"] = round(min(mall_data_dict[item_name]['sizes']), 1)
                item["max_mall_size"] = round(max(mall_data_dict[item_name]['sizes']), 1)
            except:
                item["average_mall_size"] = max(set(mall_data_dict[item_name]['sizes']), key=mall_data_dict[item_name]['sizes'].count)
print("Saving mall data...")
with open(mall_jsonl_file, "w", encoding="utf-8") as f:
    # 根据id去重并排序
    data_dict = {item["id"]: item for item in mall_data}
    data = sorted(data_dict.values(), key=lambda x: x["id"])
    last_idx = data[-1]["id"] if data else 0
    for line in data:
        f.write(json.dumps(line, ensure_ascii=False) + "\n")

for item in tqdm(auction_data, desc="Adding mall prices"):
    if item["family"] == "艺术":
        continue
    item_name = item["goods_name"].replace("cf.", "").replace("aff.", "").strip()
    if len(item_name.split()) > 1 and not any([key in item_name for key in IGNORE_KEYS]):
        if any([item_name.split()[0].endswith(end) for end in SPECICE_ENDS]):
            item_name = item_name.split()[0].strip()
            name_changes.append(f"{item['goods_name']}\t->\t{item_name}")
            # print(name_changes[-1])
        else:
            print(item["goods_name"])
    if item_name and item_name in mall_data_dict:
        item["mall_num"] = len(mall_data_dict[item_name]['prices'])
        item["average_mall_price"] = round(sum(mall_data_dict[item_name]['prices']) / len(mall_data_dict[item_name]['prices']), 0)
        item["min_mall_price"] = round(min(mall_data_dict[item_name]['prices']), 0)
        item["max_mall_price"] = round(max(mall_data_dict[item_name]['prices']), 0)
        item["average_mall_usd_price"] = round(sum(mall_data_dict[item_name]['usd_prices']) / len(mall_data_dict[item_name]['usd_prices']), 0)
        item["min_mall_usd_price"] = round(min(mall_data_dict[item_name]['usd_prices']), 0)
        item["max_mall_usd_price"] = round(max(mall_data_dict[item_name]['usd_prices']), 0)
        try:
            item["average_mall_size"] = round(sum(mall_data_dict[item_name]['sizes']) / len(mall_data_dict[item_name]['sizes']), 1)
            item["min_mall_size"] = round(min(mall_data_dict[item_name]['sizes']), 1)
            item["max_mall_size"] = round(max(mall_data_dict[item_name]['sizes']), 1)
        except:
            item["average_mall_size"] = max(set(mall_data_dict[item_name]['sizes']), key=mall_data_dict[item_name]['sizes'].count)
print("Saving auction data...")
with open(auction_jsonl_file, "w", encoding="utf-8") as f:
    # 根据id去重并排序
    data_dict = {item["id"]: item for item in auction_data}
    data = sorted(data_dict.values(), key=lambda x: x["id"])
    last_idx = data[-1]["id"] if data else 0
    for line in data:
        f.write(json.dumps(line, ensure_ascii=False) + "\n")

sorted_name_changes = sorted(name_changes, key=lambda x: x.split("\t->\t")[0])
with open(name_changes_file, "w", encoding="utf-8") as f:
    for line in sorted_name_changes:
        f.write(line + "\n")

import gzip
import shutil
print("Compressing auction JSONL files...")
auction_jsonl_file = "D:/_WangKe/scikkk.github.io/projects/ganvana/auction/getItem.jsonl"
with open(auction_jsonl_file, 'rb') as f_in, gzip.open(auction_jsonl_file.replace('.jsonl', '.jsonl.gz'), 'wb') as f_out:
    shutil.copyfileobj(f_in, f_out)
print("Compressing mall JSONL files...")
mall_jsonl_file = "D:/_WangKe/scikkk.github.io/projects/ganvana/mall/getGoodsInfo.jsonl"
with open(mall_jsonl_file, 'rb') as f_in, gzip.open(mall_jsonl_file.replace('.jsonl', '.jsonl.gz'), 'wb') as f_out:
    shutil.copyfileobj(f_in, f_out)