# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
from pprint import pprint
from time import sleep

def scrape():

    # headless=True here when running app

    # This is to initialize Splinter for Mac users...look below for instructions for Windows users
    # https://splinter.readthedocs.io/en/latest/drivers/chrome.html
    # !which chromedriver

    # executable_path = {'executable_path': '/Users/jam/Desktop/chromedriver'}
    # browser = Browser('chrome', **executable_path, headless=True)

    # Hi, Windows user initializing Splinter here...if you're a Mac user, comment this out and use the lines above
    executable_path = {'executable_path': '/Users/jam/Desktop/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=True)
    
    # Run the function below:
    first_title, first_paragraph = mars_news(browser)
    
    # Run the functions below and store into a dictionary
    results = {
        "title": first_title,
        "paragraph": first_paragraph,
        "image_URL": jpl_image(browser),
        "facts": mars_facts(),
        "hemispheres": mars_hemis(browser),
    }

    # Quit the browser and return the scraped results
    browser.quit()
    return results

def mars_news(browser):
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'lxml')

    # Scrape the first article title and teaser paragraph text; return them
    first_title = soup.find('div', class_='content_title').text
    first_paragraph = soup.find('div', class_='article_teaser_body').text
    return first_title, first_paragraph

def jpl_image(browser):
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Go to 'FULL IMAGE', then to 'more info'
    browser.click_link_by_partial_text('FULL IMAGE')
    sleep(1)
    browser.click_link_by_partial_text('more info')

    html = browser.html
    soup = bs(html, 'lxml')

    # Scrape the URL and return
    feat_img_url = soup.find('figure', class_='lede').a['href']
    feat_img_full_url = f'https://www.jpl.nasa.gov{feat_img_url}'
    return feat_img_full_url
    
def mars_facts():
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    df = tables[0]
    df.columns = ['Mars - Earth Comparison', 'Mars', 'Earth']
    # Set index to property in preparation for import into MongoDB
    df.set_index('Mars - Earth Comparison', inplace=True)
    
    # Convert to HTML table string and return
    return df.to_html()
    
def mars_hemis(browser):
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    
    import time 
    html = browser.html
    soup = bs(html, 'lxml')
    mars_hemis=[]

    links = soup.find_all('h3')
    
    for i in range (4):
        time.sleep(4)
        images = browser.find_by_tag('h3')
        images[i].click()
        html = browser.html
        soup = bs(html, 'lxml')
        partial = soup.find("img", class_="wide-image")["src"]
        img_title = soup.find("h2",class_="title").text
        img_url = 'https://astrogeology.usgs.gov'+ partial
        dictionary={"title":img_title,"img_url":img_url}
        mars_hemis.append(dictionary)
        browser.back()
    
    return mars_hemis

if __name__ == "__main__":
    scrape()