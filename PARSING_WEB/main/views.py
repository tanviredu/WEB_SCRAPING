from django.shortcuts import render,redirect
## this module is for testing
from django.http import HttpResponse

## this is where all the logic goes
import requests
from bs4 import BeautifulSoup

## import json for parsing
import json
import pandas as pd

## add searching by doing to the website using http response

def home(request):
    return render(request,'public/search.html')

def Bagdoom(keyword):
    url="https://www.bagdoom.com/catalogsearch/result/?q="+str(keyword)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    ans2= soup.findAll('div', attrs={'class':'catalog_hover'})
    d={}
    for item in ans2:
        a=item.find('h2', attrs={'class':'product-name'}).text.strip()
        b=item.find('span', attrs={'class':'price'}).text.strip()
        d.update({a:b})
    return d,url







def daraz(keyword):
    url="https://www.daraz.com.bd/catalog/?q="+str(keyword)+"&_keyori=ss&from=input&spm=a2a0e.searchlist.search.go.34001d3evRxuRK"
    # Download the page using requests
    r = requests.get(url)

    ## making the JSON ready for parsing
    soup = BeautifulSoup(r.content, 'lxml')

    for script in soup.select('script'):
        if 'window.pageData=' in script.text:
            script = script.text.replace('window.pageData=','')
            break
    items = json.loads(script)
    items=items['mods']['listItems']
    e={}
    for item in items:
        a=str(item['name'][:10])
        b=str((item['price'][:6])+" BDT")
        e.update({a:b})
    return e,url
# processing a preety url

def rokomari(keyword):
    url="https://www.rokomari.com/search?term="+str(keyword)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    ## adding the name
    name=[]
    for node in soup.findAll('div', attrs={'class':'browse__content-books-wrapper'}):
        for item in (node.findAll('p',attrs={'class':'book-title'})):
            name.append(item.text)
    result=[]
    for node in soup.findAll('div', attrs={'class':'browse__content-books-wrapper'}):
        for item in (node.findAll('p',attrs={'class':'book-price'})):
            result.append(item.text.strip())
    f={}
    for x,y in zip(name,result):
        f.update({x:y})
    return f,url    


def craiglist(keyword):
    url='https://newjersey.craigslist.org/search/sss?query='+str(keyword)+'&sort=rel'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    name=[]
    for node in soup.findAll('p',attrs={'class':'result-info'}):
        name.append((node.find('a').text))
    result=[]
    for node in soup.findAll('span',attrs={'class':'result-price'}):
        result.append((node.text))
    g={}
    for x,y in zip(name,result):
        g.update({x:y})
    return g,url

def walmart(keyword):
    url='https://www.walmart.com/search/?query='+str(keyword)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    ans= soup.findAll('ul', attrs={'class':'search-result-gridview-items'})
    name=[]
    for node in soup.findAll('a', attrs={'class':'product-title-link line-clamp line-clamp-2'}):
        name.append(node.find('span').text.strip())
    price=[]
    for node in soup.findAll('span', attrs={'class':'price display-inline-block arrange-fit price price-main'}):
        price.append(node.span.text)
    m={}
    for x,y in zip(name,price):
        m.update({x:y})
    return m,url
        
    

    



def process(request):
    if request.method == "POST":
        ## take the value
        keyword = str(request.POST['keyword'])
        ##return HttpResponse(keyword)
        text1,url1 = Bagdoom(keyword)
        data1=pd.Series(text1).to_frame()
        pd.DataFrame(data1).to_csv('bagdoom.csv')
        text2,url2 = daraz(keyword)
        data2=pd.Series(text2).to_frame()
        pd.DataFrame(data2).to_csv('daraz.csv')
        ## adding the rokomari
        text3,url3 = rokomari(keyword)
        data3=pd.Series(text3).to_frame()
        pd.DataFrame(data3).to_csv('rokomari.csv')
        text4,url4 = craiglist(keyword)
        data4=pd.Series(text4).to_frame()
        pd.DataFrame(data4).to_csv('craglist.csv')
        text5,url5 = walmart(keyword)
        data5=pd.Series(text5).to_frame()
        pd.DataFrame(data5).to_csv('walmart.csv')
        
        context = {'text1':text1,'text2':text2,'text3':text3,'text4':text4,'text5':text5,'url1':url1,'url2':url2,'url3':url3,'url4':url4,'url5':url5}
        return render(request,'public/result.html',context)
        #text=daraz(keyword)
        #return HttpResponse(text)