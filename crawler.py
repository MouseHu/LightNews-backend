import spider-api
class CNNCrawler(object):
    def __init__(self):
        self.header = {
       'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'
        }
        self.news=[];
        #self.html=[]
        self.basicURL="https://edition.cnn.com"
    def openNews(self,url):
        request = urllib.request.Request(self.basicURL+url, headers=header)
        #request = urllib2.Request(url)
        response = urllib.request.urlopen(request).read()
        #print(response)
        soup = BeautifulSoup(response,'html.parser')
        text=soup.find(attrs={"data-zn-id":"body-text"})
        #html.append(str(text))
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
        return story,date
    def getNews(self,url):
        request = urllib.request.Request(url, headers=header)
        #request = urllib2.Request(url)
        response = urllib.request.urlopen(request).read()
        #print(response)
        soup = BeautifulSoup(response,'html.parser')
        #print(soup.prettify())
        news=soup.find_all(attrs={"class":"column zn__column--idx-0"})
        print("begin")
        results=[]
        for n in news:
            media=n.find(class_="media")
            content=n.find(class_="cd__content")
            assert content is not None
            assert media is not None
            nNewsURL=media.contents[0]["href"]
            nImgURL=(media.find("img")["data-src-medium"]).strip("/")
            try:
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
            nNewsContent,nNewsDate=openNews(nNewsURL)
            print(nNewsDate)
            dict_news={"title": nTitle,"source":basicURL+nNewsURL, "abstract": nAbstract,
        "content": nNewsContent,"from_media": "CNN", "pub_date": nNewsDate}
            self.news.append(news)
            #results.append(news)
            #return results
    def craw(self):
        self.news=[]
        self.getNews("https://edition.cnn.com/regions")
        for news in self.news:
             spider-api.post_page(title=news["title"], content=news["content"],source=news["source"],from_media=news["from_media"],date=news["pub_date"])
class ChinaDailyCrawler(object):
    def __init__(self):
        self.type=None;
        self.category={}
        self.header = {
       'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'
        }
        self.news=[];
        self.html=[]
        self.basicURL="http://www.chinadaily.com.cn/world"
    def getContents(self,url,story):
        
        return
    def openNews(self,url):
        #print(url)
        request = urllib.request.Request(url, headers=header)
        #request = urllib2.Request(url)
        response = urllib.request.urlopen(request).read()
        #print(response)
        soup = BeautifulSoup(response,'html.parser')
       # print(soup)
        #print(soup.find(attrs={"class":"info_l"}))
        date=soup.find(attrs={"class":"info_l"}).text.split("Updated:")[1]
        #print(date)
        text=soup.find(attrs={"id":"Content"})
        #html.append(str(text))
        story=""
        #page="page"
        #print(3)
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
            request = urllib.request.Request(url, headers=header)
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
        request = urllib.request.Request(url, headers=header)
        #request = urllib2.Request(url)
        response = urllib.request.urlopen(request).read()
        #print(response)
        soup = BeautifulSoup(response,'html.parser')
        #print(soup.prettify())
        news1=soup.find(attrs={"class":"carousel-inner"})#滚动新闻
        #print(news1)
        #print(news1.contents)
        for n in news1.children:
            #print(n)
            if isinstance(n,(bs4.element.NavigableString,bs4.element.Comment)):
                continue
            #nWrapper=wrapper.contents[0].contents[0]
            #print(media)
            #print(media.contents[0])
            #print(media.find("img"))
            #print(type(n))
            #print(n.contents)
            #print(n.contents[3])
            #print(n.contents[1].contents)
            nContent=n.contents[3].contents[1].contents[0]
            #print(nContent)
            nPic=n.contents[1].contents[1]
            #print(nPic)
            #except:
            #    print(e)
            #    continu
            assert nContent is not None
            assert nPic is not None
            nNewsURL=nContent["href"]
            nTitle=nContent.text
            nImgURL=nPic["src"]
            nAbstract=""
            #print(nContent.text)
            #print(2)
            print(nNewsURL,nImgURL,nTitle,nAbstract)
            nNewsContent,nNewsDate=self.openNews(nNewsURL)
            if nNewsContent=="":
                continue
            print(nNewsContent,nNewsDate)
                #if nURL.name == 'a':
                #    print(basicURL+nURL['href'])
                #    openNews(basicURL+nURL['href'])
                #elif nURL.class_ == 'cd__headline':
                #    openNews(basicURL+nURL.content[0]['href'])
            news={"title": nTitle,
            "source":nNewsURL,
            "abstract": nAbstract,
            "content": nNewsContent,
            "from_media": "ChinaDaily",
            "pub_date": nNewsDate}
            self.news.append(news)
        return
        
    def craw(self):
        self.news=[]
        self.getNews("https://edition.cnn.com/regions")
        for news in self.news:
             spider-api.post_page(title=news["title"], content=news["content"],source=news["source"],from_media=news["from_media"],date=news["pub_date"])
        #openNews(news_list)
        #new.toJson()