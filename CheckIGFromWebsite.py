from operator import contains
import re
import requests
import pandas as pd
import time
# Replace 'data.csv' with your actual file path
df = pd.read_csv('look for instagram.csv',
                 usecols=['Organisation - Website'])

# Display the DataFrame with only column cls2
print(df)


def add_www_to_link(link):
    """
    Adds 'www.' to the link after 'http://' or 'https://'.

    Args:
        link (str): The original link.

    Returns:
        str: The modified link with 'www.' added.
    """
    if link.startswith("http://"):
        return link.replace("http://", "http://www.")
    elif link.startswith("https://"):
        return link.replace("https://", "https://www.")
    elif link.startswith("www") is False:
        return "https://www."+link
    else:
        return link


instagram_links = []
# Assuming you have a DataFrame 'df' with links in column 2
for link in df['Organisation - Website']:
    try:
        link = add_www_to_link(link)
        response = requests.get(link, headers={
                                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0"})
        print(response.status_code)
        if response.status_code == 200:
            # Search for Instagram URLs in the page source
            instagram_urls = re.findall(
                r'(instagram\.com/[\w.-]+)', response.text)
            if instagram_urls:
                # instagram_links.append(link)
                print(f"Instagram URLs for {link}:")
                for url in instagram_urls[:1]:
                    instagram_links.append(url)
                    print(f"- {url}")
            else:
                print(f"No Instagram URLs found for {link}")
                instagram_links.append("No Instagram URLs found for "+link)
        else:
            instagram_links.append(
                "Error fetching "+link+": Status code "+str(response.status_code))
            print(f"Error fetching {link}: Status code {response.status_code}")

    except Exception as e:
        instagram_links.append(f"Error processing {link} : {str(e)}")
        print(f"Error processing {link}: {str(e)}")

print(instagram_links)
df['Instagram Link'] = instagram_links

# Save the updated DataFrame back to the CSV file
df.to_csv('look for instagram.csv', index=False)
