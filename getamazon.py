import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import re
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker

import store

urlheader = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36", "X-Requested-With": "XMLHttpRequest"}
products = pd.read_csv('products.csv')

class GetAmazon:

	def fetch(self):
		soup = []
		for url in products.products:
		    markup = requests.get(url, headers=urlheader).text
		    soup.append(BeautifulSoup(markup, 'html.parser'))


		self.title, self.price, self.manuf, self.brand, self.weight, self.vol, self.score = [], [], [], [], [], [], []
		for s in soup:
		    
		    self.title.append(s.find("span", {"id":"productTitle"}).text.replace('\n',''))
		    
		    self.price.append(float(s.find("span", {"id":"price_inside_buybox"}).text.replace('\n','').replace('$','')))
		    
		    self.manuf.append(s.find_all("td", {"class":"a-size-base prodDetAttrValue"})[0].text.replace('\n',''))
		    
		    self.brand.append(s.find_all("td", {"class":"a-size-base prodDetAttrValue"})[1].text.replace('\n',''))
		    
		    weight_s = s.find_all("td", {"class":"a-size-base prodDetAttrValue"})[2].text
		    weight_s = float(re.search('\d+.\d+', weight_s).group(0))*0.453592
		    self.weight.append(weight_s)
		    
		    dim_s = s.find_all("td", {"class":"a-size-base prodDetAttrValue"})[3].text
		    dim_f = []
		    for n in dim_s.replace('\n','').replace('inches','').replace(' ','').split('x'):
		        dim_f.append(float(n)*2.54)
		    self.vol.append(np.prod(dim_f))
		    
		    score_s = s.find("table", {"id":"productDetails_detailBullets_sections1"}).find_all("tr")[1].find("span", {"class":"reviewCountTextLinkedHistogram noUnderline"})['title']
		    score_f = float(re.search("\d.\d", score_s).group(0))
		    self.score.append(score_f)

	def create_db(self):
		self.engine = create_engine("sqlite:///products.db")
		store.Base.metadata.create_all(self.engine, checkfirst=True)
		Session = sessionmaker(bind=self.engine)
		session = Session()

		p, c = [], []
		for i in range(0,len(self.title)):
		    c1 = store.Characteristics(manufacturer=self.manuf[i], brand=self.brand[i], weight=self.weight[i], volume=self.vol[i], score=self.score[i])
		    p1 = store.Product(name=self.title[i], price=self.price[i], char=c1)
		    p.append(p1)
		    c.append(c1)

		session.add_all(c)
		session.add_all(p)
		session.commit()



