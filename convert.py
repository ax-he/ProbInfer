import json

def convert_jsonl_to_json(jsonl_file_path, json_file_path):
    data = []

    # 打开 JSONL 文件并读取每一行
    with open(jsonl_file_path, 'r') as file:
        for line in file:
            json_obj = json.loads(line)
            data.append(json_obj)

    # 将数据保存为标准 JSON 格式
    with open(json_file_path, 'w') as file:
        json.dump(data, file, indent=4)

# 设置文件路径
jsonl_file_path = '/u/yrm2kw/Desktop/ProbInfer/asns.jsonl'
json_file_path = '/u/yrm2kw/Desktop/files/data/aspath/test/all_asn.json'

# 转换文件
convert_jsonl_to_json(jsonl_file_path, json_file_path)

print("转换完成，文件已保存到:", json_file_path)
