import os
import json
import urllib3
from tqdm import tqdm
import shutil
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def clean_img(img):
    img = img.replace("http://", "https://").strip()
    if img in ["undefined", "null", "None", ""] + [str(i) for i in range(100)]:
        return ""
    if len(img) <= 5 or '.' not in img:
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



url = "https://www.ganvana.com/auction/getItem/"
auction_root = "D:/_WangKe/ganvana/auction/getItem"
jsonl_file = "D:/_WangKe/ganvana/auction/getItem.jsonl"

# get last idx
with open(jsonl_file, "r", encoding="utf-8") as f:
    last_idx = json.loads(f.readlines()[-1])["id"]
    print("last idx:", last_idx)


def load_jsonl(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    return [json.loads(line) for line in tqdm(lines)]
examples = load_jsonl(jsonl_file)



for example in tqdm(examples, desc="Processing"):
    cur_img_list = []
    if "pic" in example and example["pic"]:
        cur_img_list.append(example["pic"])
    if "thumb" in example and example["thumb"]:
        cur_img_list.append(example["thumb"])
    if "thumb_big" in example and example["thumb_big"]:
        cur_img_list.append(example["thumb_big"])
    if "more_img" in example and example["more_img"]:
        cur_img_list.extend(example["more_img"])
    content = example.get("content", "")
    for sub_a in content.split('"'):
        for sub_b in sub_a.split("="):
            for sub_c in sub_b.split(","):
                if "http" in sub_c:
                    cur_img_list.append(sub_c.strip())
                    if not sub_c.strip().endswith(".jpg"):
                        print(sub_c)
                        
    img_dir = os.path.join(auction_root, str(example["auction_id"]),"images")
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
    for img in cur_img_list:
        if img.endswith("s.jpg"):
            continue
        img_url = clean_img(img)
        img_path = "D:/_WangKe/ganvana/imgs/" + img_url.split('https://')[-1]
        if not os.path.exists(img_path):
            print(f"Image not found: {img_path}")
            continue
        if not os.path.exists(img_dir+"/" + img_path.split("/")[-1]):
            print(f"Copying {img_path} to {img_dir}")
            shutil.copy2(img_path, img_dir)