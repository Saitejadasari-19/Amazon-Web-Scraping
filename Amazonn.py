import requests
from bs4 import BeautifulSoup
from time import sleep

import pandas as pd


user_agents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36'
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'
'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36'
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.83 Safari/537.1']


cookie={} 
# We are getting the reponse based on the search query
def getAmazonSearch(search_query):
    url="https://www.amazon.in/s?k="+search_query
    for agent in user_agents:
      header={'User-Agent': agent}
      print(url)
      page=requests.get(url,cookies=cookie,headers=header)
      if page.status_code==200:
          return page
      else:
          continue
      
# ASIN stands for Amazon Standard Identification Number.Almost every product has its own ASIN,a unique code we use to identify it.
def Searchasin(asin):
    url="https://www.amazon.in/dp/"+asin
    print(url)
    for agent in user_agents:
      header={'User-Agent': agent}
      page=requests.get(url,cookies=cookie,headers=header)
      if page.status_code==200:
          return page
      else:
          continue
    return "Error"

    
# This will return the next page URL
def getnextpage(soup):
    pages = soup.find('span', {'class': 's-pagination-strip'})
    if not pages.find('span', {'class': 's-pagination-item s-pagination-next s-pagination-disabled'}):
        ref = pages.find('a', {'class': 's-pagination-item s-pagination-next s-pagination-button s-pagination-separator'})['href']
        url = 'https://www.amazon.in' + str(ref)
        return url
    else:
        return


response=getAmazonSearch('iphone+all+mobiles')
soup=BeautifulSoup(response.content,features="html.parser")
urls = []
for i in range(2):
    url = getnextpage(soup)
    if not url:
        break
    for agent in user_agents:
      header={'User-Agent': agent}
      response=requests.get(url,cookies=cookie,headers=header)
    soup=BeautifulSoup(response.content,features="html.parser")
    urls.append(url)

# Getting ASIN numbers for the products in the urls taken
data_asin = []
for url in urls:
  page=requests.get(url,cookies=cookie,headers=header)
  soup=BeautifulSoup(page.content,features="html.parser")
  for i in soup.findAll("div",{'class':"sg-col-20-of-24 s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col s-widget-spacing-small sg-col-12-of-16"}):
    data_asin.append(i['data-asin'])

data = {'URLS': urls}
df_url = pd.DataFrame(data)
df_url.to_csv('URLs.csv')


# In this code we are scraping the Products data
link=[]
Product_title= []
Product_cost = []
Product_rating = []
Product_descrtipion = []
updated_asin = []
Total_ratings = []
print(len(data_asin))
for i in range(len(data_asin)):
    response=Searchasin(data_asin[i])
    print(response)
    if response == "Error":
      continue
    soup=BeautifulSoup(response.content,features="html.parser")
    
    title = soup.find("span",{"class":'a-size-large product-title-word-break'})
    if title == None:
      continue
    price = soup.find("span",{"class":'a-price-whole'})
    if price == None:
      continue
    description_response = soup.find("ul",{"class":'a-unordered-list a-vertical a-spacing-mini'}) #Here we search initally with the parent tag
    if description_response == None:
      continue
    description = ""
    for desc in description_response.findAll("span",{"class":'a-list-item'}): #from the response of parent tag we search the children
      description += desc.get_text().strip()+"\n"
    if description == "":
      continue
    
    
    updated_asin.append(data_asin[i])
    Product_title.append(title.get_text().strip())
    Product_cost.append(price.get_text().strip())
    Product_descrtipion.append(description)
    sleep(10)


# Stroing ASIN, Product details and links in a dataframe. 
data = {'ASIN':updated_asin,
        'Product Title': Product_title,
        'Product Description': Product_descrtipion,
        
        }

 
df = pd.DataFrame(data)
 
print(df.head())

df.to_csv("Product_details.csv")