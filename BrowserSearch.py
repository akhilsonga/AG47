#BROWSER!

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
from collections import OrderedDict
from selenium.webdriver.chrome.options import Options

#URL search-------------------------------------------------------------------------------------------------------
def url_browser(url):
    print("Agent url_browser reporting")
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless") 
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)

        elements = driver.find_elements(By.XPATH,"//*[text()]")
        formatted_text = ""
        for element in elements:
            text = element.text.strip()
            if text:
                formatted_text += text + "\n"

        driver.quit()
        print("Report sent -Over 'url_browser'")
    except Exception as e:
        print("Exception Occured, may be AI access Denied",e)
        formatted_text = "Access Denied, Exception occured"
    return formatted_text

#Browser search-------------------------------------------------------------------------------------------------------

def description_filter(text):
    lines = text.split('\n')
    source = lines[1]
    lines[1] = f'from {source}'
    del lines[2]
    modified_text = '\n'.join(lines)
    return modified_text



def Agent02(search_key):
    print("Agent02 Reporting")
    ordered_urls = OrderedDict()
    description_list = []
    
    chrome_options = Options()
    chrome_options.add_argument("--headless") 

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.google.com")

    search_text = "/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/textarea"
    search_list = "/html/body/div[5]/div/div[12]/div/div[2]/div[2]/div/div"

    search_text_button = driver.find_element(By.XPATH, search_text)
    search_text_button.send_keys(search_key)
    search_text_button.send_keys(Keys.ENTER)
    time.sleep(0.5)

    try:
        search_list_tag = driver.find_element(By.XPATH, search_list)
    except Exception as e:
        time.sleep(0.5)
        search_list_tag = driver.find_element(By.XPATH, search_list)


    child_div_elements = search_list_tag.find_elements(By.XPATH, "./div")
    time.sleep(0.5)

    for div in child_div_elements:
        #description_list.append(div.text)
        ref_d = description_filter(div.text)
        description_list.append(ref_d)
        html_content = div.get_attribute('outerHTML')
        soup = BeautifulSoup(html_content, 'html.parser')
        for child in soup.find_all('div', recursive=True):
            for inner_child in child.find_all('div', recursive=True):
                for span in inner_child.find_all('span', recursive=True):
                    for a_tag in span.find_all('a'):
                        href = a_tag.get('href')
                        if href:
                            if href not in ordered_urls:
                                ordered_urls[href] = True
    url_dict = dict(ordered_urls)
    print("Report sent Over! -Agent02")
    return url_dict, description_list
#Browser search-------------------------------------------------------------------------------------------------------

url_dict, description_list = Agent02("python llm code")

print("\n\n\n")  
print(url_dict)
print("\n\n\n")
print(description_list)