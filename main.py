import logging, json

from aiogram import Bot, Dispatcher, executor, types
from web3 import Web3

from utils import PangoSubGraph, Constants
from utils.beautify_string import readable, human_format

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
with open(".key", "r") as f:
    key = json.load(f)

bot = Bot(token=key["telegram"])

dp = Dispatcher(bot)

# web3
w3 = Web3(Web3.HTTPProvider("https://api.avax.network/ext/bc/C/rpc"))
if not w3.isConnected():
    print("Error web3 can't connect")
sherpatoken_contract = w3.eth.contract(address=Constants.SHERPATOKEN_ADDRESS, abi=Constants.SHERPATOKEN_ABI)


@dp.message_handler(commands='price')
async def price(message: types.Message):
    '''return the current price of $Sherpa'''
    price = await PangoSubGraph.getSherpaPrice()
    await bot.send_message(message.chat.id, "SHERPA price is ${}".format(round(price, 4)))


@dp.message_handler(commands='about')
async def about(message: types.Message):
    '''return the current price of $Sherpa, the market cap and the circulating supply.'''
    price = await PangoSubGraph.getSherpaPrice()
    csupply_max = float(w3.fromWei(sherpatoken_contract.functions.totalSupply().call(), 'ether'))
    mainWallet_balance = float(w3.fromWei(sherpatoken_contract.functions.balanceOf("0xC3CA3d91682c4bB7c8eE8E3fC0E24E43D4f94717").call(), 'ether'))
    # print(csupply_max, mainWallet_balance)
    csupply = csupply_max - mainWallet_balance
    mktcap = price * csupply
    await bot.send_message(message.chat.id, """SHERPA price is ${}
Market Cap: ${}
Circ. Supply: {}""".format(readable(price, 4), human_format(mktcap), human_format(csupply)))


@dp.message_handler(commands='help')
async def help(message: types.Message):
    '''print Constants.HELP_TG'''
    await bot.send_message(message.chat.id, Constants.HELP_TG)


if __name__ == "__main__":
    executor.start_polling(dp)
