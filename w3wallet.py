"""Signing + RPC bridge bound into the injected browser wallet provider."""
import json
import os
import requests
from eth_account import Account
from eth_account.messages import encode_defunct

RPC = os.getenv("SEPOLIA_RPC", "https://ethereum-sepolia-rpc.publicnode.com")
CHAIN_ID = int(os.getenv("CHAIN_ID", "11155111"))


class WalletBridge:
    def __init__(self, pk: str):
        if not pk.startswith("0x"):
            pk = "0x" + pk
        self.pk = pk
        self.acct = Account.from_key(pk)
        self.address = self.acct.address
        self.chain_hex = hex(CHAIN_ID)

    # ---------- JSON-RPC ----------
    def rpc(self, method, params_json):
        params = json.loads(params_json) if isinstance(params_json, str) else (params_json or [])
        payload = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params}
        r = requests.post(RPC, json=payload, timeout=30,
                          headers={"Content-Type": "application/json"})
        d = r.json()
        if "error" in d:
            raise Exception(f"RPC {method}: {d['error']}")
        return d.get("result")

    # ---------- signatures ----------
    def sign_message(self, a, b=None):
        """personal_sign — data may be in either position."""
        is_addr = lambda v: isinstance(v, str) and v.startswith("0x") and len(v) == 42
        if is_addr(a) and b is not None:
            data = b
        else:
            data = a
        if isinstance(data, str) and data.startswith("0x"):
            try:
                msg = encode_defunct(hexstr=data)
            except Exception:
                msg = encode_defunct(text=data)
        else:
            msg = encode_defunct(text=str(data))
        signed = Account.sign_message(msg, private_key=self.pk)
        return signed.signature.hex() if not signed.signature.hex().startswith("0x") else signed.signature.hex()

    def sign_typed_data(self, payload_json):
        p = json.loads(payload_json) if isinstance(payload_json, str) else payload_json
        types = dict(p.get("types") or {})
        types.pop("EIP712Domain", None)
        signed = Account.sign_typed_data(
            self.pk,
            domain_data=p.get("domain") or {},
            message_types=types,
            message_data=p.get("message") or {},
        )
        sig = signed.signature.hex()
        return sig if sig.startswith("0x") else "0x" + sig

    def sign_typed_data_full(self, payload_json):
        p = json.loads(payload_json) if isinstance(payload_json, str) else payload_json
        signed = Account.sign_typed_data(self.pk, full_message=p)
        sig = signed.signature.hex()
        return sig if sig.startswith("0x") else "0x" + sig

    # ---------- transactions ----------
    def send_tx(self, tx_json):
        tx = json.loads(tx_json) if isinstance(tx_json, str) else dict(tx_json)
        tx.pop("from", None)
        if "chainId" not in tx:
            tx["chainId"] = CHAIN_ID
        if "nonce" not in tx:
            tx["nonce"] = int(self.rpc("eth_getTransactionCount", json.dumps([self.address, "pending"])), 16)
        if "gas" not in tx:
            est = {"from": self.address, "to": tx.get("to"),
                   "value": tx.get("value", "0x0"), "data": tx.get("data", "0x")}
            tx["gas"] = int(int(self.rpc("eth_estimateGas", json.dumps([est])), 16) * 1.25)
        for k in ("gasPrice", "maxFeePerGas", "maxPriorityFeePerGas", "value", "gas", "nonce", "chainId"):
            if k in tx and isinstance(tx[k], str):
                tx[k] = int(tx[k], 16)
        if "gasPrice" not in tx and "maxFeePerGas" not in tx:
            try:
                base = int(self.rpc("eth_getBlockByNumber", json.dumps(["latest", False]))["baseFeePerGas"], 16)
                tip = int(self.rpc("eth_maxPriorityFeePerGas", json.dumps([])), 16)
                tx["maxPriorityFeePerGas"] = max(tip, 10 ** 9)
                tx["maxFeePerGas"] = base * 2 + tx["maxPriorityFeePerGas"]
                tx["type"] = 2
            except Exception:
                tx["gasPrice"] = int(self.rpc("eth_gasPrice", json.dumps([])), 16)
        signed = Account.sign_transaction(tx, private_key=self.pk)
        raw = signed.raw_transaction.hex()
        if not raw.startswith("0x"):
            raw = "0x" + raw
        return self.rpc("eth_sendRawTransaction", json.dumps([raw]))

    def bind(self, page):
        page.expose_binding("__w_rpc", lambda source, m, p: self.rpc(m, p))
        page.expose_binding("__w_signMessage", lambda source, a, b=None: self.sign_message(a, b))
        page.expose_binding("__w_signTypedData", lambda source, p: self.sign_typed_data(p))
        page.expose_binding("__w_sendTx", lambda source, tx: self.send_tx(tx))
