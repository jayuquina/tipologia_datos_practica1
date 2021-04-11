#imports here
from html import unescape
from http_request_randomizer.requests.proxy.requestProxy import RequestProxy
from urllib.parse import urlparse
import os
import requests
import sys
import time

USE_TOR = True

if USE_TOR==False:
    #get different number of proxy when you run this
    request_proxy = RequestProxy()
    #create proxy list
    proxy_list = request_proxy.get_proxy_list()
proxy_pos = -1

#download and save file through proxy
def download_and_save_file(url):
    ret = False
    address = '0.0.0.0:0'
    
    print(url)

    try:
        proxy_temp = None

        if USE_TOR==False:
            proxy = None

            if proxy_pos>=0:
                proxy = proxy_list[proxy_pos]

            address = proxy.get_address()

            proxy_temp = {
                "http": address,
                "https": address
            }
        else:
            address = 'socks5://localhost:9150'

            proxy_temp = {
                "http": address
            }
                
        response = requests.get(url=url, stream=True, proxies=proxy_temp, timeout=10)

        print('response.status_code', response.status_code)

        if str(response.status_code)=='200':
            base_dir  = os.path.dirname(__file__)
            file_name = os.path.basename(url)
            file_name = urlparse(file_name).path
            file_dir  = os.path.join(base_dir, 'images')

            print('file_dir=', file_dir)

            os.makedirs(file_dir, exist_ok=True)
            
            file_path = os.path.join(file_dir, file_name)

            print('file_path=', file_path)

            fwrite = open(file_path, 'wb')

            for chunk in response.iter_content():
                fwrite.write(chunk)
            
            fwrite.close()

            ret = True
        else:
            if str(response.status_code)=='403':
                ret = True
    except:
        e = sys.exc_info()[0]
        print('Error download_and_save_file address', address, str(e))
    return ret

#download and save file through proxy
def attempt_download_and_save(url):
    ret = download_and_save_file(url)

    time.sleep(5)

    if USE_TOR==False and ret==False:
        global proxy_pos
        while proxy_pos<len(proxy_list):
            proxy_pos = proxy_pos+1
            
            ret = download_and_save_file(url)

            if ret==True:
                break

#open csv and read line by line
def process_ins_file():
    fread = open('influencia_elecciones_presidenciales_ec_2021.csv', 'r', encoding='utf-8')
    c = -1

    while True:
        line = fread.readline()
        if not line:
            break

        c = c+1

        if c==0:
            continue

        #split line into list
        print('---------------', c, '---------------')
        src = line.split(';')[5]

        attempt_download_and_save(src)

        src = line.split(';')[7]

        if src!=None and src!='' :
            attempt_download_and_save(src)

    fread.close()

process_ins_file()
