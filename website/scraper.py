import requests
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.firefox.options import Options
import time
from dotenv import dotenv_values

env_vars = dotenv_values()

REVIEW_URL = "https://in.indeed.com/cmp/"
NEWS_API_KEY = env_vars['NEWS_API_KEY']
options = Options()
options.headless = False


def get_news(name):
	url = f"https://newsapi.org/v2/everything?q={name}&apiKey={NEWS_API_KEY}"
	response = requests.get(url)
	data = response.json()
	articles = {}
	for i in range(3):
		articles[i] = {"description": data['articles'][i]['description'], "url": data['articles'][i]['url'], "title": data['articles'][i]['title']}
	return articles

def get_reviews(name):
	driver = webdriver.Firefox(executable_path='/Users/varun/Desktop/Projects/geckodriver', options=options)
	driver.get(f'{REVIEW_URL}{name}/reviews?fcountry=ALL')
	time.sleep(5)
	ActionChains(driver).send_keys(Keys.ESCAPE).perform()
	reviews = []
	for i in range(5):
		try:
			xbutton = driver.find_element(By.CSS_SELECTOR, ".gnav-1xqhio")
			xbutton.click()
			time.sleep(3)
		except:
			pass
		time.sleep(5)
		ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
		time.sleep(5)
		print("Looking")
		try:
			review = driver.find_element(By.XPATH, f'/html/body/div[2]/div/div[1]/main/div[2]/div[1]/div/div[{i+1}]/div/div/div[2]/h2/a/span/span/span')
			rating = driver.find_element(By.XPATH, f'/html/body/div[2]/div/div[1]/main/div[2]/div[1]/div/div[{i+1}]/div/div/div[1]/div/button')
			reviewer = driver.find_element(By.XPATH, f'/html/body/div[2]/div/div[1]/main/div[2]/div[1]/div/div[{i+1}]/div/div/div[2]/div[1]/span')
		except:
			pass
		reviews.append({"review": review.text, "rating": rating.get_attribute("aria-label"), "reviewer": reviewer.text})

	driver.quit()
	return reviews
