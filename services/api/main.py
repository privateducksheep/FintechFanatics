# ----------------------
# Imports
# ----------------------
# FastAPI
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


# Firebase Admin
import firebase_admin
from firebase_admin import credentials, auth

# XRPL
from xrpl.wallet import Wallet
from xrpl.account import get_balance
from xrpl.models.transactions import Payment
from xrpl.transaction import autofill_and_sign, submit_and_wait

from xrpl.utils import xrp_to_drops

from xrpl.asyncio.clients import AsyncJsonRpcClient
from xrpl.asyncio.account import get_balance
from xrpl.asyncio.transaction import autofill_and_sign, submit_and_wait

# Environment
import os
from dotenv import load_dotenv

# ----------------------
# Load environment variables
# ----------------------
load_dotenv()

XRPL_SERVER = os.getenv("XRPL_SERVER") or "https://s.altnet.rippletest.net:51234"
client = AsyncJsonRpcClient(XRPL_SERVER)

# ----------------------
# Firebase initialization
# ----------------------
cred_path = "serviceAccountKey.json"  # put your JSON file here locally
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)

# ----------------------
# FastAPI setup
# ----------------------
app = FastAPI(title="FintechFanatics Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)

class MeBody(BaseModel):
    id_token: str

class WalletInitBody(BaseModel):
    uid: str

class SendTxBody(BaseModel):
    uid: str
    to: str
    amount: float

# ----------------------
# In-memory wallet store
# ----------------------
# Structure: { uid: Wallet() }
wallets = {}

# ----------------------
# /me - Firebase token verification
# ----------------------
@app.post("/me")
async def verify_token(body: MeBody):
    try:
        decoded = auth.verify_id_token(body.id_token)
        return {"uid": decoded["uid"]}
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid Firebase token")

# ----------------------
# /wallet/init - create/get wallet
# ----------------------
@app.post("/wallet/init")
async def wallet_init(body: WalletInitBody):
    uid = body.uid
    if uid not in wallets:
        wallets[uid] = Wallet.create()
    return {"address": wallets[uid].classic_address}

# ----------------------
# /wallet/balance - get XRP balance
# ----------------------
@app.get("/wallet/balance")
async def wallet_balance(uid: str):
    wallet = wallets.get(uid)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not initialized")
    try:
        balance = await get_balance(wallet.classic_address, client)
        return {"balance": balance}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ----------------------
# /tx/send - send XRP
# ----------------------
@app.post("/tx/send")
async def send_tx(body: SendTxBody):
    uid = body.uid
    to = body.to
    amount = body.amount
    
    wallet = wallets.get(uid)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not initialized")
    try:
        payment = Payment(
            account=wallet.classic_address,
            destination=to,
            amount=xrp_to_drops(amount)
        )
        # Fill sequence, fee, last ledger & sign
        signed_tx = await autofill_and_sign(payment, client, wallet)
        # Submit to XRPL
        response = await submit_and_wait(signed_tx, client)
        return {"tx_hash": response.result.get("hash")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ----------------------
# /tx/history - optional placeholder
# ----------------------
@app.get("/tx/history")
async def tx_history(uid: str):
    # Implement XRPL account_tx or local storage if needed
    return {"history": []}
