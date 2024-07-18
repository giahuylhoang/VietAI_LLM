#%%
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# Set up Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode to avoid opening a browser window
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
service = Service('/usr/local/bin/chromedriver')  # Update with the path to your chromedriver

driver = webdriver.Chrome(service=service, options=chrome_options)

# Block link

main_link = "https://www.llamaindex.ai/blog"

# Open the blog page
driver.get(main_link)

# Scroll to the bottom of the page to load all content
SCROLL_PAUSE_TIME = 2
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to the bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    # Wait to load the page
    time.sleep(SCROLL_PAUSE_TIME)
    
    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Get page source and parse with BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Close the WebDriver
driver.quit()

# Extract all blog links
blog_links = []
for a_tag in soup.find_all('a', href=True):
    href = a_tag['href']
    if '/blog/' in href:
        blog_links.append(href)

# Remove duplicates and print the blog links
blog_links = list(set(blog_links))
for link in blog_links:
    print(link)

# Extract the content of the first blog post


def has_blogpost_date_class(tag):
    return tag.has_attr('class') and any('BlogPost_date' in cls for cls in tag['class'])

def has_blogpost_title_class(tag):
    return tag.has_attr('class') and any('BlogPost_title' in cls for cls in tag['class'])

def has_blogpost_tags_class(tag):
    return tag.has_attr('class') and any('BlogPost_tags' in cls for cls in tag['class'])

def has_blogpost_content_class(tag):
    return tag.has_attr('class') and any('BlogPost_htmlPost' in cls for cls in tag['class'])

def has_blogpost_relatedposts_class(tag):
    return tag.has_attr('class') and any('BlogPost_relatedPostsList' in cls for cls in tag['class'])


blog_contents = []

# parse the first blog post using beautifulsoup
for blog_link in blog_links:
    print(f"Extracting content for blog post: {blog_link}")
    blog_link = main_link + "/" + blog_link.split("/blog")[1]
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(blog_link)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

     # Find all elements that match the criteria
    elements_with_blogpost_date = soup.find_all(has_blogpost_date_class)
    elements_with_blogpost_title = soup.find_all(has_blogpost_title_class)
    elements_with_blogpost_tags = soup.find_all(has_blogpost_tags_class)
    elements_with_blogpost_content = soup.find_all(has_blogpost_content_class)
    elements_with_blogpost_relatedposts = soup.find_all(has_blogpost_relatedposts_class)


    # extract out the content of the first blog post
    try:
        date_author = elements_with_blogpost_date[0].get_text()
        try:
            date = date_author.split(' • ')[1].strip()
        except:
            date = date_author
            author = ""
    except:
        date = ""
        author = ""
    
    author = date_author.split(' • ')[0].strip()
    title = elements_with_blogpost_title[0].get_text()
    content = elements_with_blogpost_content[0].get_text()

    # extract out the related base on the the text of the a tag
    try:
        tags = [tag['href'].split('/')[-1] for tag in elements_with_blogpost_tags[0].find_all('a')]
    except IndexError:
        tags = []
    try:
        related_posts = [post.get_text() for post in elements_with_blogpost_relatedposts[0].find_all('a')]
    except IndexError:
        related_posts = []

    blog_contents.append({
        'date': date,
        'author': author,
        'title': title,
        'tags': tags,
        'content': content,
        'related_posts': related_posts,
        'link': blog_link,
    })
    

    import json
    with open('blog_contents.json', 'w') as f:
        json.dump({"blog_posts": blog_contents}, f, indent=4)

    print(f"Extracted content for blog post: {title}")
#dump the blog contents to a json file
import json
with open('blog_contents.json', 'w') as f:
    json.dump({"blog_posts": blog_contents}, f, indent=4)




# %%
