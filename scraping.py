#Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import time

data = {}

def scrape_all():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    mars_news(browser)
    featured_image(browser)
    mars_facts()
    hemispheres(browser)

    browser.quit()

    return data


# Visit the Mars news site
def mars_news(browser):
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    slide_elem = news_soup.select_one('div.list_text')

    slide_elem.find('div', class_='content_title')

    # Use the parent element to find the first a tag and save it as `news_title`
    news_title = slide_elem.find('div', class_='content_title').get_text()
    data["news_title"] = news_title

    # Use the parent element to find the paragraph text
    news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    data["news_paragraph"] = news_p

    return

# ## JPL Space Images Featured Image
def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # find the relative image url
    img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    # Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    data["featured_image"] = img_url

    return

# ## Mars Facts
def mars_facts():
    df = pd.read_html('https://galaxyfacts-mars.com')[0]

    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    data["facts"] = df.to_html(index=False)

    return

def hemispheres(browser):
    url = (
        "https://astrogeology.usgs.gov/search/"
        "results?q=hemisphere+enhanced&k1=target&v1=Mars"
    )

    browser.visit(url)
    browser.is_element_present_by_text(
        "USGS Astrogeology Science Center", wait_time=1)
    
    hemisphere_image_urls = []
    for i in range(4):
        hemisphere = {}
        browser.find_by_css("a.product-item h3")[i].click()
        time.sleep(1)
        html = browser.html
        hemi_soup = soup(html, "html.parser")
        hemisphere['img_url'] = hemi_soup.find("a", text="Sample").get("href")
        hemisphere['title'] = hemi_soup.find("h2", class_="title").get_text()
        hemisphere_image_urls.append(hemisphere)
        browser.back()
    
    data["hemispheres"] = hemisphere_image_urls

    return

if __name__ == "__main__":  
    print() 

