from django.shortcuts import render,redirect
## this module is for testing
from django.http import HttpResponse

## this is where all the logic goes
import requests
from bs4 import BeautifulSoup

## import json for parsing
import json

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
        b=item.find('div', attrs={'class':'price-box'}).text[:20].strip()
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

def process(request):
    if request.method == "POST":
        ## take the value
        keyword = str(request.POST['keyword'])
        ##return HttpResponse(keyword)
        text1,url1 = Bagdoom(keyword)
        text2,url2 = daraz(keyword)
        
        context = {'text1':text1,'text2':text2,'url1':url1,'url2':url2}
        return render(request,'public/result.html',context)
        #text=daraz(keyword)
        #return HttpResponse(text)