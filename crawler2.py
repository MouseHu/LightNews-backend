#import spiderapi
import datetime
import json
import requests
import bs4
import urllib
from bs4 import BeautifulSoup
import socket
import http.client
import re
class Crawler(object):
    def __init__(self):
        self.header = {
       'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'
        }
        self.news=[];
    def post_page(self,title,content,source,date,from_media=None, abstract="No abstract",img_url=""):
        textmod={
        "title": title,
        "source": source,
        "abstract": abstract,
        "content": content,
        "from_media": from_media,
        "pub_date": date,
        "img_url": img_url
        }
        header_dict = {'Authorization': 'Token 7ef5bc0c59773e1c1a708b06c7d04114e56939f9','Content-Type':'application/json'}

        url='https://api.li-positive-one.com:4433/articles/'

        textmod = json.dumps(textmod).encode(encoding='utf-8')
        req = requests.post(url=url,headers=header_dict,data=textmod)
        req = req.json()
        #if textmod==req:
        print(req)
        return
    def getNews(self,url):
        print("Warning:NO Source Specified")
        return
    def craw(self):
        self.news=[]
        for url in self.crawURL:
            self.getNews(url)

        for new in self.news:

            self.post_page(title=new["title"], content=new["content"],source=new["source"],from_media=new["from_media"],date=new["pub_date"],img_url=new["img_url"])
class CNNCrawler(Crawler):
    def __init__(self):
        #self.html=[]
        super(CNNCrawler,self).__init__()   
        self.basicURL="https://edition.cnn.com"
        self.crawURL=["https://edition.cnn.com/regions"]
    def openNews(self,url):
        request = urllib.request.Request(self.basicURL+url, headers= self.header)

        response = urllib.request.urlopen(request).read()

        soup = BeautifulSoup(response,'html.parser')
        text=soup.find(attrs={"data-zn-id":"body-text"})

        story=""
        container=text.contents[0]
        for n in container.children:
            if re.match("zn-body__paragraph",n["class"][0]) is None:
                continue
            story+=n.text+"\n"
        ex=re.compile('\{.*?\}')
        story=ex.sub("",story)
        story=story.replace("Read More","")
        #news.append(story)
        print(story)
        
        date=soup.find(class_="update-time").text
        date2=date.split(" ")[-4:-1]
        newDate=""
        for i in date2:
            newDate+=i
        newDate=datetime.datetime.strptime(newDate,"%b%d,%Y")
        newDate=str(newDate).split(" ")[0]
        #print(date2)
        return story,newDate
    def getNews(self,url):
        request = urllib.request.Request(url, headers= self.header)
        #request = urllib2.Request(url)
        response = urllib.request.urlopen(request).read()
        #print(response)
        soup = BeautifulSoup(response,'html.parser')
        #print(soup.prettify())
        news=soup.find_all(attrs={"class":"column zn__column--idx-0"})
        print("begin")
        results=[]
        #print("1")
        for n in news:
            #print("holy why?")
            media=n.find(class_="media")
            content=n.find(class_="cd__content")
            assert content is not None
            assert media is not None
            nNewsURL=media.contents[0]["href"]
            nImgURL=(media.find("img")["data-src-medium"]).strip("/")
            nImgURL="http://"+nImgURL
            #print("holy why?")
            try:
                #print("why?")
                nTitle=content.find(attrs={"data-analytics":"_list-hierarchical-piped_article_"}).text
            except:
                nTitle="NO TITLE"
                continue
            try:
                nAbstract=content.find(class_="cd__headline-text").text
            except:
                nAbstract=""
            #print(nContent.text)
            print(nNewsURL,nImgURL,nTitle,nAbstract)
            nNewsContent,nNewsDate=self.openNews(nNewsURL)
            print(nNewsDate)
            submit={"title": nTitle,"source":self.basicURL+nNewsURL, "abstract": nAbstract,
        "content": nNewsContent,"from_media": "CNN", "pub_date": nNewsDate,"img_url":nImgURL}
            self.news.append(submit)
            #print(type(submit))
            #results.append(news)
            #return results
    
class ChinaDailyCrawler(Crawler):
    def __init__(self):
        super(ChinaDailyCrawler,self).__init__()   
        self.basicURL="http://www.chinadaily.com.cn/world"
        self.crawURL=["http://www.chinadaily.com.cn/world","http://www.chinadaily.com.cn/china","http://www.chinadaily.com.cn/culture","http://www.chinadaily.com.cn/life"]
    def getContents(self,url,story):
        
        return
    def openNews(self,url):
        #print(url)
        request = urllib.request.Request(url, headers= self.header)

        response = urllib.request.urlopen(request).read()

        soup = BeautifulSoup(response,'html.parser')
        
        date=soup.find(attrs={"class":"info_l"}).text.split("Updated: ")[1]
        print(date)
        date=date.split(" ")[0]
        print(date)
        text=soup.find(attrs={"id":"Content"})

        story=""
        while True:
            for p in text.children:
                if p.name !="p":
                    continue
                story+=p.text+"\n"
            page=soup.find(attrs={"id":"div_currpage"})
            if page is None:
                break
            nextPage=page.find(attrs={"class":"pagestyle"})
            if nextPage is None or nextPage.text !="Next":
                break;
            url=nextPage["href"]
            request = urllib.request.Request(url, headers= self.header)
            #request = urllib2.Request(url)
            response = urllib.request.urlopen(request).read()
            #print(response)
            soup = BeautifulSoup(response,'html.parser')   
            text=soup.find(attrs={"id":"Content"})
            #print(story,nextPage)
            
        #print(attrs={"id":"Content"})
        #date=soup.find(class_="update-time").text
        return story,date
    def getNews(self,url):
        request = urllib.request.Request(url, headers= self.header)
        response = urllib.request.urlopen(request).read()
        soup = BeautifulSoup(response,'html.parser')
        #print(soup)
        news=soup.find(attrs={"class":"carousel-inner"})#滚动新闻
        print(news)
        for n in news.children:
            if isinstance(n,(bs4.element.NavigableString,bs4.element.Comment)):
                continue
            #print(n,url,re.match("world",url))
            if re.search("world",url) is not None:
                nContent=n.contents[3].contents[1].contents[0]
                nPic=n.contents[1].contents[1]
            else:
                #print(n.contents)
                ##print(n.contents[3].contents)
                #print(n.contents[3].contents[0].contents)
                nContent=n.contents[3].contents[0].contents[0]
                nPic=n.contents[1].contents[0]
                #print(nContent,nPic)
            
            assert nContent is not None
            assert nPic is not None
            
            nNewsURL=nContent["href"]
            nTitle=nContent.text
            nImgURL=nPic["src"]
            nAbstract=""
            
            print(nNewsURL,nImgURL,nTitle,nAbstract)
            
            nNewsContent,nNewsDate=self.openNews(nNewsURL)
            
            if nNewsContent=="":
                continue
                
            print(nNewsContent,nNewsDate)
                
            submit={"title": nTitle,"source":nNewsURL, "abstract": nAbstract,"content": nNewsContent,"from_media": "CGTN","img_url":nImgURL,"pub_date": nNewsDate}
            self.news.append(submit)
        return
def craw():
    print("begin")
    chinadaily=ChinaDailyCrawler()
    chinadaily.craw()
    print("china daily news craw over")
    print("begin")
    cnn=CNNCrawler()
    cnn.craw()
    print("cnn news craw over")
