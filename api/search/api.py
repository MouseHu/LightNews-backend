# import os
# a=os.popen("curl -X GET \"localhost:9200/article/_doc/1?pretty\"")
# print(a.read())

import urllib
import json
from urllib import parse
from urllib.request import urlopen, Request
from nltk.stem import WordNetLemmatizer
import nltk
import requests

server='http://elasticsearch:9200'


def get_all():
    url = server+'/article/doc/_search/'  # 页面的地址
    header = {'Content-Type': 'application/json'}
    req = Request(url, headers=header)
    response = urlopen(req)  # 调用urllib2向服务器发送get请求
    result = response.read()
    result = json.loads(result.decode())

    #assert len(result["hits"]["hits"]) <= n_return
    return_name = []
    return_score = []
    return_id = []
    for i in range(len(result["hits"]["hits"])):
        return_name.append(result["hits"]["hits"][i]["_source"]["title"])
        return_score.append(float(result["hits"]["hits"][i]["_score"]))
        return_id.append(result["hits"]["hits"][i]["_source"]["id"])
    # print(result)
    return return_name, return_score,return_id

def get_record(list, n_return):
    url = server+'/article/doc/_search/'  # 页面的地址
    new_list=[]
    wnl=WordNetLemmatizer()
    for l in list:
        new_list.append(wnl.lemmatize(l.lower()))
    list=new_list
    data = {
        "query": {"match": {"content": " ".join(list)}}, "size": n_return
    }
    header = {'Content-Type': 'application/json'}
    data = json.dumps(data).encode(encoding='UTF8')
    print(data)
    req = Request(url, data, header)
    # response = urlopen(req)  # 调用urllib2向服务器发送get请求


    result = requests.post(url, data, header)
    result = json.loads(result.text)

    # result = response.read()
    # result = json.loads(result.decode())

    assert len(result["hits"]["hits"]) <= n_return
    return_name = []
    return_score = []
    return_id=[]
    for i in range(min(len(result["hits"]["hits"]), n_return)):
        return_name.append(result["hits"]["hits"][i]["_source"]["title"])
        return_score.append(float(result["hits"]["hits"][i]["_score"]))
        return_id.append(int(result["hits"]["hits"][i]["_source"]["id"]))
    # print(result)
    return return_name, return_score,return_id


def put_record(id, title, date, content, image_url, source, other=None):
    url = server+'/article/doc/'+str(id)+'?pretty'  # 页面的地址
    wnl = WordNetLemmatizer()
    data = {
        "id": str(id),
        "title": title,
        "date": date,
        "content": wnl.lemmatize(content.lower()+' '+title.lower()),
        "image_url": image_url,
        "source": source
    }
    header = {'Content-Type': 'application/json'}
    if (other != None):
        assert type(other) == dict
        for (k, v) in dict(other).items():
            data[k] = v
    data = json.dumps(data).encode(encoding='UTF8')
    print(data)
    req = Request(url, headers=header,data=data)

    #response = urlopen(req)  # 调用urllib2向服务器发送get请求

    response=requests.put(url, headers=header,data=data)
    print(response.text)
    result=json.loads(response.text)
    return result['result'],result['_shards']['failed']


#
#
#
# ret = put_record(15, "title_13",
#                  "20180605",
#                  "content contetn conten tested aaa content",
#                  "xxx",
#                  "CNN")
# print(ret)
# ret = put_record(14, "title_14",
#                  "20180605",
#                  "content conten tested aaa content",
#                  "xxx",
#                  "CNN")
# print(ret)
# ret = put_record(13, "title_15",
#                  "20180605",
#                  "conested aaa tent",
#                  "xxx",
#                  "CNN")
# print(ret)
# ret = put_record(16, "title_16",
#                  "20180605",
#                  "content conested aaa content lsjdoiansjcan aoisd aosid oa o pap pa ",
#                  "xxx",
#                  "CNN")
# print(ret)
# print(get_all())
ret = get_record(["aaa", "uhu","test"], 10)
# print(ret)