import os
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin
from functions import *

cookies = {
    'ip': '188.225.123.167',
    'id_pais': '164',
    'nrw': '0',
    'oneT': ',C0001,C0002,C0003,C0004,C0005,',
    'OptanonConsent': 'isGpcEnabled=0&datestamp=Thu+May+25+2023+00^%^3A20^%^3A14+GMT^%^2B0300+(^%^D0^%^9C^%^D0^%^BE^%^D1^%^81^%^D0^%^BA^%^D0^%^B2^%^D0^%^B0^%^2C+^%^D1^%^81^%^D1^%^82^%^D0^%^B0^%^D0^%^BD^%^D0^%^B4^%^D0^%^B0^%^D1^%^80^%^D1^%^82^%^D0^%^BD^%^D0^%^BE^%^D0^%^B5+^%^D0^%^B2^%^D1^%^80^%^D0^%^B5^%^D0^%^BC^%^D1^%^8F)&version=6.32.0&isIABGlobal=false&hosts=&landingPath=NotLandingPage&groups=C0001^%^3A1^%^2CC0002^%^3A1^%^2CC0003^%^3A1^%^2CC0004^%^3A1^%^2CC0005^%^3A1&geolocation=^%^3B&AwaitingReconsent=false',
    'OptanonAlertBoxClosed': '2023-05-12T20:38:22.769Z',
    'barra_cookies': '1',
    'rurl': 'https://www.tradeinn.com/bikeinn/ru/^%^D0^%^9C^%^D1^%^83^%^D0^%^B6^%^D1^%^81^%^D0^%^BA^%^D0^%^B0^%^D1^%^8F-^%^D0^%^BE^%^D0^%^B4^%^D0^%^B5^%^D0^%^B6^%^D0^%^B4^%^D0^%^B0/4011/f',
    'AMCV_59CC28AF644C2B150A495E0C^%^40AdobeOrg': '179643557^%^7CMCIDTS^%^7C19502^%^7CMCMID^%^7C39074883946931744746937270379829474987^%^7CMCOPTOUT-1684970412s^%^7CNONE^%^7CvVersion^%^7C5.5.0',
    'AMCVS_59CC28AF644C2B150A495E0C^%^40AdobeOrg': '1',
    'recommendation_products_last': '4120',
    'recommendation_products': '{4120:15,11833:10,12182:2,12479:1,12505:10,14226:7,18151:1,19075:1,12505_2579:3,12505_5003:4,12505_497:1,12505_252:1,11833_497:6,12505_1745:1}',
    'usizy.sk': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzaWQiOiJhNThjZDEwYWZhNTgxMWVkYjBlNmFlOTEyZDE4YzA4NCIsInZAZSI6WzldfQ.11FuLvmKQgzi977lNz5X_R_1gLCc21Xg4sXA_-pUAOA',
    'PHPSESSID': 'jhh522isjsm5lcqgrm49c789vi',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Proxy-Authorization': 'Basic NDQxNjk4YzYzNGFhNDQ2YmJjNDcxYTNiMDdmM2MwNWQ6dFBfRWdwTmlTUU5YS3k4eQ==',
    'Connection': 'keep-alive',
    # 'Cookie': 'ip=188.225.123.167; id_pais=164; nrw=0; oneT=,C0001,C0002,C0003,C0004,C0005,; OptanonConsent=isGpcEnabled=0&datestamp=Thu+May+25+2023+00^%^3A20^%^3A14+GMT^%^2B0300+(^%^D0^%^9C^%^D0^%^BE^%^D1^%^81^%^D0^%^BA^%^D0^%^B2^%^D0^%^B0^%^2C+^%^D1^%^81^%^D1^%^82^%^D0^%^B0^%^D0^%^BD^%^D0^%^B4^%^D0^%^B0^%^D1^%^80^%^D1^%^82^%^D0^%^BD^%^D0^%^BE^%^D0^%^B5+^%^D0^%^B2^%^D1^%^80^%^D0^%^B5^%^D0^%^BC^%^D1^%^8F)&version=6.32.0&isIABGlobal=false&hosts=&landingPath=NotLandingPage&groups=C0001^%^3A1^%^2CC0002^%^3A1^%^2CC0003^%^3A1^%^2CC0004^%^3A1^%^2CC0005^%^3A1&geolocation=^%^3B&AwaitingReconsent=false; OptanonAlertBoxClosed=2023-05-12T20:38:22.769Z; barra_cookies=1; rurl=https://www.tradeinn.com/bikeinn/ru/^%^D0^%^9C^%^D1^%^83^%^D0^%^B6^%^D1^%^81^%^D0^%^BA^%^D0^%^B0^%^D1^%^8F-^%^D0^%^BE^%^D0^%^B4^%^D0^%^B5^%^D0^%^B6^%^D0^%^B4^%^D0^%^B0/4011/f; AMCV_59CC28AF644C2B150A495E0C^%^40AdobeOrg=179643557^%^7CMCIDTS^%^7C19502^%^7CMCMID^%^7C39074883946931744746937270379829474987^%^7CMCOPTOUT-1684970412s^%^7CNONE^%^7CvVersion^%^7C5.5.0; AMCVS_59CC28AF644C2B150A495E0C^%^40AdobeOrg=1; recommendation_products_last=4120; recommendation_products={4120:15,11833:10,12182:2,12479:1,12505:10,14226:7,18151:1,19075:1,12505_2579:3,12505_5003:4,12505_497:1,12505_252:1,11833_497:6,12505_1745:1}; usizy.sk=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzaWQiOiJhNThjZDEwYWZhNTgxMWVkYjBlNmFlOTEyZDE4YzA4NCIsInZAZSI6WzldfQ.11FuLvmKQgzi977lNz5X_R_1gLCc21Xg4sXA_-pUAOA; PHPSESSID=jhh522isjsm5lcqgrm49c789vi',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'cross-site',
}

site_name = 'tradeinn.com'
url_to_add = 'https://www.tradeinn.com'
base_url = 'https://www.tradeinn.com/bikeinn/ru/%D0%9C%D1%83%D0%B6%D1%81%D0%BA%D0%B0%D1%8F-%D0%BE%D0%B4%D0%B5%D0%B6%D0%B4%D0%B0/4011/f'

downloads_dir = os.path.join('D:', os.sep, 'work', 'downloads')
os.makedirs(downloads_dir, exist_ok=True)

downloads_folder = os.path.join(downloads_dir, site_name)
os.makedirs(downloads_folder, exist_ok=True)

products_folder = os.path.join(downloads_folder, 'products')
os.makedirs(products_folder, exist_ok=True)

tradeinn_categories_csv = os.path.join(downloads_folder, 'tradeinn-categories-output2.csv')


def get_proxy_from_doc():
    with open('proxy.txt', 'r', encoding='utf-8') as file:
        proxy_str = file.read().splitlines()

    return proxy_str


def download_main_page(url, headers, cookies):
    import random
    from transliterate import translit
    from urllib.parse import unquote

    product_name = url.split('/')[-3]
    decoded_name = unquote(product_name)
    transliterated_name = translit(decoded_name, 'ru', reversed=True)
    file_name = os.path.join(downloads_folder, f'{transliterated_name.lower()}.html')

    proxies = random.choice(get_proxy_from_doc())
    download_page_proxy(url, file_name, headers, cookies, proxies, timeout=10)


def extract_category_urls():
    results = []

    for file_name in os.listdir(downloads_folder):
        if file_name.endswith('.html'):
            file_path = os.path.join(downloads_folder, file_name)

            if not os.path.exists(file_path):
                print(f'File not found: {file_name}')
                continue

            with open(file_path, 'r', encoding='utf-8') as file:
                page_content = file.read()

            soup = BeautifulSoup(page_content, 'html.parser')
            div_tag = soup.find('div', {'class': 'listado_familias'})
            for tag in div_tag:
                a_tags = tag.find_all('a', {'class': 'enlace_img'})

                for urls in a_tags:
                    part_url = urls['href']
                    product_url = urljoin(url_to_add, part_url)
                    results.append(product_url)

    df = pd.DataFrame(results)
    df.drop_duplicates(inplace=True)
    df.to_csv(tradeinn_categories_csv, index=False, header=False)


def download_product(file_path):
    import csv
    import requests

    try:
        with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for url in reader:
                url_text = ', '.join(url)
                response = requests.get(url_text, cookies=cookies, headers=headers)
                print(response.text)
    except FileNotFoundError:
        print('File not found')
    except IOError:
        print('Input/output error when reading a file')


if __name__ == '__main__':
    download_main_page(base_url, headers, cookies)
    pause(10, 30)
    extract_category_urls()
    pause(10, 30)
    download_product(tradeinn_categories_csv)
