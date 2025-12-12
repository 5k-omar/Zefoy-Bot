import os, json, time, random, base64, hashlib, traceback, urllib.parse
from datetime import datetime, timedelta, timezone
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


# =============================================================================

# I have Reversed all this form > https://zefoy.com/assets/53fbc84b11a13a7942a850361e5d7b49.js 
# i decode js file with > https://obf-io.deobfuscate.io/
# =============================================================================


# =============================================================================
# 1. cf_ob_te Cookie Generator
"""
(() => {
    var _0x290eee = ["pagead2.googlesyndication.com", "googletagmanager.com", "www.googletagmanager.com", "ep2.adtrafficquality.google", "cdnjs.cloudflare.com", "boq-content-ads-contributor", "reportPageEnds", "hnfanknocfeofbddgcijnmhnfnkdnaad", "ddgilliopjknmglnpkegbjpoilgachlm", "bfnaelmomeimhlpmgjnjophhpkkoljpa", "iidnbdjijdkbmajdffnidomddglmieko", "eppiocemhmnlbhjplcgkofciiegomcon", "cldmemdnllncchfahbcnjijheaolemfk", "[native code]"];
    var _0x70230a = new WeakSet();
    var _0x58dc76 = (_0x19e125, _0x41f16f) => {
        if ("undefined" != typeof event && event.isTrusted) {
            return;
        }
        let _0x38b87c = new Error().stack.split("\n").slice(2).join("\n");
        let _0x58f9d8 = _0x38b87c.split("\n").find(_0xc42880 => !(_0xc42880.includes("at HTMLElement.") || _0xc42880.includes("at EventTarget.") || _0xc42880.includes("at Proxy.") || _0xc42880.includes(" (<anonymous>)") || _0xc42880.includes("at dispatchEvent") || _0xc42880.includes("at Object."))) || "not_found_source";
        if (!_0x290eee.some(_0x16ae9d => _0x58f9d8.includes(_0x16ae9d) || _0x38b87c.includes(_0x16ae9d))) {
            ((_0x386c85, _0x58b3c1) => {
                let _0x406811 = new Date();
                _0x406811.setTime(_0x406811.getTime() + 18000000);
                document.cookie = _0x386c85 + "=" + _0x58b3c1 + "; path=/; expires=" + _0x406811.toUTCString();
            })("cf_ob_te", btoa("Kod: " + _0x41f16f + " \nsource: " + _0x58f9d8.trim()));
        }
    };
})();
"""
# =============================================================================
def cf_ob_te_cookie() -> str | None:
    ignore_list = [
        "pagead2.googlesyndication.com",
        "googletagmanager.com",
        "www.googletagmanager.com",
        "ep2.adtrafficquality.google",
        "cdnjs.cloudflare.com",
        "boq-content-ads-contributor",
    ]

    stack = traceback.format_stack()[:-1]
    stack_str = "\n".join(stack)

    source = "not_found_source"
    for frame in stack:
        if not any(
            bad in frame
            for bad in [
                "at HTMLElement.",
                "at EventTarget.",
                "at Proxy.",
                " (<anonymous>)",
                "at dispatchEvent",
                "at Object.",
            ]
        ):
            source = frame.strip()
            break

    if any(ignored in source or ignored in stack_str for ignored in ignore_list):
        return None

    payload = f"Kod: unknown\nsource: {source}"
    cookie_value = base64.b64encode(payload.encode()).decode()
    expiry = (datetime.now() + timedelta(hours=5)).strftime("%a, %d %b %Y %H:%M:%S GMT")
    return f"cf_ob_te={cookie_value}; Path=/; Expires={expiry}"



# =============================================================================
# 2. ltj Cookie Updater (Zefoy Now removed it but here the way anyway)
# From > https://zefoy.com/cdnjs
"""
# (function () {
#   var _0x3111ee = Math.floor(Date.now() / 1000);
#   var _0x2e1dbc = new Date(Date.now() + 604800000).toUTCString();
#   document.cookie = "ltj=" + _0x3111ee + "; path=/; expires=" + _0x2e1dbc;
#   setInterval(function () {
#     var _0x46c3ed = Math.floor(Date.now() / 1000);
#     document.cookie = "ltj=" + _0x46c3ed + "; path=/; expires=" + _0x2e1dbc;
#   }, 60000);
# })();
"""
# =============================================================================
def update_ltj_cookie() -> str:
    timestamp = int(time.time())
    expiry = (datetime.now(timezone.utc) + timedelta(days=7)).strftime("%a, %d %b %Y %H:%M:%S GMT")
    return f"ltj={timestamp}; Path=/; Expires={expiry}"


# =============================================================================
# 3. Base64 Decoder it just for decode result from zefoy
# =============================================================================
def decrypt_base64(encoded: str) -> str:
    return base64.b64decode(urllib.parse.unquote(encoded[::-1])).decode()
    


# =============================================================================
# 4. Fingerprint Generator
"""
var _0x39f21f = {
        "deviceInfo": {
            "cpuCores": _0x2e2616(() => navigator.hardwareConcurrency),
            "cpuLoad": function() {
                try {
                    var _0x2e2c96 = performance.now();
                    for (var _0x30b7cb = 0; _0x30b7cb < 10000000; _0x30b7cb++) {
                        ;
                    }
                    return Math.round(performance.now() - _0x2e2c96);
                } catch (_0x320fa5) {
                    return "Not Supported";
                }
            }(),
            "deviceMemoryGB": _0x2e2616(() => navigator.deviceMemory),
            "platform": _0x2e2616(() => navigator.platform),
            "maxTouchPoints": _0x2e2616(() => navigator.maxTouchPoints),
            "msMaxTouchPoints": _0x2e2616(() => navigator.msMaxTouchPoints),
            "gpu": function() {
                try {
                    var _0xeaf4c = document.createElement("canvas");
                    var _0xea9668 = _0xeaf4c.getContext("webgl") || _0xeaf4c.getContext("experimental-webgl");
                    var _0x44cdf6 = {
                        vendor: "Not Supported",
                        renderer: "Not Supported"
                    };
                    if (!_0xea9668) {
                        return _0x44cdf6;
                    }
                    var _0x1ce27d = _0xea9668.getExtension("WEBGL_debug_renderer_info");
                    return {
                        "vendor": _0x1ce27d ? _0xea9668.getParameter(_0x1ce27d.UNMASKED_VENDOR_WEBGL) : "Not Supported",
                        "renderer": _0x1ce27d ? _0xea9668.getParameter(_0x1ce27d.UNMASKED_RENDERER_WEBGL) : "Not Supported"
                    };
                } catch (_0x51a3e4) {
                    var _0x1f79ea = {
                        "vendor": "Not Supported",
                        "renderer": "Not Supported"
                    };
                    return _0x1f79ea;
                }
            }(),
            "battery": _0x34e455 && undefined !== _0x34e455.charging ? {
                "charging": _0x34e455.charging,
                "level": _0x34e455.level,
                "chargingTime": _0x34e455.chargingTime,
                "dischargingTime": _0x34e455.dischargingTime
            } : "Not Supported",
            "stylusDetection": _0x2e2616(() => navigator.pointerEnabled) ? "Yes" : "No",
            "touchSupport": _0x2e2616(() => "ontouchstart" in window ? "Yes" : "No")
        },
        "browserInfo": {
            "userAgent": _0x2e2616(() => navigator.userAgent),
            "timezone": _0x2e2616(() => Intl.DateTimeFormat().resolvedOptions().timeZone),
            "timezoneOffset": _0x2e2616(() => new Date().getTimezoneOffset()),
            "localeDateTime": _0x2e2616(() => new Date().toLocaleString()),
            "localUnixTime": Math.floor(Date.now() / 1000),
            "calendar": _0x2e2616(() => Intl.DateTimeFormat().resolvedOptions().calendar),
            "day": _0x2e2616(() => Intl.DateTimeFormat().resolvedOptions().day),
            "locale": _0x2e2616(() => Intl.DateTimeFormat().resolvedOptions().locale),
            "month": _0x2e2616(() => Intl.DateTimeFormat().resolvedOptions().month),
            "numberingSystem": _0x2e2616(() => Intl.DateTimeFormat().resolvedOptions().numberingSystem),
            "year": _0x2e2616(() => Intl.DateTimeFormat().resolvedOptions().year),
            "appName": _0x2e2616(() => navigator.appName),
            "appVersion": _0x2e2616(() => navigator.appVersion),
            "vendor": _0x2e2616(() => navigator.vendor),
            "language": _0x2e2616(() => navigator.language),
            "languages": _0x2e2616(() => navigator.languages),
            "cookieEnabled": _0x2e2616(() => navigator.cookieEnabled),
            "onlineStatus": _0x2e2616(() => navigator.onLine ? "Online" : "Offline"),
            "javaEnabled": _0x2e2616(() => "function" == typeof navigator.javaEnabled ? navigator.javaEnabled() : "Not Supported"),
            "doNotTrack": _0x2e2616(() => navigator.doNotTrack),
            "referrerHeader": _0x2e2616(() => document.referrer) || "None",
            "httpsConnection": _0x2e2616(() => window.isSecureContext ? "Yes" : "No"),
            "historyLength": _0x2e2616(() => window.history.length),
            "mimeTypes": _0x2e2616(() => navigator.mimeTypes.length),
            "plugins": _0x2e2616(() => navigator.plugins.length),
            "webdriver": _0x2e2616(() => navigator.webdriver),
            "pageVisibility": _0x2e2616(() => document.visibilityState),
            "isBot": function() {
                try {
                    var _0x23f8f1 = ["__webdriver_evaluate", "__selenium_evaluate", "__webdriver_script_function", "__webdriver_script_func", "__webdriver_script_fn", "__fxdriver_evaluate", "__driver_unwrapped", "__webdriver_unwrapped", "__driver_evaluate", "__selenium_unwrapped", "__fxdriver_unwrapped"];
                    var _0x328017 = ["_phantom", "__nightmare", "_selenium", "callPhantom", "callSelenium", "_Selenium_IDE_Recorder"];
                    for (var _0x12727a = 0; _0x12727a < _0x328017.length; _0x12727a++) {
                        if (window[_0x328017[_0x12727a]]) {
                            return "Yes";
                        }
                    }
                    for (var _0x3b6309 = 0; _0x3b6309 < _0x23f8f1.length; _0x3b6309++) {
                        if (document[_0x23f8f1[_0x3b6309]]) {
                            return "Yes";
                        }
                    }
                    if (window.external && "function" == typeof window.external.toString && -1 !== window.external.toString().indexOf("Sequentum")) {
                        return "Yes";
                    }
                    var _0x1843e8 = ["selenium", "webdriver", "driver"];
                    for (var _0x46868a = 0; _0x46868a < _0x1843e8.length; _0x46868a++) {
                        if (document.documentElement.getAttribute(_0x1843e8[_0x46868a])) {
                            return "Yes";
                        }
                    }
                } catch (_0x144d76) {}
                return "No";
            }(),
            "featuresSupported": {
                "geolocation": _0x2e2616(() => "geolocation" in navigator ? "Yes" : "No"),
                "serviceWorker": _0x2e2616(() => "serviceWorker" in navigator ? "Yes" : "No"),
                "localStorage": _0x2e2616(() => "localStorage" in window ? "Yes" : "No"),
                "sessionStorage": _0x2e2616(() => "sessionStorage" in window ? "Yes" : "No"),
                "indexedDB": _0x2e2616(() => "indexedDB" in window ? "Yes" : "No"),
                "notifications": _0x2e2616(() => "Notification" in window ? "Yes" : "No"),
                "notificationsFirebase": _0x2e2616(() => "undefined" != typeof Notification ? Notification.permission : "Not Supported"),
                "clipboard": _0x2e2616(() => "clipboard" in navigator ? "Yes" : "No"),
                "pushAPI": _0x2e2616(() => "PushManager" in window ? "Yes" : "No"),
                "webRTC": _0x2e2616(() => "RTCPeerConnection" in window ? "Yes" : "No"),
                "gamepadAPI": _0x2e2616(() => "getGamepads" in navigator ? "Yes" : "No"),
                "speechSynthesis": _0x2e2616(() => "speechSynthesis" in window ? "Yes" : "No"),
                "webGL": _0x2e2616(() => "WebGLRenderingContext" in window ? "Yes" : "No"),
                "vibrationAPI": _0x2e2616(() => "vibrate" in navigator ? "Yes" : "No"),
                "deviceMotion": _0x2e2616(() => "DeviceMotionEvent" in window ? "Yes" : "No"),
                "deviceOrientation": _0x2e2616(() => "DeviceOrientationEvent" in window ? "Yes" : "No"),
                "wakeLock": _0x2e2616(() => "wakeLock" in navigator ? "Yes" : "No"),
                "serial": _0x2e2616(() => "serial" in navigator ? "Yes" : "No"),
                "usb": _0x2e2616(() => "usb" in navigator ? "Yes" : "No"),
                "networkInformation": _0x2e2616(() => "connection" in navigator ? "Yes" : "No"),
                "screenCapture": _0x2e2616(() => navigator.mediaDevices && "getDisplayMedia" in navigator.mediaDevices ? "Yes" : "No"),
                "fullscreenAPI": _0x2e2616(() => "fullscreenEnabled" in document ? "Yes" : "No"),
                "pictureInPicture": _0x2e2616(() => "pictureInPictureEnabled" in document ? "Yes" : "No")
            }
        },
        "screenInfo": {
            "width": _0x2e2616(() => screen.width),
            "height": _0x2e2616(() => screen.height),
            "colorDepth": _0x2e2616(() => screen.colorDepth),
            "pixelDepth": _0x2e2616(() => screen.pixelDepth),
            "devicePixelRatio": _0x2e2616(() => window.devicePixelRatio),
            "orientation": _0x2e2616(() => function() {
                try {
                    return screen.orientation && screen.orientation.type ? screen.orientation.type : "Not Supported";
                } catch (_0x5eed5a) {
                    return "Not Supported";
                }
            }()),
            "screenOrientationAngle": _0x2e2616(() => function() {
                try {
                    return screen.orientation && undefined !== screen.orientation.angle ? screen.orientation.angle : "Not Supported";
                } catch (_0x464ff8) {
                    return "Not Supported";
                }
            }()),
            "availableWidth": _0x2e2616(() => screen.availWidth),
            "availableHeight": _0x2e2616(() => screen.availHeight),
            "screenLeft": _0x2e2616(() => window.screenLeft),
            "screenTop": _0x2e2616(() => window.screenTop),
            "outerWidth": _0x2e2616(() => window.outerWidth),
            "outerHeight": _0x2e2616(() => window.outerHeight),
            "innerWidth": _0x2e2616(() => window.innerWidth),
            "innerHeight": _0x2e2616(() => window.innerHeight)
        },
        "otherData": {
            "mouseAvailable": _0x2e2616(() => "onmousemove" in window ? "Yes" : "No"),
            "keyboardAvailable": _0x2e2616(() => "onkeydown" in window ? "Yes" : "No"),
            "bluetoothSupport": _0x2e2616(() => "bluetooth" in navigator ? "Yes" : "No"),
            "usbSupport": _0x2e2616(() => "usb" in navigator ? "Yes" : "No"),
            "gamepadSupport": _0x2e2616(() => "getGamepads" in navigator ? "Yes" : "No"),
            "incognitoMode": _0x59b9ae
        },
        "storageInfo": {
            "localStorage": _0x2e2616(() => "localStorage" in window ? Object.keys(localStorage).length : "Not Supported"),
            "sessionStorage": _0x2e2616(() => "sessionStorage" in window ? Object.keys(sessionStorage).length : "Not Supported"),
            "indexedDB": _0x2e2616(() => "indexedDB" in window ? "Available" : "Not Supported"),
            "cacheStorage": _0x2e2616(() => "caches" in window ? "Available" : "Not Supported"),
            "storageEstimate": _0x2e2616(() => _0x1d3bcd || "Not Supported")
        }
    };
"""
# =============================================================================
def generate_fingerprint():
    return json.dumps({
        "deviceInfo": {
            "cpuCores": 4,
            "cpuLoad": random.randint(3, 12),
            "deviceMemoryGB": 8,
            "platform": "Win32",
            "maxTouchPoints": 0,
            "msMaxTouchPoints": "Not Supported",
            "gpu": {
                "vendor": "Google Inc. (NVIDIA)",
                "renderer": "ANGLE (NVIDIA, NVIDIA Quadro P600 (0x00001CBC) Direct3D11 vs_5_0 ps_5_0, D3D11)"
            },
            "battery": {
                "charging": True,
                "level": 1.0,
                "chargingTime": 0,
                "dischargingTime": None
            },
            "stylusDetection": "Yes",
            "touchSupport": "No"
        },
        "browserInfo": {
            "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "timezone": "Africa/Cairo",
            "timezoneOffset": -120,
            "localeDateTime": time.strftime("%m/%d/%Y, %I:%M:%S %p"),
            "localUnixTime": int(time.time()),
            "calendar": "gregory",
            "day": "numeric",
            "locale": "en-US",
            "month": "numeric",
            "numberingSystem": "latn",
            "year": "numeric",
            "appName": "Netscape",
            "appVersion": "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "vendor": "Google Inc.",
            "language": "en-US",
            "languages": ["en-US", "en"],
            "cookieEnabled": True,
            "onlineStatus": "Online",
            "javaEnabled": False,
            "doNotTrack": None,
            "referrerHeader": "None",
            "httpsConnection": "Yes",
            "historyLength": random.randint(3, 15),
            "mimeTypes": random.choice([2, 3, 4, 5]),
            "plugins": random.choice([4, 5, 6]),
            "webdriver": False,
            "pageVisibility": "visible",
            "isBot": "No",
            "featuresSupported": {
                "geolocation": "Yes", "serviceWorker": "Yes", "localStorage": "Yes",
                "sessionStorage": "Yes", "indexedDB": "Yes", "notifications": "Yes",
                "notificationsFirebase": "default", "clipboard": "Yes", "pushAPI": "Yes",
                "webRTC": "Yes", "gamepadAPI": "Yes", "speechSynthesis": "Yes",
                "webGL": "Yes", "vibrationAPI": "Yes", "deviceMotion": "Yes",
                "deviceOrientation": "Yes", "wakeLock": "Yes", "serial": "Yes",
                "usb": "Yes", "networkInformation": "Yes", "screenCapture": "Yes",
                "fullscreenAPI": "Yes", "pictureInPicture": "Yes"
            }
        },
        "screenInfo": {
            "width": 1920, "height": 1080, "colorDepth": 24, "pixelDepth": 24,
            "devicePixelRatio": 1, "orientation": "landscape-primary",
            "screenOrientationAngle": 0, "availableWidth": 1920, "availableHeight": 1040,
            "screenLeft": 0, "screenTop": 0, "outerWidth": 1920, "outerHeight": 1040,
            "innerWidth": 1920, "innerHeight": 953
        },
        "otherData": {
            "mouseAvailable": "Yes", "keyboardAvailable": "Yes",
            "bluetoothSupport": "Yes", "usbSupport": "Yes", "gamepadSupport": "Yes",
            "incognitoMode": "No"
        },
        "storageInfo": {
            "localStorage": random.randint(2, 8),
            "sessionStorage": 0,
            "indexedDB": "Available",
            "cacheStorage": "Available",
            "storageEstimate": {
                "quota": 161258822860,
                "usage": random.randint(5000, 50000),
                "usageDetails": {"indexedDB": random.randint(5000, 30000)}
            }
        }
    }, separators=(",", ":"))



def evp_bytes_to_key(password: bytes, salt: bytes):
    dtot = b""
    d = b""
    while len(dtot) < 32 + 16:
        d = hashlib.md5(d + password + salt).digest()
        dtot += d
    return dtot[:32], dtot[32:32 + 16]


# =============================================================================
# 5. 
""" you can found key easy here 

var _0x1eee13 = JSON.stringify(_0x39f21f);
    var _0x475601 = CryptoJS.AES.encrypt(_0x1eee13, "43fdda1192dde7f8ffff7161e13580d7", _0x1fb2fd).toString();
    if (undefined !== document.getElementById("captchaencoded") && null !== document.getElementById("captchaencoded")) {
        document.getElementById("captchaencoded").value = _0x475601;
    }
"""
# =============================================================================
def cryptojs_aes_encrypt(plaintext: str) -> dict:
    password: str = "43fdda1192dde7f8ffff7161e13580d7"
    salt = os.urandom(8)
    key, iv = evp_bytes_to_key(password.encode(), salt)
    padded = plaintext.encode() + bytes([16 - len(plaintext) % 16] * (16 - len(plaintext) % 16))
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ct = cipher.encrypt(padded)
    return {
        "ct": base64.b64encode(ct).decode(),
        "iv": iv.hex(),
        "s": salt.hex()
    }


# =============================================================================
# 6. This how to decode ct,iv,s
def cryptojs_aes_decrypt(encrypted_json: dict):
    salt = bytes.fromhex(encrypted_json['s'])
    iv = bytes.fromhex(encrypted_json['iv'])
    ciphertext = base64.b64decode(encrypted_json['ct'])

    key, iv = evp_bytes_to_key("43fdda1192dde7f8ffff7161e13580d7".encode('utf-8'), salt, 32, 16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(ciphertext)

    try:
        plaintext = unpad(decrypted, AES.block_size).decode('utf-8')
    except ValueError:
        raise ValueError("Invalid padding or incorrect password.")
    
    return plaintext

def Decode_Fingerprint(data):
    """
    Examble
    {
       "ct":"",
       "iv":"f5477b40a622fa99688f01ef524e871d",
       "s":"34b69fe809e8d479"
    }
    """
    return cryptojs_aes_decrypt(data)
# =============================================================================


# =============================================================================
# 7. Obfuscated state string (mouse movement simulation)
"""
function _0x5d0ea3() {
        const _0x2d89df = function(_0x2d8981) {
            let _0x3605c2 = '';
            for (let _0x3fd4aa = 0; _0x3fd4aa < _0x2d8981.length; _0x3fd4aa++) {
                _0x3605c2 += String.fromCharCode(_0x2d8981.charCodeAt(_0x3fd4aa) ^ _0x3fd4aa % 5 + 77);
            }
            return function(_0x108372) {
                let _0x27d0c4 = '';
                let _0x208821 = 0;
                for (; _0x208821 < _0x108372.length;) {
                    const _0x2273a0 = _0x108372.charCodeAt(_0x208821++);
                    const _0x5a3ae2 = _0x108372.charCodeAt(_0x208821++);
                    const _0x54bb21 = _0x108372.charCodeAt(_0x208821++);
                    const _0x54ce76 = (3 & _0x2273a0) << 4 | _0x5a3ae2 >> 4;
                    const _0x151857 = (15 & _0x5a3ae2) << 2 | _0x54bb21 >> 6;
                    const _0x344a61 = 63 & _0x54bb21;
                    _0x27d0c4 += "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=".charAt(_0x2273a0 >> 2) + "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=".charAt(_0x54ce76) + (isNaN(_0x5a3ae2) ? "=" : "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=".charAt(_0x151857)) + (isNaN(_0x54bb21) ? "=" : "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=".charAt(_0x344a61));
                }
                return _0x27d0c4;
            }("K9x!" + _0x3605c2 + "K9x!").split('').reverse().join('');
        }("x=0&y=0&d=" + 0x0.toFixed(2) + "&g=" + false);
        const _0x457738 = document.getElementById("input");
        if (_0x457738) {
            _0x457738.value = _0x2d89df;
        }
        const _0x2a986e = document.querySelectorAll(".input");
        if (_0x2a986e.length) {
            _0x2a986e.forEach(_0x276b3f => _0x276b3f.value = _0x2d89df);
        }
    }
"""
# =============================================================================
def encode_state_string():
    points = []
    num_points = random.randint(12, 28)
    
    for i in range(num_points):
        x = random.randint(50, 1900)
        y = random.randint(50, 1000)
        d = round(random.uniform(0.05, 2.8), 4)
        g = "True" if random.random() > 0.65 else "False"
        points.append(f"x={x}&y={y}&d={d}&g={g}")
    
    raw = "|".join(points)
    xored = "".join(chr(ord(c) ^ (i % 5 + 77)) for i, c in enumerate(raw))
    wrapped = "K9x!" + xored + "K9x!"
    encoded = base64.b64encode(wrapped.encode()).decode()
    final = encoded[::-1]
    final += "=" * ((4 - len(final) % 4) % 4)
    
    return final



# examble useeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
# if __name__ == "__main__":
#     print("cf_ob_te:", cf_ob_te_cookie())
#     print("ltj cookie:", update_ltj_cookie())
#     print("state string:", encode_state_string())
#     print("fingerprint:", cryptojs_aes_encrypt(generate_fingerprint()))
