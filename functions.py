def time_now() -> str:
    """
    Returns the current date and time in the format 'dd-mm-yyyy HH:MM:SS'.

    Returns:
        str: A string with the current date and time.
    """
    from datetime import datetime

    return datetime.now().strftime('%d-%m-%Y %H:%M:%S')


def pause(min_seconds: int = 0, max_seconds: int = 10) -> None:
    """
    Pauses the execution of the program for a random number of seconds within the specified range.

    Args:
        min_seconds (int, optional): The minimum number of seconds for the pause. Defaults to 0.
        max_seconds (int, optional): The maximum number of seconds for the pause. Defaults to 10.

    Returns:
        None
    """
    import time
    import random

    num_sec = random.randint(min_seconds, max_seconds)
    time.sleep(num_sec)


def get_proxy_dict(proxy_val: str) -> dict:
    """
    Creates a dictionary with the proxy server settings for use in requests.

    Args:
        proxy_val (str): The proxy server value in the format 'host:port'.

    Returns:
        dict: A dictionary with the proxy server settings.
    """
    return {"https": 'http://' + proxy_val, "http": 'http://' + proxy_val}


def download_page_proxy(url: str, file_path: str, headers: dict, cookies: dict, proxies: str, timeout: int = 10):
    """
    Downloads a web page using a proxy server and saves it to a file.

    Args:
        url (str): The URL of the web page.
        file_path (str): The file path to save the web page.
        headers (dict): Headers for the request.
        cookies (dict): Cookies for the request.
        proxies (str): The proxy server value in the format 'host:port'.
        timeout (int, optional): The maximum time to wait for a response from the server. Defaults to 10.

    Returns:
        int: The status code of the successful page download (200), error code, or False in case of failure.
    """
    import requests
    import htmlmin

    proxies = get_proxy_dict(proxies)
    session = requests.Session()
    session.proxies.update(proxies)

    success = False
    try:
        request = session.get(url, headers=headers, cookies=cookies, timeout=timeout)

        status_code = request.status_code
        if status_code == 200:
            page_html = request.content
            text = htmlmin.minify(page_html.decode(errors='ignore'), remove_empty_space=True)
            with open(file_path, 'w', encoding='utf-8') as fl:
                fl.write(text)
                print(f'{time_now()} {url} with {proxies} has been downloaded')
                success = 200
        elif status_code == 403:
            print(f'{time_now()} 403 Forbidden for {url}, pausing')
            pause(6, 18)
        else:
            print(f'{time_now()} Error: response code {request.status_code} in {url} with {proxies}')
            print(request.text)
    except requests.exceptions.ProxyError as ex:
        print(f"{time_now()} ProxyError {ex}. Failed proxy {proxies}")
    except requests.exceptions.ConnectionError as ex:
        print(f"{time_now()} ConnectionError {ex}. Failed proxy {proxies}")
    except Exception as ex:
        print(ex)
        pause(100, 300)
    pause(2, 5)

    return success


def delay_start(min_sec=5, max_sec=600) -> None:
    """
    Delays the execution of code by a random amount of time within the specified range.

    Args:
        min_sec (int): The minimum delay time in seconds. Defaults to 5 seconds.
        max_sec (int): The maximum delay time in seconds. Defaults to 600 seconds (10 minutes).

    Returns:
        None
    """
    import random
    import time

    delay_time = random.randint(min_sec, max_sec)
    delay_minutes = round(delay_time / 60, 1)
    print(f'Wait for {delay_minutes} minutes')
    time.sleep(delay_time)
