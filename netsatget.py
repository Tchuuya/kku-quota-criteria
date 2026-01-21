import requests,json,time,random
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

a="https://apps.admissions.kku.ac.th/web/"
b="https://apply.kku.ac.th/programsearch68/showprogram2_x.php?acadyear=2568&code=&id="
h={'User-Agent':'Mozilla/5.0'}

s=requests.Session()
s.headers.update(h)

def g(i):
 try:
  r=s.get(b+str(i),timeout=8);r.encoding='utf-8'
  p=BeautifulSoup(r.text,'html.parser');m={}
  for t in p.find_all('tr'):
   d=t.find_all('td')
   if len(d)>=5:
    m[d[1].text.strip()]={"max":d[2].text.strip(),"min":d[3].text.strip(),"avg":d[4].text.strip()}
  time.sleep(random.uniform(.1,.3))
  return m
 except:return {}

def f(u):
 try:
  r=s.get(u,timeout=8);r.encoding='utf-8'
  p=BeautifulSoup(r.text,'html.parser');z=[]
  t=p.find('table',class_='subjects-table')
  if t:
   for y in t.find('tbody').find_all('tr'):
    d=y.find_all('td')
    if len(d)>=4:
     z.append({"code":d[0].text.strip(),"name":d[1].text.strip(),"weight":float(d[3].find('span').text.strip())})
  time.sleep(random.uniform(.1,.4))
  return z
 except:return []

def main():
 m={}
 with ThreadPoolExecutor(max_workers=4) as e:
  for x in e.map(g,[2,3,4,5,6,7,8,9,11,13,15,16,18,20,21,22,27,28,29,32,38,45]):
   m.update(x)

 r=s.get(a+"Quota",timeout=10);r.encoding='utf-8'
 p=BeautifulSoup(r.text,'html.parser');o=[]
 rows=p.find_all('tr',class_='table-row')

 with ThreadPoolExecutor(max_workers=5) as e:
  u=[a+x.find('a',class_='view-link')['href'] for x in rows]
  c=list(e.map(f,u))

 for x,z in zip(rows,c):
  n=x.get('data-program').strip()
  o.append({
   "faculty":x.get('data-faculty'),
   "major":n,
   "criteria":z,
   "stats_68":m.get(n,{"max":"-","min":"-","avg":"-"}),
   "url":a+x.find('a',class_='view-link')['href']
  })

 open("kku_quota_data.json","w",encoding="utf-8").write(
  json.dumps(o,ensure_ascii=False)
 )

if __name__=="__main__":
 main()
