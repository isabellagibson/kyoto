import json
import requests
import os
import time
from colorama import init, Fore

init()

TLD_LIST_URL = 'https://data.iana.org/TLD/tlds-alpha-by-domain.txt'
DOMAINS = ['gogoanime']
REQUEST_TIMEOUT = 6

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

clear()
print(f'Downloading TLD (domain ending) list from {Fore.LIGHTGREEN_EX}{TLD_LIST_URL}{Fore.RESET}')
open('tlds-alpha-by-domain.txt', 'wb').write(requests.get(TLD_LIST_URL).content)
clear()
print('Scanning for viable domains...')
TLD_LIST = [line.replace('\n', '').lower() for line in open('tlds-alpha-by-domain.txt', 'r').readlines()[1:]]
VALID_DOMAINS = []
START_TIME = time.time()
for d in DOMAINS:
    for tld in TLD_LIST:
        try:
            url = f'http://{d}.{tld}/'
            req = requests.get(url, timeout=REQUEST_TIMEOUT)
            print(f'[{Fore.LIGHTGREEN_EX}GET {str(req.status_code)}{Fore.RESET}] {Fore.LIGHTGREEN_EX}{url}{Fore.RESET}')
            VALID_DOMAINS.append(url)
        except:
            print(f'[{Fore.LIGHTRED_EX}GET{Fore.RESET}] {Fore.LIGHTRED_EX}{url}{Fore.RESET}')
            pass
clear()
END_TIME = round(time.time() - START_TIME)
print(f'Done! Took {Fore.LIGHTGREEN_EX}{str(END_TIME)}{Fore.RESET} seconds.\n - Scanned domains: {Fore.LIGHTGREEN_EX}{str(len(TLD_LIST))}{Fore.RESET}\n - Valid domains: {Fore.LIGHTGREEN_EX}{str(len(VALID_DOMAINS))}{Fore.RESET} ({str(round(((len(VALID_DOMAINS) * 100) / len(TLD_LIST)), 2))}%)')
open('mirrors.json', 'w').write(json.dumps(VALID_DOMAINS, indent=2))
os.remove('tlds-alpha-by-domain.txt')