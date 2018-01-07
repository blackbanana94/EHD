# 이미지 자동 다운로더
import requests
from bs4 import BeautifulSoup
import time
import urllib
import os
import sys

url = input('input url : ')
cookies = {'__cfduid': 'df54c782d8397bb3670a8f0df191c90481512771827', 'eap_45442': '1'}
ex_cookies = {'igneous': 'f01daa63d',
              'ipb_member_id': '816824',
              'ipb_pass_hash': '4835f1467ef9681f775a8e16654f9563',
              'lv': '1512894774-1512894774',
              's': 'bb98cb293',
              'yay': 'louder'}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36 OPR/48.0.2685.35'}
dir_name = ''
img_headers = { 'Accept':'image/webp,image/apng,image/*,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
                'Connection': 'keep-alive',
                'Host': '36.236.160.186:1024',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.97 Safari/537.36 Vivaldi/1.94.1008.34' }

http_proxy  = "http://178.214.74.27:8080"
https_proxy = "https://165.84.167.54:8080"
ftp_proxy   = "ftp://10.10.1.10:3128"

proxy_dict = {
              # "http"  : http_proxy,
              "https" : https_proxy
}
global_timeout = 40


def get_img(img_page_addr, isBlocked=False):
  try:
    img_session = requests.Session()
    if isBlocked:
      img_session.proxies.update(proxy_dict)
    img_page = img_session.get(img_page_addr, headers=headers, cookies=ex_cookies, timeout=global_timeout)
    print(img_page.status_code)
    soup = BeautifulSoup(img_page.content, 'html.parser')
    img_tag = soup.find_all('img', id='img')
    img_src = img_tag[0]['src']
    if(img_src == 'https://exhentai.org/img/509.gif'):
      print("Bandwidth Error! sleep 1 seconds and try with proxy...")
      sys.stdout.flush()
      time.sleep(1)
      return get_img(img_page_addr, True)
    return s.get(img_src, headers=img_headers, cookies=ex_cookies, timeout=global_timeout)
  except ConnectionError:
    time.sleep(1)
    return get_img(img_page_addr, isBlocked)
  except Exception:
    time.sleep(1)
    return get_img(img_page_addr, isBlocked)



requests.adapters.DEFAULT_RETRIES = 5

# url = url.replace("exhentai", "e-hentai", 1)

s = requests.Session()

page = s.get(url, headers=headers, cookies=ex_cookies, timeout=global_timeout)
print(page.status_code)
print(page.headers)

soup = BeautifulSoup(page.content, 'html.parser')

a_tags = soup.find_all("a")
for a in a_tags:
  if "View Gallery" in a:
    page = s.get(a['href'], headers=headers, cookies=ex_cookies, timeout=global_timeout)
    soup = BeautifulSoup(page.content, 'html.parser')

gdts = soup.find_all(class_="gdt2")
pages = gdts[5].text.split()[0]
print("pages : {0}".format(pages))

total_page_num = int((int(pages) / 40))
if (int(pages) % 40) != 0:
  total_page_num += 1
print("total_page_num : {0}".format(total_page_num))

title = soup.find_all('h1', id='gn')[0].text
title = title.replace('|', '')
title = title.replace('?', '')
title = title.replace('<', '(')
title = title.replace('>', ')')
title = title.replace('/', '')
title = title.replace(':', '')
title = title.replace('*', '')
title = title.replace('\"', '')
if(not os.path.exists('./{0}'.format(title))):
  os.system("xcopy SKEL \"{0}\\\" /H /K".format(title))

img_num = 1

for p in range(0, total_page_num):
  page = s.get(url+'?p={0}'.format(p), headers=headers, cookies=ex_cookies, timeout=global_timeout)
  soup = BeautifulSoup(page.content, 'html.parser')

  gdtm = soup.find_all(class_="gdtm")
  print(gdtm)
  print(type(gdtm))
  for i in range(0, len(gdtm)):
    if(os.path.exists('./{0}/{1}.jpg'.format(title, img_num))):
      print('skipping {0}.jpg ...'.format(img_num))
      img_num += 1
      continue
    a_tags = gdtm[i].find_all("a")
    print(a_tags[0]['href'])
    img_page_addr = a_tags[0]['href']

    img_session = requests.Session()
    img_page = img_session.get(img_page_addr, headers=headers, cookies=ex_cookies, timeout=global_timeout)
    print(img_page.status_code)
    soup = BeautifulSoup(img_page.content, 'html.parser')
    img_tag = soup.find_all('img', id='img')
    img_src = img_tag[0]['src']

    # host_info = img_src.replace('http://', '')
    # host_info = host_info.split('/')[0]
    # img_headers['Host'] = host_info
    img_res = get_img(img_page_addr)

    f = open('{0}/{1}.jpg'.format(title, img_num), 'wb')
    f.write(img_res.content)
    f.close()
    img_num += 1
    time.sleep(0.5)

print('trying to make icon')
if len(os.listdir('./{0}/'.format(title))) == (int(pages)+1):
  os.system('magick convert "{0}\{1}" -resize 256x256 -gravity center -background transparent -extent 256x256 "{0}\icon.ico"'.format(title, "1.jpg"))
