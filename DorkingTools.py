#!/usr/bin/python3 
# execution with DorkingTools.py

import argparse
import requests
import os 
import json
import time

# Text To ASCII
print("""
      ________                __   .__             ___________           .__    
\______ \   ___________|  | _|__| ____    ___\__    ___/___   ____ |  |   ______
 |    |  \ /  _ \_  __ \  |/ /  |/    \  / ___\|    | /  _ \ /  _ \|  |  /  ___/
 |    `   (  <_> )  | \/    <|  |   |  \/ /_/  >    |(  <_> |  <_> )  |__\___ \ 
/_______  /\____/|__|  |__|_ \__|___|  /\___  /|____| \____/ \____/|____/____  >
        \/                  \/       \//_____/                               \/ """)

def google_search(file_name,domain):
    with open(file_name,encoding="utf8") as f:
        for line in f:
            query = line.strip()
            url = f'https://www.google.com/search?q={query}+site:{domain}'
            response = requests.get(url)
            
            # Analyse de la première réponse 429 du serveur 
            #TODO: resolve 429 error prblm
            """
            if response.status_code == 429:
                retry_after = int(response.headers["Retry-After"])
                print("Error code 429 received. Expectation of", retry_after, "seconds before trying again...")
                time.sleep(retry_after)
                response = requests.get(url)
            """
        
            #Convert response to Python dictionary
            #data = json.loads(response.text)
            #Show title and URL of top search results
            #for item in data["items"]:
                #print("Titre:", item["title"])
                #print("URL:", item["link"])
                
            if response.status_code == 200:
                print(f'{query}+site:{domain} - {response.status_code}')
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