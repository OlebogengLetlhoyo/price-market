import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import time
import sqlite3

conn = sqlite3.connect('test.db')

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
#driver = webdriver.Chrome(ChromeDriverManager().install())

driver.maximize_window()
url = "https://www.pnp.co.za/pnpstorefront/pnp/en/All-Products/Household-%26-Cleaning/Tissues-%26-Toilet-Paper/Toilet-Paper/PnP-Toilet-Paper-2-Ply-White-18s/p/000000000000359011_EA"


def url_exists(url):
    response = requests.get(str(url))
    if response.status_code == 200:
        return 'Web site exists'

    return 'Web site does not exist'


def scrape_site(urls):
    driver.get(str(urls))
    time.sleep(5)
    driver.find_element(By.CLASS_NAME, "close-button").click()
    time.sleep(5)
    normalPrice = driver.find_element(By.CLASS_NAME,"normalPrice").text
    normalPrice = list(normalPrice)
    normalPrice.insert(-2,".")
    normalPrice = ''.join([str(elem) for elem in normalPrice])
    normalPrice = normalPrice.replace("R","")
    product_title = driver.find_element(By.CLASS_NAME,"fed-pdp-product-details-title").text
    return product_title, normalPrice


def create_table():
    try:
        conn.execute('''CREATE TABLE PRODUCTS
            (PRODUCTID INT PRIMARY KEY     NOT NULL,
            PRODUCT_NAME           CHAR(50)    NOT NULL,
            PRODUCT_PRICE            CHAR(50)     NOT NULL);''')
        return True
    except :
        return False


def click_cookie(url):
    driver.get(str(url))
    time.sleep(5)
    driver.find_element(By.NAME, "policiesCloseButton").click()


def add_data(title,price,retailer):
    try:
        conn.execute(f"INSERT INTO PRODUCTS (PRODUCTID,PRODUCT_NAME,PRODUCT_PRICE) \
        VALUES ({2}, '{title}', '{price}')");
        conn.commit()
        return "Data added"
    except:
        return "Failed to add data"


def check_table(table):
    c = conn.cursor()
    c.execute(''' SELECT count(PRODUCT_NAME) FROM PRODUCTS WHERE PRODUCTID=1 ''')
    if c.fetchone()[0]==1: 
        return 'exists'
    else :
        return 'notexist.'




cursor = conn.execute("SELECT PRODUCTID, PRODUCT_NAME, PRODUCT_PRICE FROM PRODUCTS")
for row in cursor:
   print "ID = ", row[0]
   print "NAME = ", row[1]
   print "ADDRESS = ", row[2]
   print "SALARY = ", row[3], "\n"


#print(url_exists(url))
#print(create_table())
#title, price =scrape_site(url)
#print(add_data(title,price,"mac"))
#print(check_table("PRODUCTS"))


