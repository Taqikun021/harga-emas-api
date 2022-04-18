from fastapi import FastAPI
from bs4 import BeautifulSoup
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
import requests
import re

app = FastAPI()
#app.add_middleware(HTTPSRedirectMiddleware)

url = 'https://harga-emas.org/widget/widget.php?v_widget_type=current_gold_price&v_width=300&v_height=215'
pages = requests.get(url)
soup = BeautifulSoup(pages.text, 'lxml')
table1 = soup.find('table')
td = table1.find_all('td')
tdharga = td[12].text
tdstatus = td[17].text
tdstatus = re.sub(r"[\t]*", "", tdstatus)
tdharga = tdharga.split()
tdstatus = tdstatus.split("\n")
status = tdstatus[1]
harga = tdharga[0]


@app.get("/api/harga-emas")
async def root():
    return {"harga_emas": int(harga.replace(".", "")),
            "updated": status,
            "sumber": "https://harga-emas.org"}
