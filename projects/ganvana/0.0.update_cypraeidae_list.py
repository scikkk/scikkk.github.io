import json
import re
from collections import defaultdict
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
auction_data = [{"name": item["goods_name"], "lat_name": item["lat_name"], 'price': item['winner_price'], 'size': item['size']} for item in auction_data if "winner_price" in item and item["winner_price"] and item["winner_price"]>1 and item["goods_name"].strip().endswith("宝螺")]
mall_data = load_jsonl(mall_jsonl_file)
mall_data = [{"name": item["name"], "lat_name": item["lat_name"], 'price': item['price'], 'size': item['size']} for item in mall_data if "price" in item and item["price"] and item["price"]>1 and item["name"].strip().endswith("宝螺")]
name_prices_szies_dict = {}
for item in tqdm(auction_data+mall_data, desc="Loading mall data"):
    item_name = item["name"].replace("cf.", "").replace("aff.", "").strip()
    if not item_name:
        continue
    item_name = item_name.replace("獵帽", "猎帽")
    if len(item_name.split()) > 1 and not any([key in item_name for key in IGNORE_KEYS]):
        if any([item_name.split()[0].endswith(end) for end in SPECICE_ENDS]):
            item_name = item_name.split()[0].strip()
            name_changes.append(f"{item['name']}\t->\t{item_name}")
            # print(name_changes[-1])
        else:
            print(item["name"])
    if item_name not in name_prices_szies_dict:
        name_prices_szies_dict[item_name] = {'prices': [], 'sizes': []}
    name_prices_szies_dict[item_name]['prices'].append(item["price"])
    if not item['size']:
        item['size'] = ''
    sizes = item['size'].lower().replace('about', '').replace('up', '').replace('mm', '')
    if sizes:
        for split_ch in [',', '，', '、', '-', '~', ';', '；']:
            sizes = sizes.replace(split_ch, '|').strip('|')
        for size in sizes.split("|"):
            try:
                name_prices_szies_dict[item_name]['sizes'].append(float(size))
            except:
                pass
                # print(f"Error parsing size for item: {item['name']}: {item['size']}: {sizes}")
print(f"Total name_prices_szies_dict items: {len(name_prices_szies_dict)}")
lat_name_prices_szies_dict = {}
for item in tqdm(auction_data+mall_data, desc="Loading mall data"):
    if not item["lat_name"]:
        continue
    item_name = item["lat_name"].lower()
    item_name = item_name.split('(')[0].split('（')[0].strip()
    item_name = item_name.replace("cf.", "").replace("aff.", "").replace("f.", "")
    item_name = item_name.replace("cf,", "").replace("aff,", "").replace("f,", "")
    item_name = item_name.replace("<span></span>", "").strip().replace(', ', ',').replace('  ', ' ').replace('  ', ' ')
    item_name = item_name.split('lorenz ')[0].split('schilder ')[0]
    item_name = item_name.split('lorenz,')[0].split('schilder,')[0]
    item_name = item_name.split('gray,1')[0].split('rochebrune,1')[0].split('raybaudi,1')[0]
    item_name = item_name.split('titana. & m.')[0].split('melvill,1')[0].split('sullioti,1')[0]
    item_name = item_name.split('dautz &')[0].split('raybaudi,1')[0].split('titana. &')[0]
    item_name = item_name.split('jousseaume,1')[0].split('gmelin,1')[0].split('dautzenberg &')[0]
    item_name = item_name.split('meyer &')[0].split('burgess,1')[0].split('alvarado &')[0]
    item_name = item_name.split('bergonzoni,2')[0].split('perry,1')[0].split('alvarado &')[0]
    if not item_name:
        continue
    if not len(item_name.split()) in [2, 3]:
        # print(f"Invalid lat_name: {item_name}")
        item_name = item_name.split()[:2]
        item_name = ' '.join(item_name)
    if item_name not in lat_name_prices_szies_dict:
        lat_name_prices_szies_dict[item_name] = {'prices': [], 'sizes': []}
    lat_name_prices_szies_dict[item_name]['prices'].append(item["price"])
    if not item['size']:
        item['size'] = ''
    sizes = item['size'].lower().replace('about', '').replace('up', '').replace('mm', '')
    if sizes:
        for split_ch in [',', '，', '、', '-', '~', ';', '；']:
            sizes = sizes.replace(split_ch, '|').strip('|')
        for size in sizes.split("|"):
            try:
                lat_name_prices_szies_dict[item_name]['sizes'].append(float(size))
            except:
                pass
                # print(f"Error parsing size for item: {item['name']}: {item['size']}: {sizes}")
print(f"Total name_prices_szies_dict items: {len(lat_name_prices_szies_dict)}")


# 3. 处理 HTML，插入商城参考价
html_file = "d:/_WangKe/scikkk.github.io/projects/ganvana/Cypraeidae.html"
with open(html_file, encoding="utf-8") as f:
    html = f.read()


def add_price_column_multiline(html):
    lines = html.split("\n")
    new_lines = []
    in_table = False
    td_buffer = []
    tr_start = None
    for idx, line in enumerate(lines):
        # 检查表头，插入表头后面
        if '<td style="font-weight:bold;text-align:center;">参考价</td>' in line:
            in_table = True
            new_lines.append(line)
            continue
        if in_table:
            cur_genus, cur_species = "", ""
            # 记录<tr>开始
            if '<tr' in line:
                tr_start = len(new_lines)
                td_buffer = []
                new_lines.append(line)
                continue
            # 记录</tr>结束
            if '</tr>' in line and tr_start is not None:
                # 处理td_buffer
                assert len(td_buffer) == 7, "td_buffer is \n" + '\n'.join(td_buffer)
                if len(td_buffer)== 7:
                    prices, sizes = [], []
                    price_str, size_str = "", ""
                    genus = re.sub("<.*?>", "", td_buffer[0]).strip()
                    if genus:
                        cur_genus = genus
                    species = re.sub("<.*?>", "", td_buffer[1]).strip()
                    if species:
                        cur_species = species
                    subspecies = re.sub("<.*?>", "", td_buffer[2]).strip()
                    names = re.sub("<.*?>", "", td_buffer[4]).strip().split(";")
                    # print(names)
                    for name in names:
                        name = name.strip()
                        if name in name_prices_szies_dict:
                            # print(f"Found {name} in mall data")
                            prices = name_prices_szies_dict[name]['prices']
                            sizes = name_prices_szies_dict[name]['sizes']
                            break
                    else:
                        lat_name = ''
                        if ' '.join([cur_genus, cur_species, subspecies]).lower in lat_name_prices_szies_dict:
                            lat_name = ' '.join([cur_genus, cur_species, subspecies]).lower()
                        elif cur_species == subspecies and ' '.join([cur_genus, cur_species]).lower() in lat_name_prices_szies_dict:
                            lat_name = ' '.join([cur_genus, cur_species]).lower()
                        if lat_name:
                            # print(f"Found {lat_name} in mall data")
                            prices = lat_name_prices_szies_dict[lat_name]['prices']
                            sizes = lat_name_prices_szies_dict[lat_name]['sizes']
                    if prices:
                        average_mall_price = round(sum(prices) / len(prices), 0)
                        min_mall_price = round(min(prices), 0)
                        max_mall_price = round(max(prices), 0)
                        price_str = f"￥{average_mall_price} ({min_mall_price}~{max_mall_price})"
                    if sizes:
                        average_mall_size = round(sum(sizes) / len(sizes), 1)
                        min_mall_size = round(min(sizes), 1)
                        max_mall_size = round(max(sizes), 1)
                        size_str = f"{average_mall_size}mm ({min_mall_size}~{max_mall_size})"
                    assert subspecies, "td_buffer is \n" + '\n'.join(td_buffer)
                    # print(genus, species, subspecies)
                    # print(price_str)
                    # exit(0)
                    # 在第6个<td>后插入商城参考价
                    insert_idx = tr_start + 6
                    new_lines.insert(insert_idx, f'                                <td style="text-align:center;">{price_str}</td>')
                    # 在第7个<td>后插入商城参考尺寸
                    insert_idx = tr_start + 7
                    new_lines.insert(insert_idx, f'                                <td style="text-align:center;">{size_str}</td>')
                new_lines.append(line)
                tr_start = None
                td_buffer = []
                continue
            # 收集<td>
            if '<td' in line or not line.strip():
                td_buffer.append(line)
            new_lines.append(line)
        else:
            new_lines.append(line)
    return "\n".join(new_lines)

new_html = add_price_column_multiline(html)

with open("d:/_WangKe/scikkk.github.io/projects/ganvana/Cypraeidae_with_price.html", "w", encoding="utf-8") as f:
    f.write(new_html)

