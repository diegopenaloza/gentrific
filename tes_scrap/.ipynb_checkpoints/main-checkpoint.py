from playwright.sync_api import sync_playwright
import asyncio
from pyppeteer import launch
import pandas as pd
import re
import time
import random
import pickle


direct="C:/Users/Diego/AppData/Local/Google/Chrome/User Data"

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(channel="chrome",headless=False,user_data_dir=direct)
    page = browser.new_page()
    page.goto(location_link)
    page.evaluate("""async () => {
            document.getElementsByClassName("_9AhH0")[6].click()
        }""")
    time.sleep(3)
    count=''
    page.evaluate("""async () => {
            var date= document.getElementsByClassName("_1o9PC")[0].innerText
        }""")
    end_year=2016
    try :
        while count != end_year:
                page.locator(".l8mY4 .wpO6b").click()
                time.sleep(3)
                count_key = page.evaluate("""async (end_year) => {
                        var eyear=end_year
                        //document.querySelector(".l8mY4 .wpO6b").click()
                        var date= document.getElementsByClassName("_1o9PC")[0].innerText
                        var find= date.search(eyear.toString());
                        if (find>0){
                        var year=end_year
                            }

                        return {year,date}

                    }""",end_year)
                count=count_key['year']
                # time.sleep(2)
                print (count_key)
    except:
        pass
    
    time.sleep(3)
    browser.close()

# # Code Scrap

async def ScrapList():
    browser = await launch(headless=False, executablePath='C:\\Program Files\\Google\Chrome\\Application\\chrome.exe', 
                           userDataDir="C:\\Users\\Diego\\AppData\\Local\\Google\\Chrome/User Data")
    # browser = await launch(channel="chrome",headless=False,user_data_dir=direct)
    page = await browser.newPage()
    await page.goto(location_link)
    await page.evaluate("""async () => {
            document.getElementsByClassName("_9AhH0")[0].click()
        }""")
    time.sleep(3)
    count=''
    list_dates=[]
    await page.evaluate("""async () => {
            var date= document.getElementsByClassName("_1o9PC")[0].innerText
        }""")
    end_year=2016
    try:
        while count != end_year:
            await page.evaluate("""async () => {
                    document.querySelector(".l8mY4 .wpO6b").click()
                }""")
            time.sleep(random.randint(2,4))
            count_key = await page.evaluate("""async (end_year) => {
                    var eyear=end_year
                    //document.querySelector(".l8mY4 .wpO6b").click()
                    var date= document.getElementsByClassName("_1o9PC")[0].innerText
                    var find= date.search(eyear.toString());
                    if (find>0){
                    var year=end_year
                        }

                    return year,date

                }""",end_year)
            # count=count_key['year']
            # time.sleep(2)
            # print (count_key)
            list_dates.append(count_key)
    except:
        pass
    time.sleep(3)
    await browser.close()
    return list_dates

# # Data El Cajas

# +
# location_link="https://www.instagram.com/explore/locations/1480633375314513/batan-shopping/"
# optain_dates=await ScrapList()

# +
# df_dates=pd.DataFrame({'Dates':optain_dates})

# +
# with open('dates.pkl', 'wb') as f:
#      pickle.dump(df_dates, f)
# -

data_dates =pd.read_pickle('data_cajas.pkl')

data_dates

# +
import locale
from datetime import datetime
locale.setlocale(locale.LC_TIME, '')

def convert_time(datetime_str):
    # display( datetime_str)
    try:
        return datetime.strptime(datetime_str.lower(), "%d de %B de %Y")
    except:
        try:
            datetime_str=datetime_str +" DE 2022"
            return datetime.strptime(datetime_str.lower(), "%d de %B de %Y")
        except:
            pass
       


# -

data_dates['dates_format']=data_dates['Dates'].apply(convert_time)

data_dates

count_post=data_dates.groupby(['dates_format'])['dates_format'].count().rename_axis(['date']).reset_index().rename(columns={'dates_format': "total_post_dia"})

count_post_mon=data_dates.groupby(pd.Grouper(key='dates_format', axis=0, 
                      freq='M'))['dates_format'].count().rename_axis(['date']).reset_index().rename(columns={'dates_format': "total_post_dia"})

count_post_mon

# +
import plotly.graph_objects as go
animals=['giraffes', 'orangutans', 'monkeys']

fig = go.Figure([go.Bar(x=count_post_mon['date'], y=count_post_mon['total_post_dia'], text=count_post_mon['total_post_dia'])])
fig.show()
# -

# # Data el Batan
