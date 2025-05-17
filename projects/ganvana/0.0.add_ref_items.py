import os
import time
import json
import shutil
from tqdm import tqdm

def load_jsonl(file_path):
    data = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in tqdm(f, desc="Loading JSONL"):
            if len(line) > 1:
                new_line = json.loads(line)
                data.append(new_line)
    return data

name_items = {}
auction_jsonl_file = "D:/_WangKe/scikkk.github.io/projects/ganvana/auction/getItem.jsonl"
auction_data = load_jsonl(auction_jsonl_file)
for item in tqdm(auction_data, desc="Adding auction prices"):
    if item['lat_name']:
        item['lat_name'] = item['lat_name'].split('(')[0].split('（')[0].strip()
    if item['lat_name'] not in name_items:
        name_items[item['lat_name']] = item
    elif item['winner_price'] > name_items[item['lat_name']]['winner_price']:
        name_items[item['lat_name']] = item
mall_jsonl_file = "D:/_WangKe/scikkk.github.io/projects/ganvana/mall/getGoodsInfo.jsonl"
mall_data = load_jsonl(mall_jsonl_file)
for item in tqdm(mall_data, desc="Adding mall prices"):
    if len(item) < 3:
        continue
    item['lat_name'] = item['lat_name'].split('(')[0].split('（')[0].strip()
    new_item = {
        'id': item['id'],
        'auction_id': -1,
        'status': item['tag'],
        'family': item['cate_name'], 
        'lat_family': item['cate_lat_name'] if item['cate_lat_name'] else '',
        'goods_name': item['name'],
        'lat_name': item['lat_name'],
        'author': item['author'],
        'goods_sn': item['sn'],
        'thumb': item['thumb'],
        'thumb_big': item['thumb_big'],
        'size': item['size'],
        'product_area': item['area'],
        'desc': '\n'.join([item['condition'], item['desc'], item['descEn'], item['content']]).strip(),
        'more_img': [],
        'bid_time': 1,
        'created_at': item['created_at'],
        'winner_who': '',
        'winner_price': item['price'],
        'winner_nickname': '',
        'winner_headimg': '',
        'winner_rec_id': 0
    }
    if new_item['lat_name'] not in name_items:
        name_items[new_item['lat_name']] = new_item
    elif new_item['winner_price'] > name_items[new_item['lat_name']]['winner_price']:
        name_items[new_item['lat_name']] = new_item



most_expensive_items = []
for item in tqdm(name_items.values(), desc="Cleaning items"):
    if not any(key in item['goods_name'] for key in ["坚螺", "巴蜗牛", "榧螺", "涡螺", "凤凰螺", "海扇蛤", "法螺", "骨螺", "芋螺", "宝螺", "谷米螺"]):
        continue
    if item['family'] == '艺术' or item['family'] == '书籍'  or item['family'] == '书' or item['family'] == '图书' or item['family'] == 'Art' or item['lat_family'] == 'Art':
        continue
    if item['family'] in ['综合标本', 'test', '1', '钟螺科1']:
        continue
    if item['goods_name'] =="海滩冲积样本":
        continue
    if item['lat_family']:
        item['lat_family'] = item['lat_family'].replace('\\r', '').replace('\\n', '').replace('<br/><br/>', '').strip()
        if any([e in item['lat_family'] for e in ['-', '+', 'x', '×', '，', '、', '；', ';']]):
            continue
    else:
        item['lat_family'] = "unknown"
    if item['family']:
        item['family'] = item['family'].split('（')[0].split('(')[0].strip()
        item['family'] = item['family'].replace('\\r', '').replace('\\n', '').replace('<br/><br/>', '').strip()
    else:
        item['family'] = "unknown"
    most_expensive_items.append(item)

# deduplicate items by goods_name
most_expensive_items_dict = {}
for item in most_expensive_items:
    if item['goods_name'] not in most_expensive_items_dict:
        most_expensive_items_dict[item['goods_name']] = item
    else:
        if item['winner_price'] > most_expensive_items_dict[item['goods_name']]['winner_price']:
            most_expensive_items_dict[item['goods_name']] = item
most_expensive_items = list(most_expensive_items_dict.values())


family_names = []
for family_item in json.loads(open("D:/_WangKe/scikkk.github.io/projects/ganvana/tags_cate1_cate2.json", "r", encoding="utf-8").read())["cate2List"]:
    family_name = family_item['name'].strip('科').strip()
    family_lat_name = family_item['lat_name'].lower().strip()
    family_names.append((family_name, family_lat_name))
family_names = sorted(family_names, key=lambda x: len(x[0]), reverse=True)
family_items = {}
for item in tqdm(most_expensive_items, desc="Categorizing items"):
    cur_family = "unknown"
    for family_name, family_lat_name in family_names:
        if family_name in item['goods_name'].strip() or family_name in item['family']:
            cur_family = family_name
            break
    if cur_family not in family_items:
        family_items[cur_family] = []
    family_items[cur_family].append(item)

dir_path = "D:/_WangKe/scikkk.github.io/projects/ganvana/auction/getItem/-1"
for subdir in tqdm(os.listdir(dir_path), desc="Clearing directory"):
    subdir_path = os.path.join(dir_path, subdir)
    if os.path.isdir(subdir_path):
        shutil.rmtree(subdir_path)

idx = 100000
for family, items in tqdm(family_items.items(), desc="Saving familys"):
    family_dir = os.path.join(dir_path, f"{family}科_{len(items)}")
    if not os.path.exists(family_dir):
        os.makedirs(family_dir)
    for item in tqdm(items, desc="Saving items", total=len(items), leave=False):
        item["id"] = idx
        item["auction_id"] = -1
        try:
            file_path = os.path.join(family_dir, str(item['id'])+".json")
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(item, f, ensure_ascii=False, indent=4)
            idx += 1
        except:
            print(json.dumps(item, ensure_ascii=False, indent=4))