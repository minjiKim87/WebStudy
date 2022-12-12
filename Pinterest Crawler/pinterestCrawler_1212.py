import os

from selenium import webdriver
from tqdm import tqdm
import sys
import urllib.request
from time import sleep
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

driver = webdriver.Chrome('E:\chromedriver_win32\chromedriver')


#링크 고정
driver.get('https://www.pinterest.co.kr/dreamycrysmh/2211~/')
sleep(1)

driver.maximize_window()



#keyword = input('검색어 : ')
maxImages = int(input('다운로드 시도할 최대 이미지 수 : '))

#저장 경로
path = 'crawled_img/'+'2211'+'_'+str(maxImages)

try:
    # 중복되는 폴더 명이 없다면 생성
    if not os.path.exists(path):
        os.makedirs(path)
    # 중복된다면 문구 출력 후 프로그램 종료
    else:
        print('이전에 같은 [검색어, 이미지 수]로 다운로드한 폴더가 존재합니다.')
        sys.exit(0)
except OSError:
    print ('os error')
    sys.exit(0)

imgCount=0
success=0
max_try = maxImages//10
for _ in range(max_try):
    body = driver.find_element(By.CSS_SELECTOR,'body')
    body.send_keys(Keys.PAGE_DOWN)
    body.send_keys(Keys.PAGE_DOWN)
    sleep(1)

    html = driver.page_source
    soup = BeautifulSoup(html,'html.parser')
    imgs = soup.select('div.XiG.zI7.iyn.Hsu img')
    sleep(3)
    for img in imgs:
     srcset = img.get('src') #pinterest에 대체재가 없어서 일단 src저화질로
     if len(srcset):
        src2=str(srcset).split()[0]
        filename = src2.split('/')[-1]
        saveUrl = path+'/'+filename
        print(src2)
        req = urllib.request.Request(src2, headers={'User-Agent': 'Mozilla/5.0'})
        try:
           imgUrl = urllib.request.urlopen(req).read() #웹 페이지 상의 이미지를 불러옴
           with open(saveUrl,"wb") as f: #디렉토리 오픈
            f.write(imgUrl) #파일 저장
            success+=1
        except urllib.error.HTTPError:
            print('에러')
            sys.exit(0)
        #print(success)
        imgCount+=1
        print(imgCount)
        if imgCount == maxImages:
          finish = True
          break

print('성공 : '+str(success)+', 실패 : '+str(maxImages-success))

while(True):
    pass
