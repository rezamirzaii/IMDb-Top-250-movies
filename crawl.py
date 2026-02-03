from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

browser = webdriver.Chrome()
headers ={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
    "Accept-Language":"en-US,en;q=0.9"
}
browser.get('https://www.imdb.com/chart/top/?ref_=nv_mv_250')
browser.implicitly_wait(15)
browser.execute_script("window.scrollTo(0,document.body.scrollHeight);")

elements = browser.find_elements(By.XPATH, "//div[@id='__next']//div[@class='ipc-metadata-list-summary-item__c']//h3[@class='ipc-title__text ipc-title__text--reduced']")
link_elems = browser.find_elements(By.XPATH, "//div[@id='__next']//div[@class='ipc-metadata-list-summary-item__c']//a[@class='ipc-title-link-wrapper']")

#for element in elements:
#    print(element.text)
movies_list = [] 
genre_list = [] 
director_list =[]
writer_list =[]
star_list=[]
for element in link_elems[:250]:
    url = element.get_attribute("href")
    page = requests.get(url,headers=headers).text
    soup = BeautifulSoup(page, 'html.parser')
    title = soup.select_one('h1 span').text
    try:
        year = soup.select_one('a[href*="releaseinfo"]').text
    except:
        year = "N/A"
    try:     
        parental_guide = soup.select_one('a[href*="parentalguide"]').text
    except:
        parental_guide = "N/A"  
    try:      
        runtime_h = soup.select_one("div.sc-13687a64-0 ul.ipc-inline-list li.ipc-inline-list__item:nth-of-type(3)").text
        match = re.match(r"(?:(\d+)h)?\s*(?:(\d+)m)?", runtime_h)
        hours = int(match.group(1)) if match.group(1) else 0
        minutes = int(match.group(2)) if match.group(2) else 0
        runtime = hours * 60 + minutes
    except:
        runtime = "N/A"    
    try:
        gross_us_canada = soup.select_one("li.ipc-metadata-list__item.ipc-metadata-list__item--align-end.sc-1c0b0ec6-2.cTBfsm:nth-of-type(2) span.ipc-metadata-list-item__list-content-item.ipc-btn--not-interactable").text
    except:
        gross_us_canada = "N/A"
         
    movies_list.append({
        "MOV-ID": url.split("/")[-2].replace("tt", ""),
        "title": title,
        "year" : year,
        "parental_guide": parental_guide,
        "runtime":runtime,
        "gross_us_canada":gross_us_canada

    })

    genre_all = soup.select("div.ipc-chip-list__scroller a.ipc-chip.ipc-chip--on-baseAlt")
    for x in genre_all:
            genre = x.text
            genre_list.append({
            "MOV-ID": url.split("/")[-2].replace("tt", ""),
            "genre":genre

                    })       

    directore_all = soup.select("div.sc-13687a64-2.knNUTS ul.ipc-metadata-list.ipc-metadata-list--dividers-all  li.ipc-metadata-list__item.ipc-metadata-list__item--align-end:first-of-type \
     div.ipc-metadata-list-item__content-container \
     ul.ipc-inline-list \
     li.ipc-inline-list__item \
     a.ipc-metadata-list-item__list-content-item"
    )
    for x in directore_all:
        director = x.text
        director_ID = x.get("href").split("/")[-2].replace("nm", "")
        director_list.append({
        "MOV-ID": url.split("/")[-2].replace("tt", ""),
        "director_ID":director_ID,
        "director":director


                })
        
    writer_all = soup.select("div.sc-13687a64-2.knNUTS ul.ipc-metadata-list.ipc-metadata-list--dividers-all  li.ipc-metadata-list__item.ipc-metadata-list__item--align-end:nth-of-type(2) \
     div.ipc-metadata-list-item__content-container \
     ul.ipc-inline-list \
     li.ipc-inline-list__item \
     a.ipc-metadata-list-item__list-content-item.ipc-metadata-list-item__list-content-item--link"
    )  
    for x in writer_all:
        writer = x.text
        writer_ID = x.get("href").split("/")[-2].replace("nm", "")
        writer_list.append({
        "MOV-ID": url.split("/")[-2].replace("tt", ""),
        "writer_ID":writer_ID,
        "writer":writer

                })
        
    star_all = soup.select("div.sc-13687a64-2.knNUTS ul.ipc-metadata-list.ipc-metadata-list--dividers-all  li.ipc-metadata-list__item.ipc-metadata-list__item--align-end:nth-of-type(3) \
     div.ipc-metadata-list-item__content-container \
     ul.ipc-inline-list \
     li.ipc-inline-list__item \
     a.ipc-metadata-list-item__list-content-item.ipc-metadata-list-item__list-content-item--link"
    )
    for x in star_all:
        star = x.text
        star_ID = x.get("href").split("/")[-2].replace("nm", "")
        star_list.append({
        "MOV-ID":url.split("/")[-2].replace("tt", ""),
        "star_ID":star_ID,
        "star":star

                })     


def ToExcel(Input,name):
    df = pd.DataFrame(Input)
    df.to_excel(f'{name}.xlsx',index=False)

ToExcel(movies_list,"movie")
ToExcel(genre_list,"genre")  
ToExcel(writer_list,"writer")  
ToExcel(director_list,"director")  
ToExcel(star_list,"star")      

      