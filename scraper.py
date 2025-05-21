import requests
from bs4 import BeautifulSoup
import re
import time
import pandas as pd
 


source_code = requests.get("https://www.law.umich.edu/special/exoneration/Pages/detaillist.aspx")
soup = BeautifulSoup(source_code.content, 'lxml')

link_list = []
for link in soup.findAll('a'):
  new_link = link.get('href')
  link_list.append(new_link)

pruned_link_list = ["https://www.law.umich.edu/special/exoneration/Pages/" + value for value in link_list if 'casedetail' in value]
df = pd.DataFrame(pruned_link_list)

df.to_csv("exhoneration_links.csv")


