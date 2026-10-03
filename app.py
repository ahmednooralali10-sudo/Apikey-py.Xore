from fastapi import FastAPI, HTTPException, Request
import requests
import urllib.parse

app = FastAPI()

# API Key الخاص بك في zapi.ink
ZAPI_KEY = "Zpi_8a7yqmgdtfnfspwcm81alss1nk"

@app.get("/deltakey")
async def get_delta_key(request: Request):
    full_url = str(request.url)
    
    if "link=" not in full_url:
        raise HTTPException(status_code=400, detail="الرجاء إرفاق الرابط بعد link=")

    # استخراج الرابط المرسل (سواء كان platoboost أو lootlabs)
    target_link = full_url.split("link=", 1)[1]

    try:
        # تشفير الرابط
        encoded_link = urllib.parse.quote(target_link, safe="")
        
        # إرسال الطلب لـ zapi.ink
        api_url = f"https://zapi.ink/api?api={ZAPI_KEY}&url={encoded_link}"
        
        response = requests.get(api_url, timeout=15)
        data = response.json()
        
        return {
            "status": "success",
            "result": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"حدث خطأ أثناء فك الرابط: {str(e)}")
