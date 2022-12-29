import requests
from random import randint
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import asyncio

global url
url = 'https://www.craiyon.com/'

async def workAI(prompt, wait=80): ## cur using selenium here
    driver = webdriver.ChromiumEdge()
    driver.get(url)
    await asyncio.sleep(3)
    driver.execute_script("window.scrollTo(0, 300)")
    await asyncio.sleep(5)
    prompt= driver.find_element(By.ID, "prompt").send_keys(prompt)
    genButton = driver.find_element(By.ID, "generateButton")
    genButton.click()

    await asyncio.sleep(wait)

    if(driver.find_element(By.ID, "closeIconHit") != None):
        driver.find_element(By.ID, "closeIconHit").click()
        await asyncio.sleep(5)
        driver.save_screenshot("result.png")
        await asyncio.sleep(5)

        driver.quit()
    else:

        await asyncio.sleep(5)
        driver.save_screenshot("result.png")
        await asyncio.sleep(5)

        driver.quit()
    
def giveQuot():
    response = requests.get('https://citaty.info/random')
    soup = BeautifulSoup(response.text, 'lxml')
    quotes = soup.find_all('div', class_='field-item even last')
    
    generating = True
    
    while generating:
        #rand_quot = randint(0, len(quotes))
        for quot in range(0, len(quotes)):
            quot_text = quotes[quot].find_all('p')

            for sing_text in quot_text:
                if (sing_text == ''):
                    continue
                else:
                    return(sing_text.text + '\n')
                    
        
    
