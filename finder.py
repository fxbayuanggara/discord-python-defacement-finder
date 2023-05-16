import requests
import urllib.parse
from bs4 import BeautifulSoup

# Change defacement_keyword
search_term = "site:yoursite.com intitle:defacement_keyword"
encoded_search_term = urllib.parse.quote(search_term)

search_engine_url = "https://www.google.com/search?q="
url = f"https://www.google.com/search?q={search_term}"

encoded_url =  search_engine_url + encoded_search_term

response = requests.get(url)

soup = BeautifulSoup(response.text, "lxml")

concatenated_link = []

if response.status_code == 200 and "No results found" not in response.text:
    links = soup.find_all("a", href=True)

    for link in links:
        href = link["href"]
        if href.startswith("/url?q="):
            # print(href[7:])
            if not "google.com" in href[7:]:
               concatenated_link.append(href[7:])

    concatenated_link_text = ' - '.join(concatenated_link)

    if len(concatenated_link) > 0:
      # Send a notification to Discord via webhook
      discord_webhook_url = "https://your/discord/webhook/url"
      data = {"content": f"A new DEFACEMENT page for '{search_term}' was found on Google!.\nSource: '{encoded_url}'.\n\nLinks '{concatenated_link_text}'}
      response = requests.post(discord_webhook_url, json=data)
      if response.status_code == 204:
          print("Notification sent to Discord.")
    else:
      print("No link found")
