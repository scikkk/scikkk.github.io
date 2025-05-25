import os
import time
import json
import urllib3
import requests
from tqdm import tqdm
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

MIN_IDX = 42277
MAX_IDX = 42398 # 42472
MAX_IDX = MIN_IDX
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
        if not os.path.exists(sub_dir):
            os.makedirs(sub_dir)
        with open(os.path.join(sub_dir, str(idx)+".json"), "w", encoding="utf-8") as f:
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
                if os.path.exists(file_path.replace("getItem", "item")):
                    with open(file_path.replace("getItem", "item"), "r", encoding="utf-8") as f2:
                        item_line = json.loads(f2.read())
                        line["bids"] = item_line[1].get("bids", [])
                        title = item_line[1]["auction"]["title"]
                        line["title"] = title if title else ""
                        video = item_line[1]["auction"]["video"]
                        video = video if video else ""
                        video_key = video.split("vid=")[-1].split('"')[0].strip()
                        new_video = f'<a href="https://v.qq.com/x/page/{video_key}.html" target="_blank" style="color:#1976d2;text-decoration:underline;">视频</a>'
                        info_path = f"D:/_WangKe/scikkk.github.io/projects/ganvana/auction/infos/{line['auction_id']}.info"
                        if os.path.exists(info_path):
                            with open(info_path, "r", encoding="utf-8") as f3:
                                raw_info = f3.read().strip().replace(video, '').replace(new_video, '').strip()
                                info = '\n'.join([raw_info, new_video]).strip()
                        else:
                            raw_info = ""
                            info = '\n'.join([title, new_video]).strip()
                        with open(info_path, "w", encoding="utf-8") as f3:
                            f3.write(info)
                if len(line) > 1:
                    if not line["winner_price"]:
                        line["winner_price"] = 1
                    examples.append(line)

def clean_imgurl(img):
    img = img.replace("http://", "https://").strip()
    if img in ["undefined", "null", "None", ""] + [str(i) for i in range(100)]:
        return ""
    if len(img) <= 5 or '.' not in img or ' ' in img.strip():
        print(f"Invalid image URL found: {img}")
        return ""
    if img.startswith("/uploads/"):
        img = img.replace("/uploads/", "https://admin.ganvana.com/uploads/")
    if img.startswith("https://www.ganvana.com/UploadFiles/p"):
        img = img.replace("https://www.ganvana.com/UploadFiles/p", "https://img.ganvana.com/img/P")
    if img.startswith("https://wechat."):
        img = img.replace("https://wechat.", "https://admin.")
    for num in ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 
                'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen', 'twenty']:
        if f"Pic{num}" in img and f"Pic{num}/" not in img:
            img = img.replace(f"Pic{num}", f"Pic{num}/")
    return img


# 根据id去重并排序
examples_dict = {int(item["id"]): item for item in examples}
examples = sorted(examples_dict.values(), key=lambda x: x["id"])

for example in tqdm(examples, desc="Cleaning image URLs"):
    if "pic" in example and example["pic"]:
        example["pic"] = clean_imgurl(example["pic"])
    if "thumb" in example and example["thumb"]:
        example["thumb"] = clean_imgurl(example["thumb"])
    if "thumb_big" in example and example["thumb_big"]:
        example["thumb_big"] = clean_imgurl(example["thumb_big"])
    if "more_img" in example and example["more_img"]:
        example["more_img"] = [clean_imgurl(img) for img in example["more_img"] if clean_imgurl(img)]
    
with open(jsonl_file, "w", encoding="utf-8") as f:
    for line in tqdm(examples, desc="Saving auction items"):
        f.write(json.dumps(line, ensure_ascii=False) + "\n")




