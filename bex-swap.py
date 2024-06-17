
from eth_account import Account
from loguru import logger

from bera_tools import BeraChainTools
from config.address_config import (
    usdc_address, wbear_address, weth_address, bex_approve_liquidity_address,
    usdc_pool_liquidity_address, weth_pool_liquidity_address, honey_address
)

account = Account.from_key('pk')
bera = BeraChainTools(private_key=account.key, rpc_url='https://bartio.rpc.berachain.com/')

# bex 使用bera交换usdc
bera_balance = bera.w3.eth.get_balance(account.address)
print(bera_balance)
print("address: ", account.address)
result = bera.bex_swap(int(bera_balance * 0.2), wbear_address, honey_address)
logger.debug(result)

# exit 
exit()

# bex 使用usdc交换weth
usdc_balance = bera.usdc_contract.functions.balanceOf(account.address).call()
result = bera.bex_swap(int(usdc_balance * 0.2), usdc_address, weth_address)
logger.debug(result)

# 授权usdc
approve_result = bera.approve_token(bex_approve_liquidity_address, int("0x" + "f" * 64, 16), usdc_address)
logger.debug(approve_result)
# bex 增加 usdc 流动性
usdc_balance = bera.usdc_contract.functions.balanceOf(account.address).call()
result = bera.bex_add_liquidity(int(usdc_balance * 0.5), usdc_pool_liquidity_address, usdc_address)
logger.debug(result)

# 授权weth
approve_result = bera.approve_token(bex_approve_liquidity_address, int("0x" + "f" * 64, 16), weth_address)
logger.debug(approve_result)
# bex 增加 weth 流动性
weth_balance = bera.weth_contract.functions.balanceOf(account.address).call()
result = bera.bex_add_liquidity(int(weth_balance * 0.5), weth_pool_liquidity_address, weth_address)
logger.debug(result)