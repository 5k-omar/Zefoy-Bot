import base64
import logging
import random
import string
import json, time, re, sys, threading
from bs4 import BeautifulSoup
import httpx
import inquirer
import tls_client
from Log import Logger
import Reverse
from requests_toolbelt.multipart.encoder import MultipartEncoder
from PIL import Image, ImageFilter, ImageEnhance
from io import BytesIO
import webview

log = Logger()
GREEN = "\033[32m"
RED = "\033[31m"
RESET = "\033[0m"

logging.getLogger('pywebview').setLevel(logging.CRITICAL)


tls_session = tls_client.Session(
    client_identifier="chrome_124",
    random_tls_extension_order=True,
    force_http1=False,
    catch_panics=True,
    debug=False
)

def ImgToWinFromBytes(image_bytes, title="Enter Captcha") -> str:
    buf = BytesIO(image_bytes)
    img = Image.open(buf).convert("RGB").filter(ImageFilter.MedianFilter(3))
    img = ImageEnhance.Sharpness(img).enhance(2.0)
    img.thumbnail((400,300))
    buf_out = BytesIO()
    img.save(buf_out, format="PNG")
    img64 = base64.b64encode(buf_out.getvalue()).decode()

    class Api:
        def __init__(self):
            self.win = None
            self.text = None

        def send_text(self, text):
            self.text = text.strip()
            if self.text:
                threading.Thread(target=self.close_after_delay).start()
            return self.text

        def close_after_delay(self):
            time.sleep(2)
            if self.win:
               self.win.destroy()

    api = Api()

    html = f"""
    <html>
    <head>
    <meta charset="utf-8">
    <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%); display: flex; justify-content: center; align-items: center; height: 100vh; overflow: hidden; user-select: none; }}
    body::before {{ content: ''; position: absolute; width: 200%; height: 200%; background: radial-gradient(circle, rgba(94,156,255,0.1) 1px, transparent 1px); background-size: 50px 50px; animation: drift 20s linear infinite; pointer-events: none; }}
    @keyframes drift {{ from {{ transform: translate(0, 0); }} to {{ transform: translate(50px, 50px); }} }}
    .container {{ position: relative; background: rgba(15, 15, 35, 0.7); backdrop-filter: blur(20px) saturate(180%); -webkit-backdrop-filter: blur(20px) saturate(180%); padding: 35px; border-radius: 24px; border: 1px solid rgba(255, 255, 255, 0.1); box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.1); text-align: center; animation: slideIn 0.6s cubic-bezier(0.34, 1.56, 0.64, 1); cursor: grab; }}
    .container:active {{ cursor: grabbing; }}
    @keyframes slideIn {{ from {{ opacity: 0; transform: translateY(-30px) scale(0.9); }} to {{ opacity: 1; transform: translateY(0) scale(1); }} }}
    .header {{ color: #fff; font-size: 18px; font-weight: 600; text-shadow: 0 2px 10px rgba(0, 0, 0, 0.5); letter-spacing: 0.5px; margin-bottom: 20px; }}
    .img-wrapper {{ position: relative; margin-bottom: 25px; overflow: hidden; border-radius: 16px; }}
    img {{ width: 100%; border-radius: 16px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3); animation: glow 3s ease-in-out infinite; transition: transform 0.3s; }}
    @keyframes glow {{ 0%, 100% {{ filter: drop-shadow(0 0 8px rgba(94,156,255,0.4)); }} 50% {{ filter: drop-shadow(0 0 20px rgba(156,94,255,0.6)); }} }}
    input {{ width: 100%; padding: 15px 18px; border-radius: 12px; border: 2px solid rgba(255, 255, 255, 0.1); background: rgba(0, 0, 0, 0.3); color: #fff; font-size: 15px; margin-bottom: 18px; outline: none; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.2); }}
    input::placeholder {{ color: rgba(255, 255, 255, 0.4); }}
    input:focus {{ border-color: rgba(94, 156, 255, 0.8); background: rgba(0, 0, 0, 0.5); box-shadow: 0 0 0 4px rgba(94, 156, 255, 0.1), inset 0 2px 8px rgba(0, 0, 0, 0.2); transform: translateY(-1px); }}
    button {{ width: 100%; padding: 14px 28px; border: none; border-radius: 12px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #fff; font-weight: 600; font-size: 15px; cursor: pointer; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.2); position: relative; overflow: hidden; }}
    button::before {{ content: ''; position: absolute; inset: 0; background: linear-gradient(135deg, transparent 0%, rgba(255,255,255,0.2) 50%, transparent 100%); transform: translateX(-100%); transition: transform 0.6s; }}
    button:hover {{ transform: translateY(-2px); box-shadow: 0 6px 25px rgba(102, 126, 234, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.3); }}
    button:hover::before {{ transform: translateX(100%); }}
    button:active {{ transform: translateY(0); }}
    #msg {{ min-height: 28px; margin-top: 15px; color: #fff; font-size: 14px; font-weight: 500; opacity: 0; transition: opacity 0.3s; text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3); }}
    .close-btn {{ position: absolute; top: 12px; right: 12px; width: 32px; height: 32px; border-radius: 8px; background: rgba(255, 255, 255, 0.1); border: 1px solid rgba(255, 255, 255, 0.1); color: rgba(255, 255, 255, 0.6); font-size: 18px; cursor: pointer; transition: all 0.2s; display: flex; align-items: center; justify-content: center; z-index: 10; }}
    .close-btn:hover {{ background: rgba(255, 59, 48, 0.8); color: #fff; border-color: rgba(255, 59, 48, 0.8); transform: rotate(90deg); }}
    </style>
    </head>
    <body>
    <div class="container" id="win">
        <div class="close-btn" onclick="pywebview.api.send_text('')">×</div>
        <div class="header">Security Verification</div>
        <div class="img-wrapper">
            <img src="data:image/png;base64,{img64}" alt="Captcha">
        </div>
        <input id="txt" type="text" placeholder="Enter the text you see..." autofocus>
        <button onclick="send()">Verify & Continue</button>
        <div id="msg"></div>
    </div>
    <script>
    const win=document.getElementById('win');
    let offsetX,offsetY,drag=false;
    win.addEventListener('mousedown',e=>{{drag=true;offsetX=e.clientX-win.offsetLeft;offsetY=e.clientY-win.offsetTop;}});
    document.addEventListener('mouseup',()=>{{drag=false;}});
    document.addEventListener('mousemove',e=>{{if(drag){{win.style.position='absolute';win.style.left=(e.clientX-offsetX)+'px';win.style.top=(e.clientY-offsetY)+'px';}}}});
    document.getElementById('txt').addEventListener('keypress', function(e) {{ if (e.key === 'Enter') {{ send(); }} }});
    async function send(){{
        let t=document.getElementById('txt').value.trim();
        if(!t){{flash("⚠️ Please enter the captcha text",'#ff6b6b');return;}}
        await pywebview.api.send_text(t);
        flash("✓ Verified successfully!",'#51cf66');
        document.getElementById('txt').value='';
    }}
    function flash(m,c){{
        let e=document.getElementById('msg'); e.textContent=m; e.style.color=c; e.style.opacity=1;
        setTimeout(()=>e.style.opacity=0,2000);
    }}
    </script>
    </body>
    </html>
    """

    win = webview.create_window(title, html=html, width=450, height=550, frameless=True, resizable=False, js_api=api, on_top=True)
    api.win = win
    webview.start()
    return api.text

SERVICES = {
    "followers": "c2VuZF9mb2xsb3dlcnNfdGlrdG9r", # It always does not work
    "hearts": "c2VuZE9nb2xsb3dlcnNfdGlrdG9r",
    "comments_hearts": "c2VuZC9mb2xsb3dlcnNfdGlrdG9r", # After 30 starts with gui for select comment
    "views": "c2VuZC9mb2xeb3dlcnNfdGlrdG9V",
    "shares": "c2VuZC9mb2xsb3dlcnNfdGlrdG9s",
    "favorites": "c2VuZF9mb2xsb3dlcnNfdGlrdG9L",
    "livestream": "c2VuZC9mb2xsb3dlcnNfdGlrdGLL" # It always does not work
}

FINGERPRINT_CACHE = None
FINGERPRINT_ENCRYPTED = None

def Getfingerprint():
    global FINGERPRINT_CACHE, FINGERPRINT_ENCRYPTED
    if FINGERPRINT_CACHE is None:
        FINGERPRINT_CACHE = Reverse.generate_fingerprint()
        FINGERPRINT_ENCRYPTED = Reverse.cryptojs_aes_encrypt(FINGERPRINT_CACHE)
    return FINGERPRINT_ENCRYPTED

def Bypass_GoogleAds():
    try:
        r = tls_session.get("https://partner.googleadservices.com/gampad/cookie.js",
            params={"domain": "zefoy.com", "callback": "_gfp_s_", "client": "ca-pub-3192305768699763"})
        m = re.search(r"_gfp_s_\((.*?)\);", r.text, re.DOTALL)
        if m:
            cookies = json.loads(m.group(1))["_cookies_"]
            tls_session.cookies.set("__gads", cookies[0]["_value_"], domain="zefoy.com")
            tls_session.cookies.set("__gpi", cookies[1]["_value_"], domain="zefoy.com")
    except: pass

def Login():
    headers = {
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding":"gzip, deflate, br, zstd",
        "Accept-Language":"en-US,en;q=0.9",
        "Connection":"keep-alive",
        "sec-ch-ua":'"Google Chrome";v="137","Chromium";v="137","Not/A)Brand";v="24"',
        "sec-ch-ua-mobile":"?0",
        "sec-ch-ua-platform":'"Windows"',
        "Sec-Fetch-Dest":"document",
        "Sec-Fetch-Mode":"navigate",
        "Sec-Fetch-Site":"none",
        "Sec-Fetch-User":"?1",
        "Upgrade-Insecure-Requests":"1",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
    }
    
    response = tls_session.get("https://zefoy.com", headers=headers)
    if "Sorry, you have been blocked" in response.text or "Just a moment..." in response.text:
        log.error("Cloudflare detected — try later")
        sys.exit()

    img_path = re.search(r'src="(.*?)" onerror="errimg\(\)"', response.text)
    form_field = re.search(r'type="text" id="captchatoken" name="(.*?)"', response.text)
    if not img_path or not form_field: log.error("Captcha missing"); sys.exit()
    captcha_url = "https://zefoy.com"+img_path.group(1).replace("amp;","")

    log.info("Starting Boost")

    cookies_dict = {c.name:c.value for c in getattr(tls_session,"cookies",[])}
    with httpx.Client(cookies=cookies_dict) as img_client:
        captcha_img = img_client.get(captcha_url, headers=headers)
        if captcha_img.status_code!=200: log.error("Failed to get captcha"); sys.exit()
        image_bytes = captcha_img.content

    log.info("Please enter the captcha in the window and press Send")
    captcha_text = ImgToWinFromBytes(image_bytes)

    soup = BeautifulSoup(response.text,"html.parser")
    inp = soup.find('input',{'name':'captcha_encoded'})
    prev = inp.find_previous_sibling('input',{'type':'hidden'}) if inp else None
    dynamic_name = prev['name'] if prev and prev.has_attr('name') else "0fe6feb54289f4c67027ec06cc2131f8"

    post_data = {
        form_field.group(1): captcha_text,
        dynamic_name: Reverse.encode_state_string(),
        "captcha_encoded": json.dumps(Getfingerprint())
    }

    post_headers = headers.copy()
    post_headers.update({
        "Content-Type":"application/x-www-form-urlencoded",
        "Cache-Control":"max-age=0",
        "Origin":"https://zefoy.com",
        "Referer":"https://zefoy.com/",
        "Sec-Fetch-Site":"same-origin"
    })

    log.info("Submitting captcha...")
    post_resp = tls_session.post("https://zefoy.com/", headers=post_headers, data=post_data)
 
    time.sleep(2)
    check = tls_session.get("https://zefoy.com/", headers=headers)
    if 'placeholder="Enter Video URL"' in check.text:
        log.success("Captcha passed! Logged in.")
        return check.text
    else:
        log.error("Captcha failed.")
        print(check.text[:500])
        sys.exit()

def check_available_services(login_html: str):
    soup = BeautifulSoup(login_html, "html.parser")
    service_map = {
        "Followers": "followers",
        "Hearts": "hearts",
        "Comments Hearts": "comments_hearts",
        "Views": "views",
        "Shares": "shares",
        "Favorites": "favorites",
        "Live Stream": "livestream"
    }
    result = {v: False for v in service_map.values()}
    for card in soup.find_all("div", class_="card-body"):
        title_tag = card.find("h5", class_="card-title")
        badge = card.find("small")
        if not title_tag: continue
        title = title_tag.text.strip()
        if title not in service_map: continue
        key = service_map[title]
        badge_text = badge.text.strip().lower() if badge else ""
        result[key] = "soon" not in badge_text
    return result

def select_service(status: dict):
    while True:
        choices = []
        for service, ok in status.items():
            if service == "livestream": continue
            txt = f"{service.title()}  {GREEN}[Online]{RESET}" if ok else f"{service.title()}  {RED}[Not working]{RESET}"
            choices.append(txt)

        question = [inquirer.List("service", message="Choose a service", choices=choices)]
        answer = inquirer.prompt(question)
        selected_raw = answer["service"]

        clean = re.compile(r'\x1b\[[0-9;]*m').sub("", selected_raw)
        clean = clean.replace("[Online]", "").replace("[Not working]", "").strip().lower()

        if status.get(clean, False):
            return clean
        log.error(f"'{clean}' is not working right now!")

def Boost(video_form: str, service_key: str, video_url: str):
    endpoint = SERVICES[service_key]
    url = f"https://zefoy.com/{endpoint}"

    boundary = '----WebKitFormBoundary' + ''.join(random.sample(string.ascii_letters + string.digits, 16))
    data1 = MultipartEncoder({video_form: (None, video_url)}, boundary=boundary)

    headers = {
        "Content-Type": data1.content_type,
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://zefoy.com",
        "Referer": "https://zefoy.com/"
    }

    
    r1 = tls_session.post(url, data=data1.to_string(), headers=headers)
   
    time.sleep(random.uniform(2, 6))

    try:
        decoded1 = Reverse.decrypt_base64(r1.text)
    except Exception as e:
        log.error(f"Failed to decode response: {e}")
        return False

    if "This service is currently not working" in decoded1:
        log.error("Service is currently not working!")
        return False
    
    if "Please try again later or" in decoded1:
        log.error("Service unavailable - please try again later")
        return False
    
    if "Please try again later. Server too busy" in decoded1:
        log.error("Server is too busy - please try again later")
        time.sleep(random.uniform(30, 60))
        return False
    
    if "An error occurred. Please try again" in decoded1:
        log.error("An error occurred - retrying...")
        time.sleep(5)
        return False
    
    if "Too many requests. Please slow down" in decoded1:
        log.error("Rate limited - slowing down...")
        time.sleep(random.uniform(60, 120))
        return False

    if "Please wait" in decoded1:
        match = re.search(r'(\d+)', decoded1)
        if match:
            secs = int(match.group(1))
            log.cooldown(secs)
            return Boost(video_form, service_key, video_url)
        else:
            log.error("Cooldown detected but couldn't parse time")
            time.sleep(60)
            return False

    soup = BeautifulSoup(decoded1, "html.parser")
    form = soup.find("form")
    if not form:
        log.error("No form found after sending URL")
        return False

    payload = {}
    state_field_name = None

    for inp in form.find_all("input"):
        name = inp.get("name")
        if not name: 
            continue
        payload[name] = inp.get("value") or ""
        if inp.get("class") == ["input"]:
            state_field_name = name

    if not state_field_name:
        log.error("State field missing - possible blocking detected!")
        return False

    payload[state_field_name] = Reverse.encode_state_string()

    boundary2 = '----WebKitFormBoundary' + ''.join(random.sample(string.ascii_letters + string.digits, 16))
    data2 = MultipartEncoder({k: (None, v) for k, v in payload.items()}, boundary=boundary2)

    headers2 = headers.copy()
    headers2["Content-Type"] = data2.content_type

    action = form.get("action") or endpoint
    
    r2 = tls_session.post(f"https://zefoy.com/{action}", data=data2.to_string(), headers=headers2)
    
    final_decoded = Reverse.decrypt_base64(r2.text)
    
    if "This service is currently not working" in final_decoded:
        log.error("Service stopped working!")
        return False
    
    if "Please try again later or" in final_decoded:
        log.error("Service unavailable")
        return False
    
    if "Please try again later. Server too busy" in final_decoded:
        log.error("Server too busy")
        return False
    
    if "An error occurred. Please try again" in final_decoded:
        log.error("Error occurred during boost")
        return False
    
    if "Too many requests. Please slow down" in final_decoded:
        log.error("Rate limited!")
        return False

    InvalidUrl = re.search(r'<button[^>]*>\s*<i[^>]*></i>\s*([\d,]+)?\s*</button>', final_decoded, re.IGNORECASE)
    if not InvalidUrl or (InvalidUrl and not InvalidUrl.group(1)):
        log.error("Invalid video URL!")
        return False

    # Check for success patterns ;)
    Views = re.search(r"Successfully\s+(\d+)\s+views sent\.", final_decoded)
    Hearts = re.search(r"(\d+\+?)\s+Hearts successfully sent\.", final_decoded)
    Shares = re.search(r"(\d+)\s+Shares successfully sent\.", final_decoded, re.IGNORECASE)
    Favorites = re.search(r"(\d+)\s+Favorites successfully sent\.", final_decoded, re.IGNORECASE)

    success_match = Views or Hearts or Shares or Favorites
    
    if success_match:
        amount = success_match.group(1)
        log.success(f"Boost successful! +{amount} {service_key}")
        return True
    else:
        log.error("Boost failed - unexpected response")
        print(f"Response preview: {final_decoded[:500]}")
        return False

if __name__ == "__main__":
    login_html = Login()
    video_form = re.search(r'name=["\'](.*?)["\'].*?placeholder=["\']Enter Video URL', login_html).group(1)

    services_status = check_available_services(login_html)
    selected_service = select_service(services_status)

    video_url = log.input("Enter TikTok Video URL: ")
    if not video_url:
        log.error("No URL")
        sys.exit()

    try:
        boost_count = int(log.input(f"How many times to boost {selected_service}? (0 for infinite): "))
    except:
        boost_count = 1

    i = 0
    while True:
        i += 1
        log.info(f"Boost #{i} → {selected_service.upper()}")
        Boost(video_form, selected_service, video_url)

        if boost_count and i >= boost_count:
            log.success(f"Finished {boost_count} boosts!")
            break

        wait = random.uniform(100, 170)
        log.info(f"Waiting {int(wait)}s before next boost...")
        time.sleep(wait)
