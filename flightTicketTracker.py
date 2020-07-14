from selenium import webdriver
import os
import time
from playsound import playsound

runtime = 5 # total runtime for this code in minutes
soundfile = "sound.mp3"
frequency = 1 # frequency of search in minutes 

flight_info = {
    'SFO-PVG' : {
        'search_dates': ['2020-07-15','2020-11-25', '2020-11-26'],
        'base_url' : 'https://www.google.com/flights?hl=en#flt=SFO.PVG.2020-11-18.SFOPVG0UA857;c:USD;e:1;s:0;sd:1;t:b;tt:o;sp:2.USD.706410'
    },

    #'DTW-PVG' : {
    #    'search_dates': ['2020-07-15','2020-11-25', '2020-11-26'],
    #    'base_url' : 'https://www.google.com/flights?hl=en#flt=DTW.PVG.2020-11-18.DTWPVG0DL389;c:USD;e:1;s:0;sd:1;t:b;tt:o;sp:2.USD.564910'
    #}
}

def alarm(n): # repeat alarm sound for n times
    for i in range(n):
        playsound(soundfile)
        time.sleep(2)

def search(freq):
    time_out_seconds = 10 # set the time to wait till web fully loaded
    for route ,info in flight_info.items():
        for date in info['search_dates'] :
            url = info['base_url'].replace('2020-11-18', date)
            driver = webdriver.Chrome()
            driver.get(url)
            time.sleep(time_out_seconds) # Let the user actually see something!
            try:
                error_msg = driver.find_element_by_css_selector('.gws-flights-results__error-message')
            except Exception as e:
                alarm(3)
                continue
            else:
                if len(error_msg.text) > 0:
                    print('flight search {} attempted on date {}, no result'.format(route, date))
                    driver.quit()
    time.sleep(freq*60)

if __name__ == '__main__':
    totaltime = (int) (runtime/frequency)
    for i in range(totaltime):
        search(frequency)


