# TEST: 1.04

import argparse
import time
import requests
from colored import colored
from requests.auth import HTTPDigestAuth
from bs4 import BeautifulSoup
from termcolor import colored
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
driver = webdriver.Chrome()


def run_up_tests():
    driver.maximize_window()
    try:
        driver.get("http://test1:tester2021@test1.cmps.hce-project.com")

        driver.get("http://test1.cmps.hce-project.com/web")

        driver.find_element(By.ID, "inputEmail").send_keys("master@ioix.com")
        driver.find_element(By.ID, "inputPassword").send_keys("mastertest")
        driver.find_element_by_tag_name("button").click()
        parse()
    except Exception as ex:
        print(ex)


def test_1():
    driver.get("http://test1.cmps.hce-project.com/web")
    try:
        time.sleep(10)
        keywords = driver.find_element(By.CLASS_NAME, "p-links-arrow")
        similarity = driver.find_element(By.CLASS_NAME, "alert-warning").text
        if "K" in similarity:
            similarity = similarity.replace("K", "00")
        similarity = similarity.replace(".", "")
        articles = driver.find_elements_by_class_name("alert-info")[0]
        tw_posts = driver.find_elements_by_class_name("tw_posts")[0]
        tw_retweet = driver.find_elements_by_class_name("tw_retweet")[0]
        tw_likes = driver.find_elements_by_class_name("tw_likes")[0]
        metrics_keyword = {
            # "keywords": keywords.text,
            "similarity": similarity,
            "articles": articles.text,
            "tw_posts": tw_posts.text,
            "tw_retweet": tw_retweet.text,
            "tw_likes": tw_likes.text
        }

        # print(metrics_keyword)
        check(metrics_keyword)
        print("======================")
    except Exception as ex:
        # similarity, articles, tw_posts, tw_retweet, tw_likes = None
        print(ex)


def test_2():
    try:
        keywords = driver.find_element(By.CLASS_NAME, "p-links-arrow")
        time.sleep(7)
        keywords.click()
        time.sleep(12)

        web = driver.find_element(By.ID, "totalNewsCountup").text
        web = web.replace(",", "")
        tv = driver.find_element(By.ID, "totalTvCountup").text
        tv = tv.replace(",", "")
        tweet = driver.find_element(By.ID, "totalTwitterCountup").text
        tweet = tweet.replace(",", "")
        search = driver.find_element(By.ID, "totalSearchCountup").text
        search = search.replace(",", "")
        metrics_ = {
            "web": web,
            "tv": tv,
            "tweet": tweet,
            "search": search
        }
        check(metrics_)
        print("======================")
    except Exception as _ex:
        # web, tv, tweet, search = None
        print(_ex)


def test_3():
    domain_list = []
    domain_list_raw = driver.find_elements(By.CSS_SELECTOR, "span.__media a")
    for item in domain_list_raw:
        domain_list.append(item.text)
        print(item.text)

    count_item = {i: domain_list.count(i) for i in domain_list}
    for k, v in count_item.items():
        print(f"\"{k}\" встречается: {v} раз")


def test_4():
    driver.get("http://test1.cmps.hce-project.com/web")
    domain_list = []
    wait = WebDriverWait(driver, 10)
    keyword = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "p-links-arrow")))
    # keyword = driver.find_elements(By.CLASS_NAME, "p-links-arrow")[0]
    keyword = keyword.text

    driver.find_element(By.CLASS_NAME, "btn__more").click()
    # btn_next = driver.find_element(By.CSS_SELECTOR, "ul.pagination li:nth-last-of-type(1) a")
    count_page = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "ul.pagination li:nth-last-of-type(2) a")))

    count_page = int(count_page.text)
    for i in range(1, count_page + 1):
        url_word = f"http://test1.cmps.hce-project.com/article/archive/domestic/{keyword}?p={i}"

        driver.get(url_word)
        # is_active_next = "disabled" in btn_next.get_attribute("class")
        time.sleep(3)
        # print(is_active_next)
        # if not is_active_next:

        domain_list_raw = driver.find_elements(By.CSS_SELECTOR, "span.__media a")
        for item in domain_list_raw:
            domain_list.append(item.text)
            # btn_next.click()
    print("======================")
    count_item_raw = {i: domain_list.count(i) for i in domain_list}
    count_item = sorted(count_item_raw.items(), key=lambda t: t[1], reverse=True)
    for k, v in count_item:
        print(f"\"{k}\" встречается: {v} раз")


def check(list_raw):
    for key, value in list_raw.items():
        if int(value) > 0:
            print(colored(f"Value of {key} is OK", "green"))
        elif int(value) <= 0:
            print(colored(f"Warning! Value of {key} is not OK", "red"))
        else:
            print(colored(f"Value of {key} not found", "blue"))


def parse():
    parser = argparse.ArgumentParser(
        description='Data processing period: day - daily, week - weekly, month - monthly')

    parser.add_argument('-p', '--period', default="week")
    period = parser.parse_args()
    periods = driver.find_elements(By.CLASS_NAME, "btnChangePeriod")
    is_active_week = "btn-black" in periods[1].get_attribute("class")
    # print("Weekly{}".format(is_active))
    # print(period)
    if not is_active_week:
        periods[1].click()
    if period.period == "day":
        i = 0
        periods[i].click()
    elif period.period == "week":
        i = 1
        periods[i].click()
    elif period.period == "month":
        i = 2
        periods[i].click()


def main():
    run_up_tests()
    test_1()
    test_2()
    test_3()
    test_4()
    driver.close()
    driver.quit()


if __name__ == '__main__':
    main()
