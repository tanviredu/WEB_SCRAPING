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

# def rokomari(keyword):
#     url="https://www.rokomari.com/search?term="+str(keyword)
#     r = requests.get(url)
#     soup = BeautifulSoup(r.content, 'lxml')
#     ## adding the name
#     name=[]
#     for node in soup.findAll('div', attrs={'class':'browse__content-books-wrapper'}):
#         for item in (node.findAll('p',attrs={'class':'book-title'})):
#             name.append(item.text)
#     result=[]
#     for node in soup.findAll('div', attrs={'class':'browse__content-books-wrapper'}):
#         for item in (node.findAll('p',attrs={'class':'book-price'})):
#             result.append(item.text.strip())
#     f={}
#     for x,y in zip(name,result):
#         f.update({x:y})
#     return f,url    


# def craiglist(keyword):
#     url='https://newjersey.craigslist.org/search/sss?query='+str(keyword)+'&sort=rel'
#     r = requests.get(url)
#     soup = BeautifulSoup(r.content, 'lxml')
#     name=[]
#     for node in soup.findAll('p',attrs={'class':'result-info'}):
#         name.append((node.find('a').text))
#     result=[]
#     for node in soup.findAll('span',attrs={'class':'result-price'}):
#         result.append((node.text))
#     g={}
#     for x,y in zip(name,result):
#         g.update({x:y})
#     return g,url

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
        

def shadmart(keyword):
    url="https://www.shadmart.com/index.php?route=product/search&search="+str(keyword)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    ans= soup.findAll('h4', attrs={'class':'name'})
    name=[]
    for item in ans:
        name.append(item.text.strip()[:20])
    price=[]
    for item in soup.findAll('span', attrs={'class':'price-new'}):
        price.append(item.text.strip()[:20])
    m={}
    for x,y in zip(name,price):
        m.update({x:y})
    return m,url




def shopclus(keyword):
    url="https://www.shopclues.com/search?q="+str(keyword)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    ans= soup.findAll('ul', attrs={'class':'search-result-gridview-items'})
    name=[]
    for node in soup.findAll('div', attrs={'class':'column col3 search_blocks'}):
        name.append(node.find('h2').text)
    price=[]
    for node in soup.findAll('div', attrs={'class':'column col3 search_blocks'}):
        price.append(node.find('span', attrs={'class':'p_price'}).text.strip())
    m={}
    for x,y in zip(name,price):
        m.update({x:y})
    return m,url



# def paytm(keyword):
#     url="https://paytm.com/shop/search?q="+str(keyword)
#     r = requests.get(url)
#     soup = BeautifulSoup(r.content, 'lxml')
#     ans= soup.findAll('ul', attrs={'class':'search-result-gridview-items'})
#     name=[]
#     for item in soup.findAll('div', attrs={'class':'_2apC'}):
#         name.append(item.text.strip())
#     price=[]
#     for item in soup.findAll('span', attrs={'class':'_1kMS'}):
#         price.append(item.text.strip())
#     m={}
#     for x,y in zip(name,price):
#         m.update({x:y})
#     return m,url




def shopclus(keyword):
    url="https://paytm.com/shop/search?q="+str(keyword)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    ans= soup.findAll('ul', attrs={'class':'search-result-gridview-items'})
    name=[]
    for item in soup.findAll('div', attrs={'class':'_2apC'}):
        name.append(item.text.strip())
    price=[]
    for item in soup.findAll('span', attrs={'class':'_1kMS'}):
        price.append(item.text.strip())
    m={}
    for x,y in zip(name,price):
        m.update({x:y})
    return m,url






def ofuronto(keyword):
    url="https://ofuronto.com/?s="+str(keyword)+"&post_type=product"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    ans= soup.findAll('ul', attrs={'class':'search-result-gridview-items'})
    name=[]
    for item in soup.findAll('p', attrs={'class':'name product-title'}):
        name.append(item.text.strip())
    price=[]
    for item in soup.findAll('span', attrs={'class':'woocommerce-Price-amount amount'}):
        price.append(item.text.strip())
    m={}
    for x,y in zip(name,price):
        m.update({x:y})
    return m,url


def priyoshop(keyword):
    url="https://priyoshop.com/src?q="+str(keyword)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    ans= soup.findAll('ul', attrs={'class':'search-result-gridview-items'})
    name=[]
    for item in soup.findAll('h2', attrs={'class':'product-title'}):
        name.append(item.text.strip())
    price=[]
    for item in soup.findAll('span', attrs={'class':'price actual-price'}):
        price.append(item.text.strip())
    m={}
    for x,y in zip(name,price):
        m.update({x:y})
    return m,url


# def allmartbd(keyword):
#     url="https://www.allmartbd.com/catalogsearch/result/?q="+str(keyword)
#     r = requests.get(url)
#     soup = BeautifulSoup(r.content, 'lxml')
#     ans= soup.findAll('ul', attrs={'class':'search-result-gridview-items'})
#     name=[]
#     for item in soup.findAll('h2', attrs={'class':'product-name'}):
#         name.append(item.text.strip())
#     price=[]
#     for item in soup.findAll('span', attrs={'class':'price'}):
#         price.append(item.text.strip())
#     m={}
#     for x,y in zip(name,price):
#         m.update({x:y})
#     return m,url

def edokander(keyword):
    url="https://www.edokandar.com/catalogsearch/result/?q="+str(keyword)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    ans= soup.findAll('ul', attrs={'class':'search-result-gridview-items'})
    name=[]
    for item in soup.findAll('h2', attrs={'class':'product-name'}):
        name.append(item.text.strip())
    price=[]
    for item in soup.findAll('span', attrs={'class':'regular-price'}):
        price.append(item.text.strip())
    m={}
    for x,y in zip(name,price):
        m.update({x:y})
    return m,url

def clickxo(keyword):
    url="https://clicxo.com.bd/en/catalogsearch/result/?q="+str(keyword)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    ans= soup.findAll('ul', attrs={'class':'search-result-gridview-items'})
    name=[]
    for item in soup.findAll('a', attrs={'class':'product-item-link'}):
        name.append(item.text.strip())
    price=[]
    for item in soup.findAll('span', attrs={'class':'price'}):
        price.append(item.text.strip())
    m={}
    for x,y in zip(name,price):
        m.update({x:y})
    return m,url

# def megashop(keyword):
#     url="https://www.megashopbd.com/index.php?route=product/search&search="+str(keyword)+"&description=true"
#     r = requests.get(url)
#     soup = BeautifulSoup(r.content, 'lxml')
#     ans= soup.findAll('ul', attrs={'class':'search-result-gridview-items'})
#     name=[]
#     for item in soup.findAll('h4', attrs={'class':'name'}):
#         name.append(item.text.strip())
#     price=[]
#     for item in soup.findAll('p', attrs={'class':'price'}):
#         price.append(item.text.strip())
#     m={}
#     for x,y in zip(name,price):
#         m.update({x:y})
#     return m,url

def ponnobd(keyword):
    url= "https://ponnobd.com/?s="+str(keyword)+"&post_type=product"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    ans= soup.findAll('ul', attrs={'class':'search-result-gridview-items'})
    name=[]
    for item in soup.findAll('div', attrs={'class':'product-loop-title'}):
        name.append(item.text.strip())
    price=[]
    for item in soup.findAll('span', attrs={'class':'woocommerce-Price-amount amount'}):
        price.append(item.text.strip())
    m={}
    for x,y in zip(name,price):
        m.update({x:y})
    return m,url

# def sonalibazar(keyword):
#     url= "https://www.sonalibazar.com/index.php?route=product/search&search="+str(keyword)
#     r = requests.get(url)
#     soup = BeautifulSoup(r.content, 'lxml')
#     ans= soup.findAll('ul', attrs={'class':'search-result-gridview-items'})
#     name=[]
#     for item in soup.findAll('a', attrs={'class':'product-name'}):
#         name.append(item.text.strip())
#     price=[]
#     for item in soup.findAll('div', attrs={'class':'price'}):
#         price.append(item.text.strip())
#     m={}
#     for x,y in zip(name,price):
#         m.update({x:y})
#     return m,url




































    



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
        #text3,url3 = rokomari(keyword)
        #data3=pd.Series(text3).to_frame()
        #pd.DataFrame(data3).to_csv('rokomari.csv')
        #text4,url4 = craiglist(keyword)
        #data4=pd.Series(text4).to_frame()
        #pd.DataFrame(data4).to_csv('craglist.csv')
        text5,url5 = walmart(keyword)
        data5=pd.Series(text5).to_frame()
        pd.DataFrame(data5).to_csv('walmart.csv')


        text6,url6 = shadmart(keyword)
        data6=pd.Series(text6).to_frame()
        pd.DataFrame(data6).to_csv('shadmart.csv')



        #text7,url7 = paytm(keyword)
        #data7=pd.Series(text7).to_frame()
        #pd.DataFrame(data7).to_csv('paytm.csv')


        text8,url8 = shopclus(keyword)
        data8=pd.Series(text8).to_frame()
        pd.DataFrame(data8).to_csv('shopclues.csv')


        text9,url9 = ofuronto(keyword)
        data9=pd.Series(text9).to_frame()
        pd.DataFrame(data9).to_csv('ofuronto.csv')


        text10,url10 = priyoshop(keyword)
        data10=pd.Series(text10).to_frame()
        pd.DataFrame(data10).to_csv('prioshop.csv')

        #text11,url11 = allmartbd(keyword)
        #data11=pd.Series(text11).to_frame()
        #pd.DataFrame(data11).to_csv('allmartbd.csv')


        text12,url12 = edokander(keyword)
        data12=pd.Series(text12).to_frame()
        pd.DataFrame(data12).to_csv('edokander.csv')

        text13,url13 = clickxo(keyword)
        data13=pd.Series(text13).to_frame()
        pd.DataFrame(data13).to_csv('clickxo.csv')

        #text14,url14 = megashop(keyword)
        #data14=pd.Series(text14).to_frame()
        #pd.DataFrame(data14).to_csv('megashop.csv')

        #text15,url15 = ponnobd(keyword)
        #data15=pd.Series(text15).to_frame()
        #pd.DataFrame(data15).to_csv('ponnobd.csv')

        #text16,url16 = sonalibazar(keyword)
        #data16=pd.Series(text16).to_frame()
        #pd.DataFrame(data16).to_csv('sonalibazar.csv')

        
        context = {'text1':text1,'text2':text2,'text5':text5,'text6':text6,'text8':text8,'text9':text9,'text10':text10,'text12':text12,'text13':text13,'url1':url1,'url2':url2,'url5':url5,'url6':url6,'url8':url8,'url9':url9,'url10':url10,'url12':url12,'url13':url13}
        #context = {'text1':text1,'text2':text2,'text3':text3,'text4':text4,'text5':text5,'url1':url1,'url2':url2,'url3':url3,'url4':url4,'url5':url5}
        return render(request,'public/result.html',context)
        #text=daraz(keyword)
        #return HttpResponse(text)