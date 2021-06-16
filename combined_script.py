from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import pandas as pd
import random
from instaloader import Instaloader, Profile
from instaloader.exceptions import QueryReturnedNotFoundException, LoginRequiredException,ProfileNotExistsException
import csv
import os.path
import glob

# path = "/Users/anchitshrivastava/Desktop/Tatras Data/Instagram Scrapping/Vietnam csv/"

def clean_profiles(link):
    if "/p/" in link[26:]:
        split_string = link[26:].split("/p",1)
        substring = split_string[0]
    elif "/?" in link[26:]:
        split_string = link[26:].split("/?",1)
        substring = split_string[0]
    elif "tv/" == link[26:29]:
        split_string = link[26:].split("/",1)
        substring = split_string[0]
    else:
        substring=link[26:-1]
        pass
    return "https://www.instagram.com/"+substring+"/"

def clean_unames(uname):
    if "/p/" in uname:
        split_string = uname.split("/p",1)
        substring = split_string[0]
    elif "/?" in uname:
        split_string = uname.split("/?",1)
        substring = split_string[0]
    elif "tv" == uname[:2]:
        split_string = uname.split("/")
        substring = split_string[0]
    else:
        substring=uname
        pass
    return substring

def find_influencers(country_code_dict,keywords,driver_path):
    files_made_list = []
    for country in country_code_dict.keys():
        for keyword in keywords:
            driver = webdriver.Chrome(driver_path)
            print("COUNTRY : ", country)
            # google settings page url
            google_settings_url = 'https://www.google.com/preferences'
            driver.get(google_settings_url)
            time.sleep((random.randint(100, 1000))/100)

            # show all regions on chrome
            show_more = driver.find_element_by_id("regionanchormore")
            show_more.click()
            time.sleep((random.randint(100, 1000))/100)

            # select the specific region
            region = driver.find_element_by_css_selector(
                "div.jfk-radiobutton[data-value=" + country_code_dict[country] + "]")
            region.click()
            time.sleep((random.randint(100, 1000))/100)

            # Save the settings
            save_btn = driver.find_element_by_xpath("//div[text()='Save']")
            save_btn.click()
            time.sleep((random.randint(100, 1000))/100)

            # closing the alert box
            try:
                WebDriverWait(driver, 5).until(EC.alert_is_present())
                #  switch_to.alert for switching to alert and accept
                alert = driver.switch_to.alert
                alert.accept()
                print("alert Exists in page")
            except TimeoutException:
                print("alert does not Exist in page")

            print("Changed Chrome settings")

            print("KEYWORD : ", keyword)
            # Searching Influencer
            insta_profiles = []
            insta_usernames = []
            search_field = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='q']")))
            time.sleep((random.randint(1000, 1500))/100)
            search_field.clear()
            search_field.send_keys("[" + keyword + "] + [" + country + "] + site:instagram.com")
            search_field.send_keys(Keys.ENTER)
            time.sleep((random.randint(100, 1000))/100)

            for page in range(100):
                # collecting urls on a page
                links = driver.find_elements_by_css_selector("div.yuRUbf a")
                for i in range(len(links)):
                    a = links[i].get_attribute("href")
                    if a[:26] == "https://www.instagram.com/" and a[26:34] != "explore/" and a[26:28] != "p/" and a[
                                                                                                                  26:29] != "tv/":
                        if a not in insta_profiles:
                            insta_profiles.append(a)
                            insta_usernames.append(a[26:-1])

                print("LEN OF INSTA PROFILES :", len(insta_profiles))
                if len(insta_profiles) > 500:
                    print("GOT 500")
                    driver.quit()
                    break
                print("COMPLETED PAGE", page + 1)
                print("Moving to next page")
                time.sleep((random.randint(100, 1000))/100)
                try:
                    next_button = driver.find_element_by_xpath('//*[@id="pnnext"]/span[2]')
                    next_button.click()
                except NoSuchElementException as e:
                    print("NO MORE PAGES")
                    time.sleep((random.randint(100, 1000))/100)
                    driver.quit()
                    break
            df1 = pd.DataFrame(insta_profiles, columns=["Insta_Profiles"])
            df2 = pd.DataFrame(insta_usernames, columns=['Insta_Usernames'])
            df = pd.concat([df1, df2], axis=1)
            df.to_csv(country + '_' + keyword + '.csv', index=False)
            files_made_list.append(country + '_' + keyword + '.csv')
            driver.quit()

        combine_csv()


def combine_csv():
    list_of_csv_files = []
    for file in glob.glob("*.csv"):
        list_of_csv_files.append(file)
    print(list_of_csv_files)
    for i , file in enumerate(list_of_csv_files):
        globals()['df'+str(i)] = pd.read_csv(file)
        globals()['df'+str(i)]['category'] = file.split(".")[0]
    list_of_df_created = []
    for i in range(len(list_of_csv_files)):
        list_of_df_created.append(globals()['df'+str(i)])
        # return list_df_created
    df = pd.concat(list_of_df_created,ignore_index=True)
    return get_count(df)


def get_count(file):
    data = pd.read_csv(file)
    output_csv = data.split(".")[0] + "_with_count.csv"
    if not os.path.exists(output_csv):
        csvfile = open(output_csv, 'w', newline='')
        obj = csv.writer(csvfile)
        obj.writerow(
            ('Insta_Profiles', 'Insta_Usernames', 'followers', 'following', 'post_count', 'full_name', 'user_bio'))
    else:
        csvfile = open(output_csv, 'a', newline='')
        obj = csv.writer(csvfile)

    # Getting the profile names
    users = data['Insta_Usernames']
    # Load instaloader
    L = Instaloader()
    count = 1
    for user in users:
        try:
            print("USER", count)
            profile = Profile.from_username(L.context, user)
            profile_url = "https://www.instagram.com/" + user + "/"
            if not profile.is_private and profile.followers > 30:
                print(profile_url)
                followers = profile.followers
                following = profile.followees
                post_count = profile.mediacount
                user_bio = profile.biography
                full_name = profile.full_name
                print(followers, following, post_count)
                print(user_bio, )
                print("==================")
                obj.writerow((profile_url, user, followers, following, post_count, full_name, user_bio))

            else:
                print("PROFILE IS PRIVATE OR HAVE LESS FOLLOWERS")
                print("========================")
        except (QueryReturnedNotFoundException, LoginRequiredException, ProfileNotExistsException):
            print("PROFILE NOT FOUND")
            print("========================")

        count += 1
    csvfile.close()


if __name__ == '__main__':
    country_code_dict = {
        "KSA":"SA",
        "Saudi Arabia":"SA",
        "Egypt":"EG",
        "Iraq":"IQ",
        "Australia":"AU",
        "New Zealand":"NZ",
        "Japan":"JP",
        "Thailand":"TH",
        "Korea":"KR",
        "Hong Kong":"HK",
        "Turkey":"TR",
        "Vietnam":"VN",
        "Philippines":"PH",
        "Malaysia":"MY",
        "Indonesia":"ID"
    }
    keywords = ['vegan food', 'healthyfoodie'] # can add more keywords
    find_influencers(country_code_dict, keywords, driver_path = "/Users/anchitshrivastava/Downloads/chromedriver")
