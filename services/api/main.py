# FastAPI
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Firebase Admin
import firebase_admin
from firebase_admin import credentials, auth

# XRPL
from xrpl.wallet import Wallet
from xrpl.clients import JsonRpcClient
from xrpl.models.transactions import Payment
from xrpl.transaction import autofill_transaction, safe_sign_transaction, submit_transaction
from xrpl.utils import xrp_to_drops

# Environment variables
import os
from dotenv import load_dotenv

# ----------------------
# Load environment vars
# ----------------------
load_dotenv()

# XRPL settings
XRPL_SERVER = os.getenv("XRPL_SERVER") or "https://s.altnet.rippletest.net:51234"
client = JsonRpcClient(XRPL_SERVER)

# Firebase service account JSON
# Put the JSON you downloaded in api/serviceAccountKey.json
cred_path = "serviceAccountKey.json"
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)

# FastAPI app
app = FastAPI(title="FintechFanatics Backend")

# Allow CORS (so frontend can call backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# ----------------------
# In-memory wallet store
# ----------------------
# { uid: Wallet() }
wallets = {}

# ----------------------
# /me endpoint - Firebase token verification
# ----------------------
@app.post("/tx/send")
async def send_tx(uid: str, to: str, amount: float):
    wallet = wallets.get(uid)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not initialized")

    try:
        # Create payment
        payment = Payment(
            account=wallet.classic_address,
            destination=to,
            amount=xrp_to_drops(amount),
        )

        # Autofill fee, sequence, last ledger
        payment = autofill_transaction(payment, client)
        # Sign transaction
        signed_tx = safe_sign_transaction(payment, wallet)
        # Submit to XRPL
        response = submit_transaction(signed_tx, client)

        return {"tx_hash": response.result["hash"]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ----------------------
# /wallet/init - create or get XRPL wallet
# ----------------------
@app.post("/wallet/init")
async def wallet_init(uid: str):
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
        balance = get_balance(wallet.classic_address, client)
        return {"balance": balance}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ----------------------
# /tx/send - send XRP
# ----------------------
client = JsonRpcClient(XRPL_SERVER)

@app.post("/tx/send")
async def send_tx(uid: str, to: str, amount: float):
    wallet = wallets.get(uid)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not initialized")
    try:
        payment = Payment(
            account=wallet.classic_address,
            destination=to,
            amount=xrp_to_drops(amount)
        )

        # Fill sequence, fee, last ledger etc.
        payment = autofill_transaction(payment, client)
        # Sign with wallet
        signed_tx = safe_sign_transaction(payment, wallet)
        # Submit
        tx_response = submit_transaction(signed_tx, client)

        return {"tx_hash": tx_response.result["hash"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ----------------------
# /tx/history - optional, not implemented fully
# ----------------------
@app.get("/tx/history")
async def tx_history(uid: str):
    # Placeholder: implement XRPL account_tx or store locally
    return {"history": []}
