# +
# import asyncio
# import time
# from playwright.async_api import async_playwright
# import playwright.async_api as async_api


# linkpaht="https://www.instagram.com/explore/locations/3000346/st-patricks-cathedral/"
# direct="C:/Users/Diego/AppData/Local/Google/Chrome/User Data"

# async def run(playwright):
#     # Inicia la sesión de Playwright
#     user_dir="C:\\Users\\Diego\\AppData\\Local\\Google\\Chrome/User Data"
#     executable_path="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
#     # browser = await playwright.chromium.launch(headless=False,channel="chrome" )
#     # browser = await playwright.chromium.launch(headless=False)
#     # browser = await browser_type.launch(executable_path=executable_path)
#     browser = await playwright.chromium.launch(headless=False, executable_path=executable_path)
#     # browser =await playwright.chromium.launch_persistent_context(user_dir, headless=False)
#     browserContex = await  playwright.chromium.launch_persistent_context(direct) 
# #     browser = await async_api.launch(
# #         headless=False,
# #         executable_path="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
# #         user_data_dir="C:\\Users\\Diego\\AppData\\Local\\Google\\Chrome\\User Data",
# #     )
        
#     # browser = await playwright.firefox.launch() # or "chromium" or "webkit".
#     # create a new incognito browser context.
#     context = await browser.new_context(record_har_path="github.har")
#     # create a new page in a pristine context.
#     page = await context.new_page()
#     await page.goto(linkpaht)

#     # gracefully close up everything
#     time.sleep(5)
#     await context.close()
#     await browser.close()
# async def main():
#     async with async_playwright() as playwright:
#         await run(playwright)
# asyncio.run(main())
# -



import pandas as pd
from playwright.sync_api import sync_playwright
import threading
import time
import pandas as pd
import re
import time
import random
import pickle
from datetime import datetime
import json

# +
import asyncio
import time
from playwright.async_api import async_playwright
import playwright.async_api as async_api

direct="C:/Users/Diego/AppData/Local/Google/Chrome/User Data"
# linkpaht="https://www.instagram.com/explore/locations/3000346/st-patricks-cathedral/"
linkpaht="https://www.instagram.com/explore/locations/475811064/roma-mexico-city/"

minut=60
milisegun=minut*60000
segun=minut*60
async def run(playwright):
    browser = await playwright.chromium.launch_persistent_context(channel="chrome",headless=True,user_data_dir=direct,record_har_path="github.har")
    page = await browser.new_page()
    await page.goto(linkpaht)
    status = await page.evaluate("""async (milisegun) => {
    
         function scrollAutomatically() {
      const timeLimit = milisegun;

      // Tiempo transcurrido
      let elapsedTime = 0;

      // Función recursiva que se llama a sí misma cada vez que se mueve el scroll
      function scroll() {
        // Obtener un número aleatorio entre 2 y 5
        const randomInterval = Math.floor(Math.random() * (4000 - 1000)) + 1000;

        // Mover el scroll hacia abajo
        window.scrollBy(0, window.innerHeight);

        // Actualizar el tiempo transcurrido
        elapsedTime += randomInterval;

        // Si el tiempo transcurrido es menor que el tiempo límite, programar una llamada a esta función de nuevo
        // después del intervalo aleatorio
        if (elapsedTime < timeLimit) {
          setTimeout(scroll, randomInterval);
            }
          }

          // Iniciar el proceso de scroll automático
          scroll();
        }

        scrollAutomatically();

        }""",milisegun)
   
    time.sleep(segun)
    await browser.close()
async def main():
    async with async_playwright() as playwright:
        await run(playwright)
asyncio.run(main())

# +
# direct="C:/Users/Diego/AppData/Local/Google/Chrome/User Data"
# linkpaht="https://www.instagram.com/explore/locations/3000346/st-patricks-cathedral/"
# with sync_playwright() as p:
#     # browser = p.chromium.launch(headless=False)
#     browser = p.chromium.launch_persistent_context(channel="chrome",headless=False,user_data_dir=direct,record_har_path="github.har")
#     # with open("github.har", encoding="utf-8") as f:
#         # data = json.load(f)
#       # Carga el contenido del archivo en una variable
#     # data = json.load(f)
#     # print(data["log"]["entries"][36]["response"]["headers"][7]['value'])
    
#     page = browser.new_page()
#     page.goto(linkpaht)
#     status = page.evaluate("""async () => {
    
#      function scrollAutomatically() {
#   // Tiempo límite en milisegundos (2 minutos)
#   const timeLimit = 360000;

#   // Tiempo transcurrido
#   let elapsedTime = 0;

#   // Función recursiva que se llama a sí misma cada vez que se mueve el scroll
#   function scroll() {
#     // Obtener un número aleatorio entre 2 y 5
#     const randomInterval = Math.floor(Math.random() * (5000 - 2000)) + 2000;

#     // Mover el scroll hacia abajo
#     window.scrollBy(0, window.innerHeight);

#     // Actualizar el tiempo transcurrido
#     elapsedTime += randomInterval;

#     // Si el tiempo transcurrido es menor que el tiempo límite, programar una llamada a esta función de nuevo
#     // después del intervalo aleatorio
#     if (elapsedTime < timeLimit) {
#       setTimeout(scroll, randomInterval);
#         }
#       }

#       // Iniciar el proceso de scroll automático
#       scroll();
#     }

#     scrollAutomatically();

#     }""")
   
#     time.sleep(5)
#     browser.close()


# -

def convert_har(ubi_har):
    # Abre el archivo .har
    with open(ubi_har, encoding="utf-8") as f:
      # Carga el contenido del archivo en una variable
      data = json.load(f)
    #

    # # Accede a los datos del archivo .har
    # data["log"]["entries"][36]["response"]["headers"][7]['value']
    # data["log"]["entries"][38]["response"]["headers"][9]['value']
    # len(data["log"]["entries"])

    def select_date(x):
        # La cadena de texto a convertir
        text = x
        try:
            # El formato de la cadena de texto
            fmt = '%a, %d %b %Y %H:%M:%S %Z'

            # Convertir la cadena de texto a un objeto datetime
            dt = datetime.strptime(text, fmt)
            return dt  # imprime: 2022-12-12 20:13:32
        except:
            pass

    list_date=[]
    for i in data["log"]["entries"]:
        try:
            list_date.append(i["response"]["headers"][9]['value'])
        except:
            pass

    dates_har=list(filter(select_date,list_date))
    return dates_har
