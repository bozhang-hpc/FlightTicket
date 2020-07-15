from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import time
import requests
from playsound import playsound
import re
from io import BytesIO
from zipfile import ZipFile

####################################################################################################

runtime = 5  # total runtime for this code in minutes
frequency = 1  # frequency of search in minutes

way_of_notification = "alarm"  # call alarm / notify

sound_file = "sound.mp3"
TIMEOUT_IN_SECONDS = 10  # set the time to wait till web fully loaded

EVENT_NAME = "UA857"

flight_info = {
    'SFO-PVG': {
        'search_dates': ['2020-07-15', '2020-11-25', '2020-11-26'],
        'base_url': 'https://www.google.com/flights?hl=en#flt=SFO.PVG.2020-11-26.SFOPVG0UA857;c:USD;e:1;s:0;sd:1;t:b;tt:o;sp:2.USD.706410'
    },
}

#####################################################################################################

API_KEY = open(r"API_KEY").readline().strip("\n")
if not API_KEY:
    raise Exception("You need to fill in the API_KEY in the directory.")

notification_url = f"https://maker.ifttt.com/trigger/{EVENT_NAME}/with/key/{API_KEY}"


def get_web_driver():
    import platform

    print("downloading the web driver...", end="")

    system_name = platform.system()
    if system_name == "Windows":
        system_name = "win32"
    elif system_name == "Darwin":
        system_name = "mac64"
    elif system_name == "Linux":
        system_name = "linux64"
    else:
        raise Exception("Unknown system type")

    drive_url = f"https://chromedriver.storage.googleapis.com/83.0.4103.39/chromedriver_{system_name}.zip"

    response = requests.get(drive_url)
    response.raise_for_status()

    with ZipFile(BytesIO(response.content)) as z:
        z.extractall()

    print("Done")


def alarm(n):
    """repeat alarm sound for n times"""
    for i in range(n):
        playsound(sound_file)
        time.sleep(2)


def notify(*values):
    """
    use IFTTT to notify
    Refer to https://zhuanlan.zhihu.com/p/103419701 for details
    """
    data = {"value"+str(i+1): value for i, value in enumerate(values[:3])}

    response = requests.request("POST", notification_url, data=data)
    response.raise_for_status()


def search(freq):
    for route, info in flight_info.items():
        for date in info['search_dates']:
            url = re.sub(r"2020(-\d{2}){2}", date, info['base_url'])
            driver = webdriver.Chrome()
            driver.get(url)
            time.sleep(TIMEOUT_IN_SECONDS)  # Let the user actually see something!

            try:
                error_msg = driver.find_element_by_css_selector('.gws-flights-results__error-message')
            except Exception:
                if way_of_notification == "alarm":
                    alarm(3)
                elif way_of_notification == "notify":
                    notify(route)
                continue
            else:
                if len(error_msg.text):
                    print('flight search {} attempted on date {}, no result'.format(route, date))
                    driver.quit()
    time.sleep(freq*60)


if __name__ == '__main__':
    try:
        webdriver.Chrome().quit()
    except (FileNotFoundError, WebDriverException):
        get_web_driver()

    total_time = int(runtime / frequency)
    for _ in range(total_time):
        search(frequency)
