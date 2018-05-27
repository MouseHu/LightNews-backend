import json
import requests

def post_page(title,content,source,date,from_media=None, abstract="No abstract"):
    textmod={
    "title": title,
    "source": source,
    "abstract": abstract,
    "content": content,
    "from_media": from_media,
    "pub_date": date
    }
    header_dict = {'Authorization': 'Token 7ef5bc0c59773e1c1a708b06c7d04114e56939f9','Content-Type':'application/json'}
    
    url='https://api.li-positive-one.com:4433/articles/'

    textmod = json.dumps(textmod).encode(encoding='utf-8')
    req = requests.post(url=url,headers=header_dict,data=textmod)
    req = req.json()
    print(req)

if __name__ == '__main__':

    example={

    "title": "Putin: Russia-China ties significant, bilateral cooperation promising",
    "source": "https://news.cgtn.com/news/3d3d414d34417a4e77457a6333566d54/share_p.html",
    "abstract": "No abstract",
    "content": "sad",
    "from_media": None,
    "pub_date": "2018-05-29"}

    post_page(title=example["title"], content=example["content"],source=example["source"],date=example["pub_date"])