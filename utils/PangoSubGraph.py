import asyncio
import json
import requests

from utils import Constants


async def genericQuery(query):
    r = requests.post(Constants.PANGO_API_URL, json={'query': query})
    assert(r.status_code == 200)
    return json.loads(r.text)


async def getAvaxPrice():
    USDTPrice = await genericQuery("""{pair(id: "0x9ee0a4e21bd333a6bb2ab298194320b8daa26516") {token1Price}}""")
    DAIPrice = await genericQuery("""{pair(id: "0x17a2e8275792b4616befb02eb9ae699aa0dcb94b") {token1Price}}""")
    return float(USDTPrice["data"]["pair"]["token1Price"]) / 2 + float(DAIPrice["data"]["pair"]["token1Price"]) / 2

async def getSherpaPrice():
    avaxPrice = await getAvaxPrice()
    sherpaDerivedEth = float((await genericQuery("""{pair(id: "0xd27688e195b5495a0ea29bb6e9248e535a58511e") {token1Price}}"""))["data"]["pair"]["token1Price"])
    return avaxPrice * sherpaDerivedEth

# print(asyncio.run(getSherpaPrice()))