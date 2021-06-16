from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import pandas as pd
import random

# import requests
# from stem import Signal
# from stem.control import Controller

# country_code_dict = {"KSA":"SA",
#                     "Saudi Arabia":"SA",
#                     "Egypt":"EG",
#                     "Iraq":"IQ"
#                     "Australia":"AU",
#                     "New Zealand":"NZ",
#                     "Japan":"JP",
#                     "Thailand":"TH",
#                     "Korea":"KR",
#                     "Hong Kong":"HK",
#                     "Turkey":"TR","Korea":"KR",
                    # "Hong Kong":"HK",
#                     "Vietnam":"VN",
#                     "Philippines":"PH",
#                     "Malaysia":"MY",
#                     "Indonesia":"ID"
#                     }

# country_code_dict = {
#                     "Korea":"KR",
#                     "Hong Kong":"HK",
#                     "Turkey":"TR"and a[26:29]!="tv/"
#                     }
# country_code_dict = {
#                     "Philippines":"PH",
#                     "Malaysia":"MY",
#                     "Indonesia":"ID"
#
#                     }
country_code_dict = {
    "Hong Kong":"HK"
}

# Cooking,  dessert, food blogger, foodie, instafood
keywords = ['美食博客','美食家','美食博客','美食家','美食家','素食主义者','健康美食家']



for keyword in keywords:
    for country in country_code_dict.keys():
        driver = webdriver.Chrome("/Users/anchitshrivastava/Downloads/chromedriver")
        print("COUNTRY : ",country)
        # google settings page url
        google_settings_url = 'https://www.google.com/preferences'
        driver.get(google_settings_url)
        time.sleep(random.randint(2,10))

        # show all regions on chrome
        show_more = driver.find_element_by_id("regionanchormore")
        show_more.click()
        time.sleep(random.randint(2,10))

        # select the specific region
        region = driver.find_element_by_css_selector("div.jfk-radiobutton[data-value="+country_code_dict[country]+"]")
        region.click()
        time.sleep(random.randint(2,10))

        # Save the settings
        save_btn = driver.find_element_by_xpath("//div[text()='Save']")
        save_btn.click()
        time.sleep(random.randint(2,10))

        # closing the alert box
        try:
            WebDriverWait(driver, 5).until (EC.alert_is_present())
            #  switch_to.alert for switching to alert and accept
            alert = driver.switch_to.alert
            alert.accept()
            print("alert Exists in page")
        except TimeoutException:
            print("alert does not Exist in page")

        print("Changed Chrome settings")



        print("KEYWORD : ",keyword)
        # Searching Influencer
        insta_profiles = []
        insta_usernames = []
        search_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='q']")))
        time.sleep(random.randint(10,15))
        search_field.clear()
        search_field.send_keys("[" + keyword +"] + [" + country + "] + site:instagram.com")
        search_field.send_keys(Keys.ENTER)
        time.sleep(random.randint(2,10))

        for page in range(100):
            # collecting urls on a page
            links = driver.find_elements_by_css_selector("div.yuRUbf a")
            for i in range(len(links)):
                a=links[i].get_attribute("href")
                if a[:26]=="https://www.instagram.com/" and a[26:34]!="explore/" and a[26:28]!="p/" and a[26:29]!="tv/":
                    if a not in insta_profiles:
                        insta_profiles.append(a)
                        insta_usernames.append(a[26:-1])

            print("LEN OF INSTA PROFILES :",len(insta_profiles))
            if len(insta_profiles)>500:
                print("GOT 500")
                driver.quit()
                break
            print("COMPLETED PAGE", page + 1)
            print("Moving to next page")
            time.sleep(random.randint(2,10))
            try:
                next_button = driver.find_element_by_xpath('//*[@id="pnnext"]/span[2]')
                next_button.click()
            except NoSuchElementException as e:
                print("NO MORE PAGES")
                time.sleep(random.randint(2,10))
                driver.quit()
                break
        df1 = pd.DataFrame(insta_profiles,columns=["Insta_Profiles"])
        df2 = pd.DataFrame(insta_usernames,columns=['Insta_Usernames'])
        df = pd.concat([df1,df2],axis=1)
        df.to_csv(country+'_'+keyword+'.csv',index=False)
        driver.quit()
    time.sleep((random.randint(4000,5000))/100)