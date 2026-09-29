// Injected EIP-1193 wallet provider (MetaMask-compatible).
// Signing + broadcast are delegated to the host process via exposed bindings:
//   window.__w_rpc(method, params)      -> JSON-RPC passthrough (read-only)
//   window.__w_signMessage(hexOrText)   -> personal_sign signature
//   window.__w_signTypedData(json)      -> EIP-712 signature
//   window.__w_sendTx(txJson)           -> broadcast raw tx, returns tx hash
(function () {
  if (window.__injectedWallet) return;
  window.__injectedWallet = true;

  const ACCOUNT = window.__WALLET_ADDRESS;
  const CHAIN_HEX = window.__WALLET_CHAIN_HEX || "0xaa36a7";
  const listeners = {};
  let curChain = CHAIN_HEX;
  let accounts = [];

  const emit = (ev, ...args) => {
    (listeners[ev] || []).forEach((f) => {
      try { f(...args); } catch (e) { console.error("listener err", e); }
    });
  };

  const LOCAL = new Set([
    "eth_requestAccounts", "eth_accounts", "eth_chainId", "net_version",
    "personal_sign", "eth_sign", "eth_signTypedData", "eth_signTypedData_v1",
    "eth_signTypedData_v3", "eth_signTypedData_v4",
    "eth_sendTransaction", "wallet_switchEthereumChain", "wallet_addEthereumChain",
    "wallet_requestPermissions", "wallet_getPermissions", "wallet_revokePermissions",
    "eth_requestAccounts", "eth_coinbase", "eth_sendRawTransaction",
  ]);

  async function request({ method, params }) {
    params = params || [];
    switch (method) {
      case "eth_requestAccounts":
        if (!accounts.length) {
          accounts = [ACCOUNT];
          setTimeout(() => emit("accountsChanged", accounts), 0);
        }
        return accounts;
      case "eth_accounts":
        return accounts;
      case "eth_coinbase":
        return ACCOUNT;
      case "eth_chainId":
        return curChain;
      case "net_version":
        return String(parseInt(curChain, 16));
      case "wallet_switchEthereumChain": {
        const want = params[0] && params[0].chainId;
        if (want && want !== curChain) {
          curChain = want;
          emit("chainChanged", curChain);
        }
        return null;
      }
      case "wallet_addEthereumChain":
        return null;
      case "wallet_requestPermissions":
        return [{ parentCapability: "eth_accounts" }];
      case "wallet_getPermissions":
        return [{ parentCapability: "eth_accounts" }];
      case "wallet_revokePermissions":
        return null;
      case "personal_sign":
      case "eth_sign":
        // params: [data, address] (or [address, data] for some wallets)
        return await window.__w_signMessage(params[0], params[1]);
      case "eth_signTypedData":
      case "eth_signTypedData_v1":
      case "eth_signTypedData_v3":
      case "eth_signTypedData_v4": {
        let payload = params[1];
        if (typeof payload === "string") payload = JSON.parse(payload);
        return await window.__w_signTypedData(JSON.stringify(payload));
      }
      case "eth_sendTransaction": {
        return await window.__w_sendTx(JSON.stringify(params[0]));
      }
      default:
        if (window.__w_rpc) return await window.__w_rpc(method, JSON.stringify(params || []));
        throw new Error("Unsupported method " + method);
    }
  }

  const provider = {
    isMetaMask: true,
    isConnected: () => true,
    get chainId() { return curChain; },
    get selectedAddress() { return accounts[0] || null; },
    get networkVersion() { return String(parseInt(curChain, 16)); },
    request,
    enable: () => request({ method: "eth_requestAccounts" }),
    send: (m, p) => {
      if (typeof m === "string") return request({ method: m, params: p });
      return request(m);
    },
    sendAsync: (payload, cb) => {
      request(payload).then((r) => cb(null, { id: payload.id, jsonrpc: "2.0", result: r }))
        .catch((e) => cb(e, null));
    },
    on: (ev, fn) => { (listeners[ev] = listeners[ev] || []).push(fn); return provider; },
    addListener: (ev, fn) => provider.on(ev, fn),
    once: (ev, fn) => { const w = (...a) => { provider.removeListener(ev, w); fn(...a); }; return provider.on(ev, w); },
    removeListener: (ev, fn) => { listeners[ev] = (listeners[ev] || []).filter((f) => f !== fn); return provider; },
    removeAllListeners: (ev) => { if (ev) delete listeners[ev]; else listeners = {}; return provider; },
    emit,
  };

  Object.defineProperty(window, "ethereum", { value: provider, writable: false, configurable: false });
  window.__providerReady = ACCOUNT;

  // EIP-6963 discovery
  const info = {
    uuid: "11111111-2222-3333-4444-555555555555",
    name: "MetaMask",
    icon: "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciLz4=",
    rdns: "io.metamask",
  };
  function announce() {
    window.dispatchEvent(new CustomEvent("eip6963:announceProvider", {
      detail: Object.freeze({ info, provider }),
    }));
  }
  window.addEventListener("eip6963:requestProvider", announce);
  setTimeout(announce, 0);
  setTimeout(announce, 300);
})();
