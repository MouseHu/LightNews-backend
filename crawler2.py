# %load crawler2.py
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
import demjson
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
        if text is None:
            return None,None
        container=text.contents[0]
        for n in container.children:
            if re.match("zn-body__paragraph",n["class"][0]) is None:
                continue
            story+=n.text+"\n"
        ex=re.compile('\{.*?\}')
        story=ex.sub("",story)
        story=story.replace("Read More","")
        #news.append(story)
        #print(story)
        
        date=soup.find(class_="update-time").text
        date2=date.split(" ")[-4:-1]
        newDate=""
        for i in date2:
            newDate+=i
        newDate=datetime.datetime.strptime(newDate,"%B%d,%Y")
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
            if content is None or  media is None:
                continue
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
            if nNewsContent is None or nNewsContent == "":
                continue
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
        self.crawURL=["http://www.chinadaily.com.cn/travel","http://www.chinadaily.com.cn/business","http://www.chinadaily.com.cn/world","http://www.chinadaily.com.cn/china",
                      "http://www.chinadaily.com.cn/culture","http://www.chinadaily.com.cn/life",
                      "http://www.chinadaily.com.cn/opinion"]
        self.types={"http://www.chinadaily.com.cn/business":2,"http://www.chinadaily.com.cn/travel":2,
                    "http://www.chinadaily.com.cn/world":0,"http://www.chinadaily.com.cn/china":1,"http://www.chinadaily.com.cn/culture":1,"http://www.chinadaily.com.cn/life":0,
                   "http://www.chinadaily.com.cn/culture":1,"http://www.chinadaily.com.cn/opinion":0
                   }
        
    def getContents(self,url,story):
        
        return
    def openNews(self,url):
        #print(url)
        request = urllib.request.Request(url, headers= self.header)

        response = urllib.request.urlopen(request).read()

        soup = BeautifulSoup(response,'html.parser')
        
        date=soup.find(attrs={"class":"info_l"}).text.split("Updated: ")[1]
        date=date.split(" ")[0]

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
            nextPage=page.find_all(attrs={"class":"pagestyle"})
            if nextPage is None:
                break
            next_flag=False
            for button in nextPage:
                if button.text !="Next":
                    continue
                url=button["href"]
                next_flag=True
            if next_flag==False:
                break
            request = urllib.request.Request(url, headers= self.header)
            #request = urllib2.Request(url)
            response = urllib.request.urlopen(request).read()
            #print(response)
            soup = BeautifulSoup(response,'html.parser')   
            text=soup.find(attrs={"id":"Content"})
        return story,date
    def getNews(self,url):
        request = urllib.request.Request(url, headers= self.header)
        response = urllib.request.urlopen(request).read()
        soup = BeautifulSoup(response,'html.parser')
        #print(soup)
        if self.types[url]==2:
            news=soup.find(attrs={"id":"D1pic1"})#滚动新闻
        else:
            news=soup.find(attrs={"class":"carousel-inner"})#滚动新闻
        #print(news)
        for n in news.children:
            if isinstance(n,(bs4.element.NavigableString,bs4.element.Comment)):
                continue
            #print(n)
            nURL=""
            try:
                if self.types[url]==0:
                    nContent=n.contents[3].contents[1].contents[0]
                    nPic=n.contents[1].contents[1]
                elif self.types[url]==1:
                    #print(n.contents)
                    nContent=n.contents[3].contents[0].contents[0]

                    nPic=n.contents[1].contents[0]
                    #print(nContent,nPic)
                else:
                    #print(n.contents[1].contents)
                    nContent=n.contents[3].contents[1]
                    nPic=n.contents[1].contents[1]
                    nURL=n.contents[1]
            except IndexError:
                continue
            assert nContent is not None
            assert nPic is not None
            if self.types[url]==2:
                nNewsURL=nURL["href"]
            else:
                nNewsURL=nContent["href"]
            nTitle=nContent.text
            nImgURL=nPic["src"]
            nAbstract=""
            
            print(nNewsURL,nImgURL,nTitle,nAbstract)
            
            nNewsContent,nNewsDate=self.openNews(nNewsURL)
            
            if nNewsContent=="":
                continue
                
            #print(nNewsContent,nNewsDate)
                
            submit={"title": nTitle,"source":nNewsURL, "abstract": nAbstract,"content": nNewsContent,"from_media": "ChinaDaily","img_url":nImgURL,"pub_date": nNewsDate}
            self.news.append(submit)
        return

class CGTNCrawler(Crawler):
    def __init__(self):
        super(CGTNCrawler,self).__init__()   
        self.header = {
       'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36 '
        }
        self.basicURL="https://www.cgtn.com/news/"
        self.crawURL=["https://www.cgtn.com/news/section.do?curPage=0&category=1",
                      "https://www.cgtn.com/news/section.do?curPage=0&category=2",
                      "https://www.cgtn.com/news/section.do?curPage=0&category=4",
                      "https://www.cgtn.com/news/section.do?curPage=0&category=5",
                      "https://www.cgtn.com/news/section.do?curPage=0&category=7",
                      "https://www.cgtn.com/news/section.do?curPage=0&category=8",
                      "https://www.cgtn.com/news/section.do?curPage=0&category=9"]
        self.types={"https://www.cgtn.com/news/section.do?curPage=0&category=1":0,
                      "https://www.cgtn.com/news/section.do?curPage=0&category=2":0,
                      "https://www.cgtn.com/news/section.do?curPage=0&category=4":0,
                      "https://www.cgtn.com/news/section.do?curPage=0&category=5":0,
                      "https://www.cgtn.com/news/section.do?curPage=0&category=7":0,
                      "https://www.cgtn.com/news/section.do?curPage=0&category=8":0,
                      "https://www.cgtn.com/news/section.do?curPage=0&category=9":0
                   }
        
    def getContents(self,url,story):
        
        return
    def openNews(self,url):
        #print(url)
        request = urllib.request.Request(url, headers= self.header)
        response = urllib.request.urlopen(request).read()
        soup = BeautifulSoup(response,'html.parser')
        nImgURL=""
        try:
            nImgURL=soup.find(attrs={"class":"TopPicture"})["src"]
        except:
            pass
        #print("begin here")
        #print(soup)
        #print("end here")
        content=soup.find(attrs={"class":"m-content"})
        #print(content)
        text=demjson.decode(content['data-json'])
        #print(text)
        story=""
        for t in text:
            if t["contentType"]==1:
                 story+=t['content']
        #story=text[0]["content"]
        #print(story)
        #story=re.sub(r"</[^>].*?>","\n",story)
        story=re.sub(r"<[^>].*?>","\n",story)
        story=re.sub(r"\n+","\n",story)
        #print(story)
        if nImgURL=="":
            try:
                nImgURL=content.find_all(attrs={"class":"cmsImage"})[0].contents[0]["src"]
            except:
                pass
                #print(content)
        #if nImgURL=="":
        #print(story)
        return story,nImgURL
    def getNews(self,url):
        #print(url)
        request = urllib.request.Request(url, headers= self.header)
        response = urllib.request.urlopen(request).read()
        soup = BeautifulSoup(response,'html.parser')
        #print(soup)
        if self.types[url]==0:
            news=soup.find_all(attrs={"class":"m-content-section-description"})+soup.find_all(attrs={"class":"m-content-top-first-description"})#滚动新闻
        else:
            news=soup.find(attrs={"class":"carousel-inner"})#滚动新闻
        #print(news)
        for n in news:
            if isinstance(n,(bs4.element.NavigableString,bs4.element.Comment)):
                continue
            #print(n)
            
            title=n.find(attrs={"class":"title"})
            content=n.find(attrs={"class":"content"})
            date=n.find(attrs={"class":"time"})
            #print(title)
            try:
                nTitle=title.contents[0].contents[0].text
                nNewsURL=title.contents[0].contents[0]["href"]
            except:
                nTitle=title.contents[0].text
                nNewsURL=title.contents[0]["href"]
            if content is None:
                nAbstract=""
            else:
                nAbstract=content.text
            nNewsDate=date.contents[0].text.split(" ")[0]
            #nDate=datetime.datetime.strptime(nDate,"%Y-%m-%d %H:%M ")
            #nDate=str(nDate).split(" ")[0]
            
            print(nNewsURL,nTitle,nAbstract,nNewsDate)
            nNewsContent,nImgURL=self.openNews(nNewsURL)
            
            if nNewsContent=="":
                continue
                
            #print(nNewsContent,nNewsDate)
                
            submit={"title": nTitle,"source":nNewsURL, "abstract": nAbstract,"content": nNewsContent,"from_media": "CGTN2","img_url":nImgURL,"pub_date": nNewsDate}
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
    print("begin")
    cgtn=CGTNCrawler()
    cgtn.craw()
    print("cgtn news craw over")
#craw() 