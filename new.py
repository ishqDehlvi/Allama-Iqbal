import requests
from bs4 import BeautifulSoup
import json
import re

# Define the URL of the website
base_url = 'https://jang.com.pk'

# Create a text file for storing the data
output_file = open('article_data.txt', 'w', encoding='utf-8')

# Send an HTTP GET request to the homepage
response = requests.get(base_url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find and extract news article information
    article_elements = soup.find_all('a', href=True, title=True)
    
    for article in article_elements:
        article_title = article.find('h3')
        article_url = article['href']
        
        if article_title and article_url:
            # Send a request to the article page
            article_response = requests.get(article_url)
            
            if article_response.status_code == 200:
                article_soup = BeautifulSoup(article_response.text, 'html.parser')
                
                # Find the JSON-LD script containing article information
                script = article_soup.find('script', type='application/ld+json')
                
                if script:
                    # Clean up the JSON content to remove invalid characters
                    cleaned_json = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', script.string)
                    
                    try:
                        json_data = json.loads(cleaned_json)
                        article_description = json_data.get('description', '')
                        image_url = json_data.get('image', [''])[0]
                        
                        # Write the data to the text file
                        output_file.write(f"Title: {article_title.text.strip()}\n")
                        output_file.write(f"Article URL: {article_url}\n")
                        output_file.write(f"Description: {article_description.strip()}\n")
                        output_file.write(f"Image URL: {image_url}\n\n")
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON: {e}")
            
            else:
                print(f"Failed to retrieve the article page: {article_url}")
else:
    print(f"Failed to retrieve the homepage. Status code: {response.status_code}")

# Close the text file
output_file.close()
