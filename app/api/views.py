from django.shortcuts import render, redirect
from web3 import Web3
import os

from dotenv import load_dotenv

load_dotenv()

import requests
import json

from .forms import SurveyForm
from .models import Survey

from django.utils import timezone
from datetime import *


from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from django.contrib import messages

# GOERLI Test Wallet where the ERC20 Token was deployed
my_account = "0x3eDb1E13ae5D632a555128E57052B7662106DEa6"
private_key = os.getenv("PRIVATE_KEY")

# GOERLI Infura test net
web3 = Web3(
    Web3.HTTPProvider("https://goerli.infura.io/v3/ca8d7422b9de421bb11a1dd384b64102")
)
chain_id = 5
print(web3.is_connected())

# Smart Contract Data
token_abi = [
    {
        "inputs": [
            {"internalType": "address", "name": "spender", "type": "address"},
            {"internalType": "uint256", "name": "value", "type": "uint256"},
        ],
        "name": "approve",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "spender", "type": "address"},
            {"internalType": "uint256", "name": "requestedDecrease", "type": "uint256"},
        ],
        "name": "decreaseAllowance",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "string", "name": "name", "type": "string"},
            {"internalType": "string", "name": "symbol", "type": "string"},
            {"internalType": "uint256", "name": "initialSupply", "type": "uint256"},
        ],
        "stateMutability": "nonpayable",
        "type": "constructor",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "spender", "type": "address"},
            {"internalType": "uint256", "name": "currentAllowance", "type": "uint256"},
            {"internalType": "uint256", "name": "requestedDecrease", "type": "uint256"},
        ],
        "name": "ERC20FailedDecreaseAllowance",
        "type": "error",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "spender", "type": "address"},
            {"internalType": "uint256", "name": "allowance", "type": "uint256"},
            {"internalType": "uint256", "name": "needed", "type": "uint256"},
        ],
        "name": "ERC20InsufficientAllowance",
        "type": "error",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "sender", "type": "address"},
            {"internalType": "uint256", "name": "balance", "type": "uint256"},
            {"internalType": "uint256", "name": "needed", "type": "uint256"},
        ],
        "name": "ERC20InsufficientBalance",
        "type": "error",
    },
    {
        "inputs": [{"internalType": "address", "name": "approver", "type": "address"}],
        "name": "ERC20InvalidApprover",
        "type": "error",
    },
    {
        "inputs": [{"internalType": "address", "name": "receiver", "type": "address"}],
        "name": "ERC20InvalidReceiver",
        "type": "error",
    },
    {
        "inputs": [{"internalType": "address", "name": "sender", "type": "address"}],
        "name": "ERC20InvalidSender",
        "type": "error",
    },
    {
        "inputs": [{"internalType": "address", "name": "spender", "type": "address"}],
        "name": "ERC20InvalidSpender",
        "type": "error",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "owner",
                "type": "address",
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "spender",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "value",
                "type": "uint256",
            },
        ],
        "name": "Approval",
        "type": "event",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "spender", "type": "address"},
            {"internalType": "uint256", "name": "addedValue", "type": "uint256"},
        ],
        "name": "increaseAllowance",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "to", "type": "address"},
            {"internalType": "uint256", "name": "value", "type": "uint256"},
        ],
        "name": "transfer",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "from",
                "type": "address",
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "to",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "value",
                "type": "uint256",
            },
        ],
        "name": "Transfer",
        "type": "event",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "from", "type": "address"},
            {"internalType": "address", "name": "to", "type": "address"},
            {"internalType": "uint256", "name": "value", "type": "uint256"},
        ],
        "name": "transferFrom",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "owner", "type": "address"},
            {"internalType": "address", "name": "spender", "type": "address"},
        ],
        "name": "allowance",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "address", "name": "account", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "decimals",
        "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "name",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "symbol",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "totalSupply",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
]
contract_address = "0xd0E7330A453fA1B0AE0E077C531525347AE91218"
contract = web3.eth.contract(contract_address, abi=token_abi)


def homePage(request):
    return render(request, "app/homePage.html")


def tokenReward(request):
    if request.method == "POST":
        form = SurveyForm(request.POST)
        newSurvey = Survey()
        if form.is_valid():
            newSurvey.author = request.user
            newSurvey.date = datetime.now()
            newSurvey.email = form.cleaned_data.get("email")
            newSurvey.receipt = form.cleaned_data.get("receipt")
            newSurvey.receiptAmount = form.cleaned_data.get("receiptAmount")

            amount = int(form.cleaned_data.get("receiptAmount")) * 0.1
            ptkAmount = int(amount * 1000000000000000000)
            print(amount)
            print(ptkAmount)

            # Procedure with lib. web3 to send the Token to the user that compiled the form

            # From Metamask found the adress of the Wallet
            receiver_address = request.user.get_username()
            print(receiver_address)

            # Create the transaction:
            raw_txn = {
                "from": my_account,
                "gasPrice": web3.eth.gas_price,
                "gas": 200000,
                "to": contract_address,
                "value": "0x0",
                "data": contract.encodeABI(
                    "transfer", args=(receiver_address, 1000000000000000000)
                ),
                "nonce": web3.eth.get_transaction_count(my_account),
            }
            # Sign the transaction
            signed_txn = web3.eth.account.sign_transaction(raw_txn, private_key)
            # Send the transaction
            tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
            # Wait for the transaction to be mined, and get the transaction receipt
            print("Waiting for transaction to finish...")
            tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=600)
            print(f"Done! Contract deployed to {tx_receipt.contractAddress}")

            newSurvey.save()
            messages.success(
                request,
                "Your token request is correctly received - Tokens are now on your wallet - You could insert a new request or Logout.",
            )
            return redirect("homePage")
        else:
            return HttpResponse("Error")
    else:
        form = SurveyForm()
    return render(request, "app/tokenReward.html", {"form": form})


# MORALIS
# MORALIS_APP_ID = "60e99188-4387-46fd-af66-8033ad1a02ba"
# MORALIS_API_KEY = "iSJtrvy5e5c5KTMpC3Pu2NyI3Y2c7u4HsbtF7IrM97kwCUMtxMYMIaJ44JNXJ1sc"

API_KEY = "iSJtrvy5e5c5KTMpC3Pu2NyI3Y2c7u4HsbtF7IrM97kwCUMtxMYMIaJ44JNXJ1sc"
# this is a check to make sure the API key was set
# you have to set the API key only in line 9 above
# you don't have to change the next line
if API_KEY == "WEB3_API_KEY_HERE":
    print("API key is not set")
    raise SystemExit


def moralis_auth(request):
    return render(request, "app/login.html", {})


def my_profile(request):
    return render(request, "app/profile.html", {})


def request_message(request):
    data = json.loads(request.body)
    print(data)

    # setting request expiration time to 1 minute after the present->
    present = datetime.now(timezone.utc)
    present_plus_one_m = present + timedelta(minutes=1)
    expirationTime = str(present_plus_one_m.isoformat())
    expirationTime = str(expirationTime[:-6]) + "Z"

    REQUEST_URL = "https://authapi.moralis.io/challenge/request/evm"
    request_object = {
        "domain": "defi.finance",
        "chainId": 1,
        "address": data["address"],
        "statement": "Please confirm",
        "uri": "https://defi.finance/",
        "expirationTime": expirationTime,
        "notBefore": "2020-01-01T00:00:00.000Z",
        "timeout": 15,
    }
    x = requests.post(REQUEST_URL, json=request_object, headers={"X-API-KEY": API_KEY})

    return JsonResponse(json.loads(x.text))


def verify_message(request):
    data = json.loads(request.body)
    print(data)

    REQUEST_URL = "https://authapi.moralis.io/challenge/verify/evm"
    x = requests.post(REQUEST_URL, json=data, headers={"X-API-KEY": API_KEY})
    print(json.loads(x.text))
    print(x.status_code)
    if x.status_code == 201:
        # user can authenticate
        eth_address = json.loads(x.text).get("address")
        print("eth address", eth_address)
        try:
            user = User.objects.get(username=eth_address)
        except User.DoesNotExist:
            user = User(username=eth_address)
            user.is_staff = False
            user.is_superuser = False
            user.save()
        if user is not None:
            if user.is_active:
                login(request, user)
                request.session["auth_info"] = data
                request.session["verified_data"] = json.loads(x.text)
                return JsonResponse({"user": user.username})
            else:
                return JsonResponse({"error": "account disabled"})
    else:
        return JsonResponse(json.loads(x.text))
