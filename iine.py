# coding: utf-8
import os
import time
from platform import system as getos

from selenium import webdriver

work_dir = os.path.dirname(os.path.abspath(__file__))


def chrome_driver():
    os_type = getos()
    if os_type == "Windows":
        return os.path.join(work_dir, "driver", "chromedriver.exe")
    elif os_type == "Linux":
        return os.path.join(work_dir, "driver", "chromedriver_linux")
    elif os_type == "Darwin":
        return os.path.join(work_dir, "driver", "chromedriver_mac")
    else:
        return None


def ameblo_inne(username, password, target_url):
    driver = chrome_driver()
    if os.path.exists(driver) is False:
        print("No Driver.")
        exit()

    headers = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
    chrome_options = webdriver.ChromeOptions()
    # 自定义UA
    chrome_options.add_argument('user-agent={}'.format(headers))
    # 设置无头模式
    chrome_options.add_argument("--headless")
    # 设置代理地址
    # chrome_options.add_argument('--proxy-server=http://127.0.0.1:1080')
    browser = webdriver.Chrome(chrome_options=chrome_options, executable_path=driver)

    # 登录
    ameblo_login_url = "https://dauth.user.ameba.jp/ameba/login"
    browser.get(ameblo_login_url)

    browser.find_element_by_name("accountId").send_keys(username)
    time.sleep(2)
    browser.find_element_by_name("password").send_keys(password)
    time.sleep(2)
    browser.find_element_by_css_selector("input.c-btn").click()

    # 点赞
    browser.get(target_url)
    # 将滚动条移动到点赞区域
    js = browser.find_element_by_xpath('//div[@class="skin-entryFooter"]')
    browser.execute_script("arguments[0].scrollIntoView(false);", js)

    # いいね！
    time.sleep(5)
    browser.find_element_by_xpath('//div[@class="skin-entryFooter"]/div/div/p/a').click()
    browser.close()


def main():
    username = ""
    password = ""
    target_url = "https://ameblo.jp/yoshinekyoko/entry-12474800455.html"
    ameblo_inne(username, password, target_url)


if __name__ == "__main__":
    main()
