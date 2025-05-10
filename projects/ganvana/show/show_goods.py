import os
import json
import time
import requests
from tqdm import tqdm
import sys
sys.path.append("D:/_WangKe/ganvana")
from imgs.get_imgs import imgurl2path, get_img_list, clean_imgurl





def id2show_goods(show_idx):
    mall_root = "D:/_WangKe/scikkk.github.io/projects/ganvana/mall/getGoodsInfo"
    html_file = "D:/_WangKe/scikkk.github.io/projects/ganvana/show/showgoods.html"
    sub_dir = os.path.join(mall_root, f"{show_idx//10000:05d}")
    with open(os.path.join(mall_root, sub_dir, str(show_idx)+".json"), "r", encoding="utf-8") as f:
        new_line = json.loads(f.read())
        # print(json.dumps(new_line, ensure_ascii=False, indent=4))
        if len(new_line) == 1:
            print("no goods:", show_idx)
            return

    html_str = ""
    with open(html_file, "r", encoding="utf-8") as f:
        html_str = f.read()
    html_str = html_str.replace("|goods_id|", str(new_line["id"]))
    html_str = html_str.replace("|goods_name|", new_line["name"])
    with open(html_file.replace(".html", "_true.html"), "w", encoding="utf-8") as f:
        f.write(html_str)

    img_list = get_img_list(new_line)
    new_line_str = json.dumps(new_line, ensure_ascii=False, indent=4)
    for imgurl in img_list:
        imgpath = imgurl2path(clean_imgurl(imgurl))
        if imgpath.endswith("s.jpg"):
            imgpath = imgpath.replace("s.jpg", ".jpg")
        new_line_str = new_line_str.replace(imgurl, imgpath.replace("\\", "/").split("/ganvana")[-1])
    new_line = json.loads(new_line_str)
    new_line["img_list"] = img_list
    return new_line

def show_goods(show_idx):
    print("show_goods:", show_idx)
    new_line = id2show_goods(show_idx)
    show_json = "D:/_WangKe/ganvana/show/goods.json"
    with open(show_json, "w", encoding="utf-8") as f:
        f.write(json.dumps(new_line, ensure_ascii=False, indent=4))

if __name__ == "__main__":
    import random
    import time
    for i in range(100):
        show_goods(random.randint(1, 46551))
        time.sleep(1)
        