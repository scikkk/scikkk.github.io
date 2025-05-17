import json
from tqdm import tqdm

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

def load_jsonl(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        data = [json.loads(line) for line in tqdm(f, desc=f"Loading {file_path}")]
    return data

def get_img_list(example):
    cur_img_list = []
    if "pic" in example and example["pic"]:
        cur_img_list.append(example["pic"])
    if "thumb" in example and example["thumb"]:
        if not any([example["thumb"].lower().strip().endswith(ext) for ext in ["s.jpg", "s.jpeg", "s.png", "s.gif"]]):
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
    return cur_img_list

def get_img_list_from_jsonl(file_paths=[
        "D:/_WangKe/scikkk.github.io/projects/ganvana/auction/getItem.jsonl",
        "D:/_WangKe/scikkk.github.io/projects/ganvana/mall/getGoodsInfo.jsonl",
        "D:/_WangKe/scikkk.github.io/projects/ganvana/jilu/getList.jsonl"
    ]):
    examples = []
    for file_path in file_paths:
        examples.extend(load_jsonl(file_path))

    img_list = []
    for example in tqdm(examples, desc="Generating image list"):
        cur_img_list = get_img_list(example)
        img_list.extend(cur_img_list)
    cleaned_img_list = []
    for img in tqdm(img_list, desc="Cleaning image URLs"):
        cleaned_img = clean_imgurl(img)
        if cleaned_img:
            cleaned_img_list.append(cleaned_img)
    print("Removing duplicates...")
    sorted_img_list = sorted(set(cleaned_img_list), key=lambda x: x)
    print(f"Total images: {len(sorted_img_list)}")

    with open("D:/_WangKe/scikkk.github.io/projects/ganvana/imgs/img_list.txt", "w", encoding="utf-8") as f:
        for img in tqdm(sorted_img_list, desc="Saving image list"):
            f.write(img + "\n")

import os
import requests
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

def download_image(url_save_path):
    url, save_path = url_save_path
    try:
        response = requests.get(url, stream=True, timeout=60)
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
        else:
            print(f"Failed to download {url}: Status code {response.status_code}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")

def imgurl2path(img_url):
    img_path = os.path.join("D:/_WangKe/scikkk.github.io/projects/ganvana/imgs", img_url.split('https://')[-1])
    if not os.path.exists(os.path.dirname(img_path)):
        os.makedirs(os.path.dirname(img_path))
    return img_path

def download_all_images(img_list_path="D:/_WangKe/scikkk.github.io/projects/ganvana/imgs/img_list.txt"):
    print("Loading image list...")
    with open(img_list_path, "r", encoding="utf-8") as f:
        img_list = [line.strip() for line in f.readlines()]
    url_save_path = []
    for img_url in tqdm(img_list, desc="Preparing download list"):
        img_path = imgurl2path(img_url)
        if not os.path.exists(img_path):
            url_save_path.append((img_url, img_path))

    # max_workers = 128
    with ThreadPoolExecutor(max_workers=32) as executor:
        list(tqdm(executor.map(download_image, url_save_path), total=len(url_save_path), desc="Downloading"))

    
if __name__ == "__main__":
    get_img_list_from_jsonl()
    download_all_images()