from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

import requests
# import json
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
    # options.add_argument("--headless") # 웹 브라우저 안띄우기
    # options.add_argument("--no-sandbox")
    # options.add_argument("--disable-dev-shm-usage")

    browser = webdriver.Chrome(options = options)
    browser.maximize_window()
    action = ActionChains(browser)

    browser.get(url_list[0])
    WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.XPATH,"//*[@id='root']/div[3]/div[2]/div[2]/section[1]/div/section/div/div[2]/div/div/div/div")))

    products = browser.find_element(By.CLASS_NAME,"fr-ec-product-collection").find_elements(By.CLASS_NAME,"fr-ec-product-tile-resize-wrapper")

    for i in range(len(products)):
        product = products[i]

        # 제품 상세 URL 가져오기
        url = product.find_element(By.TAG_NAME, "a").get_attribute("href")
        browser.get(url)
        time.sleep(10)

        option = browser.find_element(By.XPATH,"//*[@id='root']/div[4]/div/section[1]/div/div[2]")
        # 제품명
        name = option.find_element(By.CLASS_NAME,"fr-ec-gutter-container").find_element(By.TAG_NAME,"ul").find_element(By.TAG_NAME,"h1").text
        print("제품명: "+name+"\n")

        # 색상
        colors = []
        color_list = option.find_element(By.ID,"product-color-picker").find_elements(By.TAG_NAME,"li")
        for color in color_list:
            color_map = {color.find_element(By.TAG_NAME,"input").get_attribute("aria-label") : color.find_element(By.TAG_NAME,"input").get_attribute("value")}
            colors.append(color_map)
        print("색상: "+str(colors)+"\n")

        # 사이즈
        sizes = []
        size_list = option.find_element(By.ID,"product-size-picker").find_elements(By.TAG_NAME,"li")
        for size in size_list:
            sizes.append(size.find_element(By.TAG_NAME,"label").find_element(By.CLASS_NAME,"fr-ec-chip__label-text").text)
        print("사이즈: "+str(sizes)+"\n")

        #가격
        price = option.find_element(By.XPATH,"//*[@id='root']/div[4]/div/section[1]/div/div[2]/div[4]/div[2]/div[1]/div/div/p").text
        print("가격: "+price+"\n")

        time.sleep(3)
        
        # WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "fr-ec-template-pdp"))) 
        # 스크롤 이동하기
        action.move_to_element(browser.find_element(By.XPATH,"//*[@id='productExchangeAndReturnDescription']")).perform()
        time.sleep(2)

        # 제품 상세 / 제품 상세 설명 Click
        gutter_container = browser.find_element(By.XPATH,"//*[@id='root']/div[4]/div/section[1]/div/div[1]/div[2]")
        # gutter_container.find_element(By.TAG_NAME,"button").click()
        time.sleep(2)
        # WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME,"rah-static--height-zero")))
        
        code = gutter_container.find_element(By.CLASS_NAME,"fr-ec-caption").text
        print(code)

        try:
            isProductFeatures = gutter_container.find_element(By.ID,"productFeatures-content")
            if isProductFeatures:
                print("[제품 상세]")
                description_list = []
                descriptions = isProductFeatures.find_elements(By.CLASS_NAME,"fr-ec-content-alignment--direction-row")
                for description in descriptions:
                    description_map = {description.find_element(By.CLASS_NAME,"fr-ec-image").find_element(By.TAG_NAME,"img").get_attribute("src") : description.find_element(By.CLASS_NAME,"fr-ec-content-alignment--direction-column").find_element(By.CLASS_NAME,"fr-ec-body").text}
                    description_list.append(description_map)
                print(description_list)
        except Exception as e:
            print("제품 상세가 존재하지 않습니다.")
      
        try:
            gutter_container.find_element(By.ID,"productLongDescription").click()
            time.sleep(1)
            isProductLongDescription = gutter_container.find_element(By.ID,"productLongDescription-content")
            if isProductLongDescription:
                print("[제품 상세 설명]")
                print(isProductLongDescription.find_element(By.CLASS_NAME,"fr-ec-body").text)
        except Exception as e:
            print("제품 상세 설명이 존재하지 않습니다.")
        
        print("============================================================\n")

        # 상품 리스트 페이지로 돌아가기
        browser.back()

        # 다시 제품 목록 로드 대기
        WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'fr-ec-product-tile-resize-wrapper')]")))
        products = browser.find_elements(By.XPATH, "//div[contains(@class, 'fr-ec-product-tile-resize-wrapper')]")  # 요소를 다시 찾기

    browser.quit()           
crawling()