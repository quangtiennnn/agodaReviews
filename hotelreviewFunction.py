import pandas as pd
import time
import os
import csv

from selenium import webdriver
from selenium.webdriver.common.by import By
# from seleniumFunction import *
from selenium.webdriver.chrome.options import Options


# ==================== GLOBAL VARIABLES
# Set Chrome options:
chrome_options = Options()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox') 
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-application-cache")
chrome_options.add_argument("--disable-cache")
chrome_options.add_argument("--disk-cache-size=0")

city = pd.read_csv('city.csv')


def reviewInfomation(driver: webdriver):
    reviews = driver.find_elements(By.CSS_SELECTOR, 'div[data-element-name="review-comments"] div[data-review-id]')
    review_id = [review.get_attribute("data-review-id") for review in reviews]
    data = []
    for id in set(review_id):
        elem = driver.find_element(By.CSS_SELECTOR, f'div[data-review-id="{id}"]')
        # ReviewersInfo
        try:
            reviewersInfo = elem.find_element(By.CSS_SELECTOR, 'div[data-info-type="reviewer-name"]')
            info = reviewersInfo.text.split(" ")
            reviewername = info[0]
            national = " ".join(info[2:])
        except:
            reviewername = ''
            national = ''
        # GroupsName
        try:
            groupname = elem.find_element(By.CSS_SELECTOR, 'div[data-info-type="group-name"]').text
        except:
            groupname = ''

        # RoomTypes
        try:
            roomtype = elem.find_element(By.CSS_SELECTOR, 'div[data-info-type="room-type"]').text
        except:
            roomtype = ''

        # StaysDetail
        try:
            staydetail = elem.find_element(By.CSS_SELECTOR, 'div[data-info-type="stay-detail"]').text
        except:
            staydetail = ''
            
        # Review Title:
        try:   
            reviewtitle = elem.find_element(By.CSS_SELECTOR, 'h3[data-testid="review-title"]').text
        except:
            reviewtitle = ''

        # Comments
        try:
            comment = elem.find_element(By.CSS_SELECTOR, 'p[data-selenium="comment"]').text
        except:
            comment = ''
        
        try:
            pos_comment = elem.find_element(By.CSS_SELECTOR, 'div[data-selenium="positive-comment"]').text.split('\n')[1]
        except:
            pos_comment = ''
        
        try:
            neg_comment = elem.find_element(By.CSS_SELECTOR, 'div[data-selenium="negative-comment"]').text.split('\n')[1]
        except:
            neg_comment = ''
        
        
        # Scores
        try:
            score = elem.find_element(By.CSS_SELECTOR, 'div[class="Review-comment-leftScore"]').text
        except:
            score = ''

        new_data = [reviewername,national,groupname,roomtype,staydetail,reviewtitle,comment,pos_comment,neg_comment,score]

        # Add new data to the existing list
        data.append(new_data)
    return data

def url_edited(url):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(2)
    elem = driver.find_element(By.CSS_SELECTOR, "a[data-element-name='property-card-content']")
    href = elem.get_attribute('href')
    return href.replace('https://www.agoda.com/','https://www.agoda.com/vi-vn/')


def hotelReviews(id:str,city):
    driver = webdriver.Chrome()
    old_url = city[city.hotel_id == int(id)].url.iloc[0]
    driver.get(url_edited(old_url))
    
    filepath = f'hotelReviews/{id}.csv'

    if len(filepath.split('/')) > 1:
        directory = '/'.join(filepath.split('/')[:-1])
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    data = ['reviewername','national','groupname','roomtype','staydetail','reviewtitle','comment','positive','negative','score']
    with open(filepath, mode='a', newline='',encoding='utf-8-sig') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(data)
    try:
        button = driver.find_element(By.CSS_SELECTOR, 'i.ficon.ficon-24.ficon-carrouselarrow-right')
        # Move it to button element to able to click
        driver.execute_script("arguments[0].scrollIntoView(); window.scrollBy(0, -200);", button)
        time.sleep(2)
        while True:
            try:
                data = reviewInfomation(driver)
                print(data)
                with open(filepath, mode='a', newline='',encoding='utf-8-sig') as file:
                    csv_writer = csv.writer(file)
                    csv_writer.writerows(data)
                time.sleep(2)
                button.click()
                time.sleep(2)
                
            except Exception as e:
                print(e)
                break
    except:
        pass
     