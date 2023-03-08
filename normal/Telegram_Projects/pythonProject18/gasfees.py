import requests, os
from ethprice import forgwei

#API = os.environ['ether']
getgas = "https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey="#+API
gweitoeth = 0.000000001


def gasfee():
    data = requests.get(getgas).json()

    low = int(data["result"]["SafeGasPrice"])
    avg = int(data["result"]["ProposeGasPrice"])
    fast = int(data["result"]["FastGasPrice"])
    usdp = forgwei()
  
    class feeusd:
        def __init__(self, usd):
            self.usd = str(round(usd * 21000 * usdp * gweitoeth, 3))
  
    lowp = feeusd(low)
    avgp = feeusd(avg)
    fastp = feeusd(fast)
    
    gasinfo = f"""<b><ins>Ethereum Live Gas Fees:</ins></b>
Low: <i>{low}</i> GWEI | ${lowp.usd}
Average: <i>{avg}</i> GWEI | ${avgp.usd}
High/Fast: <i>{fast}</i> GWEI | ${fastp.usd}
    
Powered by <a href=\"https://etherscan.io\">EtherScan</a>"""
    
    return gasinfo



def uniswap():
    data = requests.get(getgas).json()

    low = int(data["result"]["SafeGasPrice"])
    avg = int(data["result"]["ProposeGasPrice"])
    fast = int(data["result"]["FastGasPrice"])
    usdp = forgwei()

    class uniusd:
      def __init__(self, usd):
        self.usd = str(round(usd * 184523 * usdp * gweitoeth, 3))

    class univ2:
        def __init__(self, gafe):
            self.gafe = str(round(gafe * 152809 * usdp * gweitoeth, 3))

    unilow = uniusd(low)
    uniavg = uniusd(avg)
    unifast = uniusd(fast)

    unilow2 = univ2(low)
    uniavg2 = univ2(avg)
    unifast2 = univ2(fast)

    uniswapgas = f"""<b><ins>Uniswap ETH Live Gas Fees:</ins></b>
<b>V3</b>
Low: ${unilow.usd}
Average: ${uniavg.usd}
Fast: ${unifast.usd}

<b>V2</b>
Low: ${unilow2.gafe}
Average: ${uniavg2.gafe}
Fast: ${unifast2.gafe}

Powered by <a href=\"https://etherscan.io\">EtherScan</a>"""

    return uniswapgas


def erc20():
    data = requests.get(getgas).json()

    low = int(data["result"]["SafeGasPrice"])
    avg = int(data["result"]["ProposeGasPrice"])
    fast = int(data["result"]["FastGasPrice"])
    usdp = forgwei()

    class erc20fee:
        def __init__(self, fees):
            self.fees = str(round(fees * 65000 * usdp * gweitoeth, 3))

    erclow = erc20fee(low)
    ercavg = erc20fee(avg)
    ercfast = erc20fee(fast)

    ERC20Fees = f"""<b><ins>ERC-20 Token Transfer Fees:</ins></b>
Low: ${erclow.fees}
Average: ${ercavg.fees}
Fast: ${ercfast.fees}

Powered by <a href=\"https://etherscan.io\">EtherScan</a>"""

    return ERC20Fees

def ens():
    data = requests.get(getgas).json()

    low = int(data["result"]["SafeGasPrice"])
    avg = int(data["result"]["ProposeGasPrice"])
    fast = int(data["result"]["FastGasPrice"])
    usdp = forgwei()

    class gasfee:
        def __init__(self, fees):
            self.fees = str(round(fees * 266996 * usdp * gweitoeth, 3))

    low = gasfee(low)
    avg = gasfee(avg)
    fast = gasfee(fast)

    ens_registration_fees = f"""<b><ins>ENS: Domain Registration Fees</ins></b>
Low: ${low.fees}
Average: ${avg.fees}
Fast: ${fast.fees}

Powered by <a href=\"https://etherscan.io\">Etherscan</a>"""

    return ens_registration_fees
