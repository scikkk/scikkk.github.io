import os
import time
import json
import urllib3
import requests
from lxml import etree
from pdf2image import convert_from_path
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


response = requests.get('https://www.ganvana.com/mall/goods/1', verify=False, timeout=10)
print(response.text)
with open('D:/_WangKe/ganvana/goods_template.html', 'w', encoding='utf-8') as f:
    f.write(response.text)
response = requests.get('https://www.ganvana.com/mall/list/', verify=False, timeout=10)
print(response.text)
with open('D:/_WangKe/ganvana/list_template.html', 'w', encoding='utf-8') as f:
    f.write(response.text)