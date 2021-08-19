import asyncio
import json
import requests

from utils import Constants


async def genericQuery(query):
    r = requests.post(Constants.PANGO_API_URL, json={'query': query})
    assert(r.status_code == 200)
    return json.loads(r.text)


async def getAvaxPrice():
    USDTe_query = await genericQuery("""{pair(id:"0xe28984e1ee8d431346d32bec9ec800efb643eef4"){token1Price, reserve1}}""")
    DAIe_query = await genericQuery("""{pair(id:"0xba09679ab223c6bdaf44d45ba2d7279959289ab0"){token1Price, reserve1}}""")
    avaxPriceUSDTe = float(USDTe_query["data"]["pair"]["token1Price"])
    avaxPriceDAIe = float(DAIe_query["data"]["pair"]["token1Price"])
    usdte_liq = float(USDTe_query["data"]["pair"]["reserve1"])
    daie_liq = float(DAIe_query["data"]["pair"]["reserve1"])
    sum_liq = usdte_liq + daie_liq
    return avaxPriceUSDTe * (usdte_liq / sum_liq) + avaxPriceDAIe * (daie_liq / sum_liq)

async def getSherpaPrice():
    avaxPrice = await getAvaxPrice()
    sherpaDerivedEth = float((await genericQuery("""{pair(id: "0xd27688e195b5495a0ea29bb6e9248e535a58511e") {token1Price}}"""))["data"]["pair"]["token1Price"])
    return avaxPrice * sherpaDerivedEth

# print(asyncio.run(getSherpaPrice()))