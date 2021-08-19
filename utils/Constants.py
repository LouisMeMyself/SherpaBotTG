# SubGraph link
import json

PANGO_API_URL = "https://api.thegraph.com/subgraphs/name/dasconnor/pangolin-dex"

# address for web3
SHERPATOKEN_ADDRESS = "0xa5E59761eBD4436fa4d20E1A27cBa29FB2471Fc6"


# ABI for web3
try:
    with open("utils/sherpaABI.json", "r") as f:
        SHERPATOKEN_ABI = json.load(f)
except:
    pass

# help
HELP_TG = """JoeBot commands:
/price : return the current price of $SHERPA.
/about : return the current price of $SHERPA, the market cap and the circulating supply.
"""