#!/usr/bin/python3 
# execution with DorkingTools.py

import argparse
import requests
import os 
import json
import time
from bs4 import BeautifulSoup
from termcolor import colored

# Text To ASCII
print("""
      ________                __   .__             ___________           .__    
\______ \   ___________|  | _|__| ____    ___\__    ___/___   ____ |  |   ______
 |    |  \ /  _ \_  __ \  |/ /  |/    \  / ___\|    | /  _ \ /  _ \|  |  /  ___/
 |    `   (  <_> )  | \/    <|  |   |  \/ /_/  >    |(  <_> |  <_> )  |__\___ \ 
/_______  /\____/|__|  |__|_ \__|___|  /\___  /|____| \____/ \____/|____/____  >
        \/                  \/       \//_____/                               \/ """)

    """
    Todo : 
    Update 429 with google search or selenium...
    Export google_search function
    """
    
def google_search(file_name,domain):
    with open(file_name,encoding="utf8") as f:
        for line in f:
            query = line.strip()
            time.sleep(3) 
            url = f'https://www.google.com/search?q={query}+site:{domain}'
            #response = requests.get(url) # request to google
            response = requests.get(url,headers = {'User-agent': 'your bot 0.2'})  # request to google with user agent 
            # Analyse de la première réponse 429 du serveur 
            if response.status_code == 429:
                retry_after = response.headers.get("Retry-After")
                if retry_after:
                    retry_after = int(retry_after)
                    print(f"Error code 429 received. Expectation of {retry_after} seconds before trying again...")
                    time.sleep(retry_after)
                else:
                    print("Error code 429 received. Retry-After header not found. Waiting 5 seconds before trying again...")
                    time.sleep(7)
                response = requests.get(url)           

            if response.status_code == 200:
                # get link response from html template 
                data = response.text
                soup = BeautifulSoup(data,'html.parser')
                urls = []
                for link in soup.find_all('a'):
                    url = link.get('href')
                    # exclude adress already in google result page
                    exclude_list = ["https://accounts.google.com/ServiceLogin?hl=fr&continue=https://www.google.com/search?q%3Dintext:%2522&gae=cb-none", 
        "https://policies.google.com/technologies/cookies?hl=fr&utm_source=ucb",
        "https://consent.google.com/dl?continue=https://www.google.com/search?q%3Dintext:%2522&gl=FR&hl=fr&pc=srp&uxe=none&src=1",
        "https://policies.google.com/privacy?hl=fr&utm_source=ucb",
        "https://policies.google.com/terms?hl=fr&utm_source=ucb"]

                # define request print 
                print(f'{query} site:{domain} HTTP: {response.status_code}')    
                
                if url not in exclude_list:
                    print(url)
                #  print("find information", urls) # basique
                print("find information", colored(urls, '#00ff00'))  # add some color             
                # print(f'{query}+site:{domain} - {response.status_code}')
            else:
                print(f'{query}+site:{domain} - {response.status_code}')
                
                
                
                
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Search keywords on Google, google dorks')
    parser.add_argument('-f', '--file', help='File containing the dorks to search for',default='./payload/payload.txt')
    parser.add_argument('-d', '--domain', help='Domain to limit search results to',default='google-gruyere.appspot.com')
    
    args = parser.parse_args()
    
if args.file and args.domain:
    google_search(args.file,args.domain)
elif args.file:
    print('No domain specified. Use -d or --domain to specify a domain.')
elif args.domain:
    print('No file specified. Use -f or --file to specify a file.')
else:
    print('No file or domain specified. Use -f or --file and -d or --domain to specify a file and domain.')


