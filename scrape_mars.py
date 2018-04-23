
# coding: utf-8

# In this assignment, you will build a web application that scrapes various websites for data related to the Mission to Mars and displays the information in a single HTML page. The following outlines what you need to do.
# 
# Step 1 - Scraping
# 
# Complete your initial scraping using Jupyter Notebook, BeautifulSoup, Pandas, and Requests/Splinter.
# 
# Create a Jupyter Notebook file called mission_to_mars.ipynb and use this to complete all of your scraping and analysis tasks. The following outlines what you need to scrape.
# NASA Mars News
# 
# Scrape the NASA Mars News Site and collect the latest News Title and Paragragh Text. Assign the text to variables that you can reference later.
# # Example:
# news_title = "NASA's Next Mars Mission to Investigate Interior of Red Planet"
# 
# news_p = "Preparation of NASA's next spacecraft to Mars, InSight, has ramped up this summer, on course for launch next May from Vandenberg Air Force Base in central California -- the first interplanetary launch in history from America's West Coast."
# 

# In[1]:


#Dependencies
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import pandas as pd


# In[2]:


# URL of Python reddit
url = 'https://mars.nasa.gov/news'


# In[3]:


# Retrieve page with the requests module
html = requests.get(url)


# In[4]:


# Create BeautifulSoup object; parse with 'html.parser'
soup1 = bs(html.text, 'html.parser')


# In[5]:


print(soup1.prettify())


# In[6]:


# Extract title text
title = soup1.title.text
print(title)


# In[7]:


# results are returned as an iterable list
results = soup1.find_all('div', class_="slide")

# Loop through returned results
for result in results:
    # Error handling
    try:
        # Identify and return title of listing
        news_title = result.find('div', class_="content_title").text
        # Identify and return paragraph/text of listing
        news_p = result.find('div',class_="rollover_description_inner").text
        # Identify and return link to listing
        link = result.a['href']

        # Print results only if news_title, news_paragraph, and link are available
        if (news_title and news_p and link):
            print('-'*100)
            print(news_title)
            print(news_p)
            print(link)
    except Exception as e:
        print(e)


# ## JPL Mars Space Images - Featured Image
# 
# Visit the url for JPL's Featured Space Image here.
# <https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars>
# 
# Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called featured_image_url.
# 
# Make sure to find the image url to the full size .jpg image.
# 
# Make sure to save a complete url string for this image.
# 
# # Example:
# featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA16225_hires.jpg'

# In[8]:


# scrape the website using chromedriver
executable_path = {'executable_path': '/Users/Mayurshah/Downloads/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
base_url='https://www.jpl.nasa.gov'
browser.visit(url)
html = browser.html    
soup2 = bs(html, 'html.parser')

featured_image = soup2.find('div', class_='carousel_items')

featured_image


# In[9]:


# To get image link for Full Image. 
# Alternative to key/value pair; just use "img_title = soup.find('a', class_='data-fancybox-href')
img_title = soup2.find('a', attrs={'id':'full_image','data-title':True}).get('data-title')
img = soup2.find('a', attrs={'id': 'full_image', 'data-fancybox-href': True}).get('data-fancybox-href')
img_title
img


# In[10]:


featured_image_url = base_url + img


# In[11]:


print(img_title)
print(featured_image_url)


# # Mars Weather
# 
# Visit the Mars Weather twitter account here and scrape the latest Mars weather tweet from the page. Save the tweet text for the weather report as a variable called mars_weather.
# # Example:
# mars_weather = 'Sol 1801 (Aug 30, 2017), Sunny, high -21C/-5F, low -80C/-112F, pressure at 8.82 hPa, daylight 06:09-17:55'
# Mars Facts
# 
# Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
# 
# Use Pandas to convert the data to a HTML table string.

# In[12]:


# scrape the twitter account using chromedriver
executable_path = {'executable_path': '/Users/Mayurshah/Downloads/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)
url = 'https://twitter.com/marswxreport?lang=en'
browser.visit(url)
html = browser.html    
soup3 = bs(html, 'html.parser')
print(soup3.prettify())


# In[13]:


string = soup3.find('div', class_='js-tweet-text-container').text
mars_weather = string.replace('\n',"")
mars_weather


# In[14]:


# scrape the twitter account using chromedriver
executable_path = {'executable_path': '/Users/Mayurshah/Downloads/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)
url = 'https://space-facts.com/mars/'
browser.visit(url)
html = browser.html    
soup4 = bs(html, 'html.parser')
print(soup4.prettify())


# In[15]:


# Read table
tables = pd.read_html(url)
tables


# In[16]:


# Replace header of the table
df = tables[0]
df.columns=['Measures','Details']
df


# In[17]:


# replace index with Measures
df.set_index('Measures', inplace=True)
df.head()


# In[18]:


html_table = df.to_html()
html_table


# In[19]:


# Remove white spaces
html_table.replace('\n', '')


# In[20]:


# Save table to html file
df.to_html('table.html')


# # Mars Hemisperes
# 
# Visit the USGS Astrogeology site here to obtain high resolution images for each of Mar's hemispheres.
# 
# You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
# 
# Save both the image url string for the full resolution hemipshere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys img_url and title.
# 
# Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.

# In[22]:


# scrape the twitter account using chromedriver
executable_path = {'executable_path': '/Users/Mayurshah/Downloads/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
base_url2 = 'https://astrogeology.usgs.gov'
browser.visit(url)
html = browser.html    
soup5 = bs(html, 'html.parser')
print(soup5.prettify())


# In[23]:


cerberus = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced'
schiaparelli = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced'
syrtis = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'
valles = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'
img_url = [cerberus,schiaparelli,syrtis,valles]


# In[24]:


img_url


# In[25]:


img_titles = soup.find_all('h3')
img_titles = [h3.text.strip() for h3 in img_titles]
img_titles


# In[26]:


hemisphere_images = [{'title': img_titles, 'img_url': img_url}]


# In[27]:


hemisphere_images


# In[28]:


combined_hemisphere_image = list(zip(img_titles,img_url))
print(combined_hemisphere_image)


# # Step 2 - MongoDB and Flask Application

# Use MongoDB with Flask templating to create a new HTML page that displays all of the information that was scraped from the URLs above.
# 
# Start by converting your Jupyter notebook into a Python script called scrape_mars.py with a function called scrape that will execute all of your scraping code from above and return one Python dictionary containing all of the scraped data.
# 
# Next, create a route called /scrape that will import your scrape_mars.py script and call your scrape function.
# 
# Store the return value in Mongo as a Python dictionary.
# Create a root route / that will query your Mongo database and pass the mars data into an HTML template to display the data.
# 
# Create a template HTML file called index.html that will take the mars data dictionary and display all of the data in the appropriate HTML elements. Use the following as a guide for what the final product should look like, but feel free to create your own design.

# In[30]:


get_ipython().system(' jupyter nbconvert --to script --template basic mission_to_mars.ipynb --output scrape_mars')

