#Coursera Rohan Data
import pandas as pd
import time
start_time = time.time()
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

#To open Headless Browser
input_data = pd.read_csv("input.csv")
s = 0
i = 0
data = pd.DataFrame()
for i in range(input_data.shape[0]):
    print(input_data.loc[i,'Category'],",",input_data.loc[i,'Sub_Category'])
    driver = webdriver.Firefox()
    driver.implicitly_wait(30)
    Cat = input_data.loc[i,'Category']
    SubCat = input_data.loc[i,'Sub_Category']
    base_url = "https://www.coursera.org/browse/" + str(input_data.loc[i,'Category']) + "/" + str(input_data.loc[i,'Sub_Category']) + "?languages=en"
    driver.get(base_url)
    time.sleep(4)

    html_source = driver.page_source
    soup = BeautifulSoup(html_source,"lxml")
    page_count = 1
    if(soup.find(class_="Container_1c9hjzi")):
        page_count = soup.find(class_="Container_1c9hjzi").find_all("a")[-2]['data'][5:]
    print("Total Number of pages :",page_count)
    driver.close()
    for k in range(1,int(page_count) + 1):
        print("Page Number : ",k)
        driver = webdriver.Firefox()
        driver.implicitly_wait(30)
        url = base_url + "&page=" + str(k)
        print(url)
        driver.get(url)
        time.sleep(4)
        html_source = driver.page_source
        soup = BeautifulSoup(html_source,"lxml")
        z = 0
        for abc in soup.find_all(class_="offering-content"):
            data.loc[s,'URL'] = "https://www.coursera.org"+ soup.find(class_="bt3-container center-column body").find(class_="bt3-row").find(class_="bt3-col-sm-9 bt3-col-sm-push-3 main-container").find_all("a")[z]["href"]
            data.loc[s,'Image'] = abc.img['srcset']   
            data.loc[s,'Name'] = abc.find(class_="horizontal-box").h2.text
            if(abc.find("span",attrs={"class":"specialization-course-count"})):
                data.loc[s,'Number of Courses'] = abc.find("span",attrs={"class":"specialization-course-count"}).text
            if(abc.find("span",attrs={"class":"text-light offering-partner-names"})):
                data.loc[s,'University'] = abc.find("span",attrs={"class":"text-light offering-partner-names"}).text
            else:
                data.loc[s,'University'] = abc.find(class_="text-light offering-partner-names").text
            data.loc[s,'Category'] = Cat
            data.loc[s,'Sub_Category'] = SubCat
            data.loc[s,'Course_Language'] = "en"
            s = s + 1
            z = z + 1
        driver.close()
        data.to_csv("result.csv")
print(data.head())

