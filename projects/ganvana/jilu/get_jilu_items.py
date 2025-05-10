import os
import json
import time
import requests
from tqdm import tqdm

url = "https://www.ganvana.com/jilu/getList"
"""POST /jilu/getList HTTP/1.1"""
headers = {"Accept": "*/*",
"Accept-Encoding": "gzip, deflate, br, zstd",
"Accept-Language": "zh,zh-CN;q=0.9,en;q=0.8",
"Connection": "keep-alive",
"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
"Cookie": "TouchStone20181129=eyJuaWNrbmFtZSI6InNjaWtrayIsIndobyI6IjE3NDUzOTg1NzI3MDczMGFlMmU0Njc3MzQyYjA5NGNhZmYzMDUyNzU4ZWFiMSIsIl9leHBpcmUiOjE3NDgxODE2MTY4NDIsIl9tYXhBZ2UiOjI1OTIwMDAwMDB9; TouchStone20181129.sig=_SVoewtC3xjDrtyRjmCo2wIhUYo",
"Host": "www.ganvana.com",
"Origin": "https://www.ganvana.com",
"Referer": "https://www.ganvana.com/jilu/list",
"Sec-Fetch-Dest": "empty",
"Sec-Fetch-Mode": "cors",
"Sec-Fetch-Site": "same-origin",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
"X-Requested-With": "XMLHttpRequest",
"sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
"sec-ch-ua-mobile": "?0",
"sec-ch-ua-platform": "Windows"
}
    


MAX_PAGE = 10
dir = "D:/_WangKe/ganvana/jilu/getList"
jsonl_file = "D:/_WangKe/ganvana/jilu/getList.jsonl"

# get last page
with open(jsonl_file, "r", encoding="utf-8") as f:
    last_page = json.loads(f.readlines()[-1])["page"]
    print("last page:", last_page)
for page in tqdm(range(MAX_PAGE + 1)):
    if page <= last_page:
        continue
    data = {
        "page": f"{page}",
        "search[name]": "",
        "search[lat_name]": "",
        "search[cate1]": "0",
        "search[cate2]": "0",
    }
    for _ in range(1):
        try:
            response = requests.post(url, headers=headers, data=data, timeout=60)
            new_list = response.json()["list"]
            assert MAX_PAGE == response.json()["pages"]["all_page"]
            break
        except:
            print("error:", page)
            print(response.status_code)
            print(response.text)
            time.sleep(0.1)
    for new_line in new_list:
        idx = new_line["id"]
        new_line["page"] = page
        sub_dir = os.path.join(dir, f"{idx//10000:05d}")
        if not os.path.exists(os.path.join(dir, sub_dir)):
            os.makedirs(os.path.join(dir, sub_dir))
        with open(os.path.join(dir, sub_dir, str(idx)+".json"), "w", encoding="utf-8") as f:
            json.dump(new_line, f, ensure_ascii=False, indent=4)
        with open(jsonl_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(new_line, ensure_ascii=False) + "\n")
    time.sleep(1)

