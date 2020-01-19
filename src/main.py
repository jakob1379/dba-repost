from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
import argparse
import progressbar as Pbar
import sys
from getpass import getpass

parser = argparse.ArgumentParser(description="""
dba-repost is a script to repost all ads which are due date from dba.dk""")
parser.add_argument("-t", "--timeout",
                    help="max time to wait for content to appear in webpage",
		    metavar="time",
                    type=int,
		    nargs='?',
                    default=5)

args = parser.parse_args()
maxDelay = args.timeout
email = input("Enter username/email: ")
password = getpass("Enter password: ")

if __name__ == '__main__':

    page = 'https://www.dba.dk'
    inactive_ads = page + '/min-dbadk/mine-annoncer/inaktive-annoncer/'
    login = page + '/log-ind/'

    print('Find login page..')
    driver = webdriver.Firefox()
    driver.get(login)

    print('Fill email...')
    emailField = driver.find_element_by_xpath('//*[@id="Email"]')
    emailField.send_keys(email)

    print('Fill password...')
    pwdField = driver.find_element_by_xpath('//*[@id="Password"]')
    pwdField.send_keys(password)

    print('Enter dba...')
    button = driver.find_element_by_xpath('//*[@id="LoginButton"]')
    button.click()

    print('go to inactive ads...')
    sleep(1)
    driver.get(inactive_ads)

    print('Wait for content...')
    try:
        WebDriverWait(driver, maxDelay).until(
            EC.presence_of_element_located((
                By.XPATH,
                '/html/body/div[1]/div/div[2]/section/div[2]/ul/li[3]/div/span')))
    except TimeoutException:
        print("Max timeout reached!")
        sys.exit()

    print('get inactive ads urls...')
    ads = driver.find_elements_by_xpath(
        "//a[contains(@data-ga-act,'RepostAdBegin')]")
    urls = [elem.get_attribute("href") for elem in ads][:3]

    if urls:
        # While loop is for several pages of inactive ads exists
        counter = 0
        while urls:
            print("reposting ads...")

            pbar = Pbar.ProgressBar(redirect_stdout=True)
            for url in pbar(urls):
                counter += 1

                print(f"reposting: {url}")
                driver.get(url)
                button = driver.find_element_by_xpath(
                    '/html/body/div[1]/div/div[2]/div/div/form/div/button')
                button.click()

                # wait for page to redirect
                try:
                    WebDriverWait(driver, maxDelay).until(
                        EC.presence_of_element_located((
                            By.XPATH,
                            "//div[contains(@id,'listing-owners-toolbox')]")))
                except TimeoutException:
                    print("Max timeout reached!")
                    sys.exit()


            print("Checking for more inactive ads..")
            driver.get(inactive_ads)
            try:
                WebDriverWait(driver, maxDelay).until(
                    EC.presence_of_element_located((
                        By.XPATH,
                        '/html/body/div[1]/div/div[2]/section/table/tbody')))
            except TimeoutException:
                print("Max timeout reached!")
                sys.exit()

            ads = driver.find_elements_by_xpath(
                "//a[contains(@data-ga-act,'RepostAdBegin')]")
            urls = [elem.get_attribute("href") for elem in ads]

        print(f"Finished reposting {counter} ads!")
    else:
        print("No inactive ads!")
    driver.close()
