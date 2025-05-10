import gzip
import shutil

auction_jsonl_file = "D:/_WangKe/scikkk.github.io/projects/ganvana/auction/getItem.jsonl"
with open(auction_jsonl_file, 'rb') as f_in, gzip.open(auction_jsonl_file.replace('.jsonl', '.jsonl.gz'), 'wb') as f_out:
    shutil.copyfileobj(f_in, f_out)
mall_jsonl_file = "D:/_WangKe/scikkk.github.io/projects/ganvana/mall/getGoodsInfo.jsonl"
with open(mall_jsonl_file, 'rb') as f_in, gzip.open(mall_jsonl_file.replace('.jsonl', '.jsonl.gz'), 'wb') as f_out:
    shutil.copyfileobj(f_in, f_out)