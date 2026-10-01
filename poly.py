"""Polyester testnet API client — calls ConnectRPC services from inside the logged-in page."""
import json
import time

import cdp_browser as CB

API = "https://api.testnet.polyester.com"

JS_CALL = """
async ([base, path, payload, token]) => {
  const headers = {
    'content-type': 'application/json',
    'connect-protocol-version': '1',
  };
  if (token) headers['authorization'] = 'Bearer ' + token;
  const r = await fetch(base + '/' + path, {
    method: 'POST', headers, body: JSON.stringify(payload || {}),
  });
  let body;
  const txt = await r.text();
  try { body = JSON.parse(txt); } catch (e) { body = txt.slice(0, 2000); }
  return { status: r.status, body };
}
"""


class Poly:
    def __init__(self, page):
        self.page = page

    def token(self):
        for c in self.page.context.cookies():
            if c["name"] == "polyester_auth_token":
                return c["value"]
        return None

    def _usable(self):
        """True when the page sits on the app origin.

        Running the in-page fetch from the Cloudflare interstitial (or any other page)
        trips that page's CSP: connect-src blocks api.testnet.polyester.com and Playwright
        surfaces it as `Page.evaluate: TypeError: Failed to fetch`. Check before every call.
        """
        try:
            url = self.page.url or ""
        except Exception:
            return False
        if not url.startswith(CB.BASE):
            return False
        try:
            return not CB.is_challenge(self.page)
        except Exception:
            return False

    def _recover(self):
        """Re-seat the page on the app origin: wait out CF, else reload and re-inject."""
        try:
            if CB.is_challenge(self.page):
                CB.pass_cf(self.page, 90, "-api")
            if self._usable():
                return True
            self.page.goto(CB.BASE + "/account/dashboard",
                           wait_until="domcontentloaded", timeout=60000)
            CB.pass_cf(self.page, 90, "-api")
            if not self._usable():
                return False
            self.page.evaluate(CB.INJECT)
            return True
        except Exception:
            return False

    def call(self, path, payload=None, tries=4):
        last = None
        for i in range(tries):
            try:
                if not self._usable():
                    self._recover()
                return self.page.evaluate(JS_CALL, [API, path, payload or {}, self.token()])
            except Exception as e:
                last = e
                time.sleep(2 + 3 * i)
                self._recover()
        raise last

    # ---- convenience wrappers ----
    def me(self):
        return self.call("auth.v1.AuthService/Me", {})

    def profile(self):
        return self.call("auth.v1.ProfileService/GetProfile", {})

    def subaccounts(self):
        return self.call("auth.v1.SubaccountService/ListSubaccounts", {})

    def balances(self, subaccount_id=0):
        return self.call("ledger.read.v1.LedgerReadService/GetBalances", {"subaccountId": str(subaccount_id)})

    def claim_status(self):
        return self.call("claims.v1.ClaimsService/GetDailyClaimStatus", {})

    def claim(self):
        return self.call("claims.v1.ClaimsService/ClaimDailyReward", {})

    def social(self, provider):
        return self.call("auth.v1.SocialVerificationService/GetSocialVerification", {"provider": provider})

    def start_social(self, provider, method=1, handle=""):
        return self.call("auth.v1.SocialVerificationService/StartSocialVerification",
                         {"provider": provider, "method": method, "handle": handle})

    def social_ready(self, provider):
        return self.call("auth.v1.SocialVerificationService/SocialVerificationReady", {"provider": provider})

    def spot_config(self):
        return self.call("marketdata.v1.MarketDataService/GetSpotConfig", {})

    def zipper_config(self):
        return self.call("chain.zipper.v1.ZipperService/GetDepositWithdrawConfig", {})

    def list_deposit_addresses(self, chain_id=None, subaccount_id=None):
        p = {}
        if chain_id is not None:
            p["chainId"] = str(chain_id)
        if subaccount_id is not None:
            p["subaccountId"] = str(subaccount_id)
        return self.call("chain.deposit.v1.DepositAddressService/ListDepositAddresses", p)

    def create_deposit_address(self, chain_id, subaccount_id=0):
        return self.call("chain.deposit.v1.DepositAddressService/CreateDepositAddress",
                         {"chainId": str(chain_id), "subaccountId": str(subaccount_id)})

    def flows(self, subaccount_id=0):
        return self.call("chain.lifecycle.v1.LifecycleReadService/ListFlows",
                         {"subaccountId": str(subaccount_id)})

    def open_orders(self, subaccount_id=0):
        return self.call("orders.v1.OrdersReadService/GetOpenOrders", {"subaccountId": str(subaccount_id)})

    def order_history(self, subaccount_id=0):
        return self.call("orders.v1.OrdersReadService/GetOrderHistory", {"subaccountId": str(subaccount_id)})

    def trades(self, subaccount_id=0):
        # GetUserTrades rejects subaccountId=0 (must be >0); omit it.
        return self.call("orders.v1.OrdersReadService/GetUserTrades", {})

    def preview_order(self, intent, subaccount_id=0):
        return self.call("orders.v1.OrdersService/PreviewOrder",
                         {"subaccountId": str(subaccount_id), "order": intent})

    def create_order(self, intent, subaccount_id=0):
        return self.call("orders.v1.OrdersService/CreateOrder",
                         {"subaccountId": str(subaccount_id), "order": intent})

    def cancel_order(self, subaccount_id=0, **kw):
        p = {"subaccountId": str(subaccount_id)}
        p.update(kw)
        return self.call("orders.v1.OrdersService/CancelOrder", p)
