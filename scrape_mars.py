from splinter import Browser
import time
import pandas as pd
from bs4 import BeautifulSoup

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    # **NASA Mars News**
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(5)
    html = browser.html
    soup= BeautifulSoup(html, "html.parser")

    mars= soup.find("ul", class_="item_list").find("li", class_="slide")
    news_title=mars.find("div", class_="content_title").get_text()

    news_p=mars.find("div", class_="article_teaser_body").get_text()

    # **JPL Mars Space Images**
    url2="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url2)
    time.sleep(10)
    browser.click_link_by_partial_text('FULL IMAGE')
    browser.is_element_present_by_text('more info', wait_time=1)
    html = browser.html
    soup= BeautifulSoup(html, "html.parser")
    jpl=soup.find("img", class_="fancybox-image")["src"]
    img_url="https://www.jpl.nasa.gov"
    featured_img_url=f'{img_url}{jpl}'
    # **Mars Weather**
    url3="https://twitter.com/marswxreport?lang=en"
    browser.visit(url3)
    time.sleep(10)
    html = browser.html
    soup= BeautifulSoup(html, "html.parser")
    abc=soup.find("div", class_="css-1dbjc4n").find("div", class_="css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0")
    mars_weather=abc.find("span", class_="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0").text
    # **Mars Facts**
    url4="https://space-facts.com/mars/"
    tables=pd.read_html(url4)
    df = (tables[0])
    df.set_index(0, inplace=True)
    df=df.rename(columns={1: "Values"})
    df= df.rename_axis(None)
    facts_table=df.to_html()
    facts_table=facts_table.replace("\n","")

    # **Mars Hemispheres**
    url5="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url5)
    time.sleep(5)
    html = browser.html
    soup= BeautifulSoup(html, "html.parser")
    results=soup.find_all("div", class_="item")

    hemisphere_image_urls=[]
    for x in range(4):
        current_item=results[x]
        title=current_item.find("h3").text
        word=title.split(' ', 1)[0]
        browser.click_link_by_partial_text(word)
        time.sleep(3)
        html = browser.html
        soup= BeautifulSoup(html, "html.parser")
        image_url=soup.find("div", class_="downloads").find("ul").find("li").find("a")["href"]
        image_url=image_url.replace("'", "")
        dict_= {"title": title, "img_url": image_url}
        hemisphere_image_urls.append(dict_)

    scrape_dict={"news_title":news_title,
    "news_para":news_p,
    "featured_img_url":featured_img_url,
    "weather":mars_weather,
    "facts":facts_table,
    "hemisphere":hemisphere_image_urls}
    return scrape_dict
