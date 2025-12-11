# Zefoy.com Full Client-Side Reversal (2025)  
**Bypassing All Anti-Bot Protections**

> Reverse Engineered from: `https://zefoy.com/assets/53fbc84b11a13a7942a850361e5d7b49.js`  
> Deobfuscated with: https://obf-io.deobfuscate.io/  
> **Status: Fully bypassed** (CAPTCHA + Fingerprint + Mouse Simulation + Cookies)

![zefoy banner](https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=200&section=header&text=Zefoy%20Reversed&fontSize=60&fontAlignY=38&animation=fadeIn&fontColor=ffffff)

---

### I. How I Reversed It – Step by Step

| Step | What Zefoy Does | How I Broke It |
|------|------------------|----------------|
| 1    | `cf_ob_te` cookie anti-automation trap | Replicated exact stack trace logic |
| 2    | `ltj` timestamp cookie (now removed) | Still works if server checks old versions |
| 3    | Encrypted fingerprint via CryptoJS AES | Found static key: `43fdda1192dde7f8ffff7161e13580d7` |
| 4    | Mouse movement simulation (obfuscated state string) | Reversed XOR + Base64 + Reverse trick |
| 5    | Base64 + URL decode + reverse response | Simple but hidden in JS |

---

### II. 1. `cf_ob_te` Cookie Generator (Anti-Bot Trap)

**Zefoy tries to detect automation by checking **where** certain events are triggered from**.

```js
// Original obfuscated snippet
if (!_0x290eee.some(_0x16ae9d => _0x58f9d8.includes(_0x16ae9d) || _0x38b87c.includes(_0x16ae9d))) {
    document.cookie = "cf_ob_te=" + btoa("Kod: " + _0x41f16f + " \nsource: " + _0x58f9d8.trim());
}
```

**My Python implementation:**

```python
def cf_ob_te_cookie() -> str | None:
    ignore_list = [
        "pagead2.googlesyndication.com", "googletagmanager.com",
        "www.googletagmanager.com", "ep2.adtrafficquality.google",
        "cdnjs.cloudflare.com", "boq-content-ads-contributor"
    ]
    stack = traceback.format_stack()[:-1]
    stack_str = "\n".join(stack)
    source = "not_found_source"
    for frame in stack:
        if not any(bad in frame for bad in ["HTMLElement.", "EventTarget.", "Proxy.", "<anonymous>", "dispatchEvent", "Object."]):
            source = frame.strip()
            break
    if any(ignored in source or ignored in stack_str for ignored in ignore_list):
        return None
    payload = f"Kod: unknown\nsource: {source}"
    cookie_value = base64.b64encode(payload.encode()).decode()
    expiry = (datetime.now() + timedelta(hours=5)).strftime("%a, %d %b %Y %H:%M:%S GMT")
    return f"cf_ob_te={cookie_value}; Path=/; Expires={expiry}"
```

> This cookie **must be sent** or you get blocked instantly.

---

### III. 2. Fingerprint Generation + CryptoJS AES Encryption

The most important part — they encrypt the entire browser fingerprint using **CryptoJS AES-CBC** with a **hardcoded key**.

```js
var _0x475601 = CryptoJS.AES.encrypt(_0x1eee13, "43fdda1192dde7f8ffff7161e13580d7", _0x1fb2fd).toString();
```

**Static Key Found:**  
```text
43fdda1192dde7f8ffff7161e13580d7
```

**Full working Python encryptor (CryptoJS compatible):**

```python
def evp_bytes_to_key(password: bytes, salt: bytes):
    dtot = b""
    d = b""
    while len(dtot) < 48:
        d = hashlib.md5(d + password + salt).digest()
        dtot += d
    return dtot[:32], dtot[32:48]

def cryptojs_aes_encrypt(plaintext: str) -> dict:
    password = "43fdda1192dde7f8ffff7161e13580d7"
    salt = os.urandom(8)
    key, iv = evp_bytes_to_key(password.encode(), salt)
    padded = plaintext.encode() + bytes([16] * (16 - len(plaintext) % 16))
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ct = cipher.encrypt(padded)
    return {
        "ct": base64.b64encode(ct).decode(),
        "iv": iv.hex(),
        "s": salt.hex()
    }
```

Decrypt example:

```python
def cryptojs_aes_decrypt(data: dict) -> str:
    salt = bytes.fromhex(data['s'])
    iv = bytes.fromhex(data['iv'])
    ct = base64.b64decode(data['ct'])
    key, _ = evp_bytes_to_key("43fdda1192dde7f8ffff7161e13580d7".encode(), salt)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), 16)
    return pt.decode()
```

---

### IV. Realistic Fingerprint Generator (Spoofed)

```python
def generate_fingerprint() -> str:
    fp = {
        "deviceInfo": {
            "cpuCores": random.choice([8, 12, 16]),
            "deviceMemoryGB": random.choice([8, 16]),
            "platform": "Win32",
            "gpu": {
                "vendor": "Google Inc. (NVIDIA)",
                "renderer": "ANGLE (NVIDIA GeForce RTX 3060 Direct3D11 vs_5_0 ps_5_0)"
            },
            "battery": {"charging": True, "level": round(random.uniform(0.6, 1.0), 2)},
            "touchSupport": "No"
        },
        "browserInfo": {
            "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/137.0 Safari/537.36",
            "timezone": "Africa/Cairo",
            "language": "en-US",
            "webdriver": False,
            "isBot": "No"
        },
        "screenInfo": {
            "width": 1920, "height": 1080,
            "colorDepth": 24, "devicePixelRatio": 1
        }
    }
    return json.dumps(fp, separators=(",", ":"))
```

Then encrypt it:

```python
encrypted_fp = cryptojs_aes_encrypt(generate_fingerprint())
# Send → encrypted_fp['ct'], encrypted_fp['iv'], encrypted_fp['s']
```

---

### V. Mouse Movement Obfuscated State String (K9x! Magic)

One of the most annoying parts — heavily obfuscated.

```js
"K9x!" + xored_string + "K9x!" → Base64 → reverse → b64encode
```

**My clean reimplementation:**

```python
def encode_state_string() -> str:
    s = f"x={random.randint(100,1800)}&y={random.randint(100,900)}&d={random.uniform(0.01,1.2):.3f}&g=False"
    xored = "".join(chr(ord(c) ^ ((i % 5) + 77)) for i, c in enumerate(s))
    final = base64.b64encode(("K9x!" + xored + "K9x!").encode()).decode()[::-1]
    return final
```

This string goes into the hidden input field (or all `.input` fields).

---

![footer](https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=120&section=footer)
```


Enjoy with Fu*k Zefoy.
```
