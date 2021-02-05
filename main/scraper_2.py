from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time


class AnyEc:
    """ Use with WebDriverWait to combine expected_conditions
        in an OR.
    """
    def __init__(self, *args):
        self.ecs = args
    def __call__(self, driver):
        for fn in self.ecs:
            try:
                if fn(driver): return True
            except:
                pass


driver = webdriver.Chrome()

driver.get("https://www.robinhood.com/account/history")

#need to surround this in try-catch in case we navigate to wrong page and we get a timeout exception
WebDriverWait(driver, 20).until(AnyEc(
    EC.presence_of_element_located((By.CLASS_NAME, "css-19gyy64")),
    EC.presence_of_element_located((By.CLASS_NAME, "rh-expandable-item-a32bb9ad"))
    )
)

if (EC.presence_of_element_located((By.CLASS_NAME, "css-19gyy64"))):
    print("we're at the login page")
else:
    print("we're at the account page")


#WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "css-19gyy64")))
#^is for detecting login page

