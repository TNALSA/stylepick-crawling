from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import requests
import json
import time

# OUTER - [파카&블루종, 재킷, 감탄 재킷, 경량 패딩, 코트, 다운]
url_list = ["https://www.uniqlo.com/kr/ko/men/outerwear/parkas-and-blousons?path=%2C%2C58035%2C", # 파카&블루종
            "https://www.uniqlo.com/kr/ko/men/outerwear/jackets?path=%2C%2C58037%2C", # 재킷
            "https://www.uniqlo.com/kr/ko/men/outerwear/gamtan-jackets?path=%2C%2C58036%2C", # 감탄 재킷
            "https://www.uniqlo.com/kr/ko/men/outerwear/pufftech-and-ultra-light-down?path=%2C%2C58038%2C", # 경량 패딩
            "https://www.uniqlo.com/kr/ko/men/outerwear/coats?path=%2C%2C98233%2C", # 코트
            "https://www.uniqlo.com/kr/ko/men/outerwear/down?path=%2C%2C98234%2C"] # 다운

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Accept-Language":"ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
}

def createSoup(url):
    res = requests.get(url, headers=headers)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "lxml")
    return soup

def crawling():
    # 옵션 추가하기
    options = webdriver.ChromeOptions()
    options.add_argument("--headless") # 웹 브라우저 안띄우기
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    browser = webdriver.Chrome(options = options)
    browser.get(url_list[0])
    WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.XPATH,"//*[@id='root']/div[3]/div[2]/div[2]/section[1]/div/section/div/div[2]/div/div/div/div")))

    products = browser.find_element(By.CLASS_NAME,"fr-ec-product-collection").find_elements(By.CLASS_NAME,"fr-ec-product-tile-resize-wrapper")

    for i in range(len(products)):
            product = products[i]

            # 제품 상세 URL
            url = product.find_element(By.TAG_NAME, "a").get_attribute("href")
            browser.get(url)

            # browser가 출력될 때까지 대기
            WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "fr-ec-template-pdp"))) 

            code = browser.find_element(By.CLASS_NAME,"fr-ec-template-pdp") \
                        .find_element(By.CLASS_NAME,"fr-ec-layout") \
                        .find_element(By.CLASS_NAME,"fr-ec-gutter-container") \
                        .find_element(By.CLASS_NAME,"fr-ec-caption").text

            # 제품 상세 설명 Click
            browser.find_element(By.CLASS_NAME,"fr-ec-template-pdp") \
                        .find_element(By.CLASS_NAME,"fr-ec-layout") \
                        .find_element(By.CLASS_NAME,"fr-ec-gutter-container") \
                        .find_element(By.TAG_NAME,"legend").click()
            WebDriverWait(browser, 20).until(EC.presence_of_all_elements_located((By.ID,"productLongDescription-content")))
         
            description = browser.find_element(By.CLASS_NAME,"fr-ec-template-pdp") \
                        .find_element(By.CLASS_NAME,"fr-ec-layout") \
                        .find_element(By.CLASS_NAME,"fr-ec-gutter-container") \
                        .find_element(By.ID,"productLongDescription-content") \
                        .find_element(By.CLASS_NAME,"fr-ec-body").text
                        
            print(code)
            print(description)

            # 상품 리스트 페이지로 돌아가기
            browser.back()

            # 다시 제품 목록 로드 대기
            WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'fr-ec-product-tile-resize-wrapper')]")))
            products = browser.find_elements(By.XPATH, "//div[contains(@class, 'fr-ec-product-tile-resize-wrapper')]")  # 요소를 다시 찾기
            
            



   

           
           
           



crawling()