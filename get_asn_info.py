import time
import requests
import ujson
import os
from multiprocessing import Pool

# 定义API的URL和请求头
API_URL = 'https://api.asrank.caida.org/v2/graphql'
HEADERS = {'Content-Type': 'application/json'}

def multi_process(function, argc, num_process):
    p = Pool(num_process)
    result = p.map(function, argc)
    p.close()
    p.join()
    return result

def get_asn_data(asn, retry=3, delay=5):
    # GraphQL查询
    query = '''
    {{
    asn(asn: "{asn}") {{
        asn
        asnName
        rank
        source
        organization {{
        orgName
        rank
        }}
        cone {{
        numberAsns
        numberPrefixes
        numberAddresses
        }}
        asnDegree {{
        provider
        peer
        customer
        sibling
        transit
        total
        }}
        country {{
        iso
        name
        }}
    }}
    }}
    '''.format(asn=asn)

    # # 发送请求
    # response = requests.post(API_URL, headers=HEADERS, json={'query': query})
    # # 检查响应
    # if response.status_code == 200:
    #     data = ujson.loads(response.text)
    #     # 根据需要调整返回数据的结构以符合V1.0的格式
    #     return data['data']['asn']
    # else:
    #     print("Query failed for ASN {}: Status code {}. {}".format(asn, response.status_code, response.text))
    #     return None
    
    while retry > 0:
        response = requests.post(API_URL, headers=HEADERS, json={'query': query})
        if response.status_code == 200:
            data = ujson.loads(response.text)
            return data['data']['asn']
        else:
            retry -= 1
            print("Retry {} for ASN {}: Status code {}. {}".format(3 - retry, asn, response.status_code, response.text))
            time.sleep(delay)  # 等待一段时间后重试
    return None

def get_asn_list():
    # 获取ASN列表的逻辑根据您的具体情况编写
    asn_json = '/u/yrm2kw/Desktop/files/data/aspath/test/all_asn.json' # 替换为您的实际文件路径
    with open(asn_json, 'r') as fp:
        data = ujson.load(fp)
    return [item['asn'] for item in data if 'asn' in item]

def fetch_asn_data(asn_list):
    asn_data = {}
    for asn in asn_list:
        data = get_asn_data(asn, 3, 5)
        if data:
            asn_data[asn] = data
        # time.sleep(1)  # 每个请求之间暂停1秒
    return asn_data

if __name__ == "__main__":
    n = 10 # 进程数量
    total_asn_list = get_asn_list() # 获取所有ASN列表
    length = len(total_asn_list)
    para = [total_asn_list[i::n] for i in range(n)] # 将ASN列表分割为n部分

    result = multi_process(fetch_asn_data, para, n)
    asn_info = {}
    for r in result:
        asn_info.update(r)

    # 将结果保存到文件
    as_rank_json = '/u/yrm2kw/Desktop/files/data/aspath/as_rank_info.json' # 替换为您的实际文件路径
    with open(as_rank_json, 'w') as fp:
        ujson.dump(asn_info, fp)
