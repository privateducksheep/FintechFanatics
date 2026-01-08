from fastapi import FastAPI, HTTPException
import firebase_admin
from firebase_admin import auth, credentials
import os
from dotenv import load_dotenv
import os

load_dotenv()  

cred = credentials.Certificate({
    "type": "service_account",
    "project_id": os.getenv("FIREBASE_PROJECT_ID"),
    "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
    "private_key": os.getenv("FIREBASE_PRIVATE_KEY").replace("\\n", "\n"),
    "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
    # other fields...
})
firebase_admin.initialize_app(cred)

app = FastAPI()

@app.post("/me")
async def verify_token(id_token: str):
    try:
        decoded_token = auth.verify_id_token(id_token)
        return {"uid": decoded_token["uid"]}
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")


from xrpl.wallet import Wallet

wallets = {}  # Simple in-memory store; can use DB

@app.post("/wallet/init")
async def wallet_init(uid: str):
    if uid not in wallets:
        seed = Wallet.create().seed
        wallets[uid] = Wallet(seed=seed, sequence=0)
    return {"address": wallets[uid].classic_address}


from xrpl.clients import JsonRpcClient
from xrpl.account import get_balance

client = JsonRpcClient(os.getenv("XRPL_SERVER"))

@app.get("/wallet/balance")
async def wallet_balance(uid: str):
    wallet = wallets.get(uid)
    if not wallet:
        raise HTTPException(404, detail="Wallet not initialized")
    balance = get_balance(wallet.classic_address, client)
    return {"balance": balance}


from xrpl.transaction import send_reliable_submission, safe_sign_and_autofill_transaction
from xrpl.models.transactions import Payment
from xrpl.utils import xrp_to_drops

@app.post("/tx/send")
async def send_tx(uid: str, to: str, amount: float):
    wallet = wallets.get(uid)
    if not wallet:
        raise HTTPException(404, detail="Wallet not initialized")
    payment = Payment(
        account=wallet.classic_address,
        amount=xrp_to_drops(amount),
        destination=to,
    )
    signed_tx = safe_sign_and_autofill_transaction(payment, wallet, client)
    tx_response = send_reliable_submission(signed_tx, client)
    return {"tx_hash": tx_response.result["hash"]}


