from fastapi import FastAPI
import uvicorn

import requests
from bs4 import BeautifulSoup
import json

app=FastAPI()

class Exchanges:
    def __init__(self, name, trading_volume, market_share, no_of_markets):
        self.name = name
        self.trading_volume = trading_volume
        self.market_share=market_share
        self.no_of_markets=no_of_markets

@app.get("/metrics")
def getMetrics():
    data=[]
    r=requests.get("https://coinmarketcap.com/rankings/exchanges/")
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'html.parser')
        str=soup.find(id="__NEXT_DATA__").text
        my_json_object = json.loads(str)

        for i in range (0,228):
            name=my_json_object["props"]["pageProps"]["initialData"]["exchanges"][i]["name"]
            trading_volume=my_json_object["props"]["pageProps"]["initialData"]["exchanges"][i]["totalVol24h"]
            market_share=my_json_object["props"]["pageProps"]["initialData"]["exchanges"][i]["marketSharePct"]
            no_of_markets=my_json_object["props"]["pageProps"]["initialData"]["exchanges"][i]["numMarkets"]
            
            data.append(Exchanges(name, trading_volume, market_share, no_of_markets))
    return data


@app.get("/description")
def getDescription(slug:str):
    r=requests.get("https://coinmarketcap.com/exchanges/{0}".format(slug))

    if r.status_code == 200:
        new_soup = BeautifulSoup(r.text, 'html.parser')
        desc=new_soup.find(class_='sc-fd47dc68-0 dgZpLd')
      
    return str(desc)
        