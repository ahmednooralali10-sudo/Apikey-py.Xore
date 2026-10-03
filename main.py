from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
import requests
import urllib.parse

app = FastAPI()

ZAPI_KEY = "Zpi_8a7yqmgdtfnfspwcm81alss1nk"

# 1. واجهة الموقع الأساسية (HTML + CSS + JS)
@app.get("/", response_class=HTMLResponse)
async def home():
    html_content = """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>TikTok Data Extractor</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #121212; color: #fff; text-align: center; padding: 20px; }
            .container { max-width: 600px; margin: 40px auto; background: #1e1e1e; padding: 30px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.5); }
            h2 { color: #fe2c55; margin-bottom: 20px; }
            input { width: 80%; padding: 12px; border-radius: 8px; border: 1px solid #333; background: #2a2a2a; color: #fff; margin-bottom: 15px; text-align: center; font-size: 16px; }
            button { padding: 12px 25px; border-radius: 8px; border: none; background: #fe2c55; color: #fff; font-size: 16px; cursor: pointer; font-weight: bold; }
            button:hover { background: #e02648; }
            #result { margin-top: 25px; text-align: right; background: #2a2a2a; padding: 15px; border-radius: 8px; white-space: pre-wrap; word-break: break-all; max-height: 400px; overflow-y: auto; font-family: monospace; }
            .loading { display: none; color: #ff0; margin-top: 15px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>جلب بيانات تيك توك 🎵</h2>
            <p>أدخل يوزر الحساب أو رابط الفيديو لجلب جميع البيانات:</p>
            <input type="text" id="userInput" placeholder="مثال: username أو رابط الفيديو">
            <br>
            <button onclick="fetchData()">جلب البيانات</button>
            <div id="loading" class="loading">جاري جلب البيانات...</div>
            <div id="result">النتائج ستظهر هنا...</div>
        </div>

        <script>
            async function fetchData() {
                const input = document.getElementById('userInput').value.trim();
                const resultDiv = document.getElementById('result');
                const loadingDiv = document.getElementById('loading');

                if (!input) {
                    alert('الرجاء إدخال اليوزر أو الرابط');
                    return;
                }

                loadingDiv.style.display = 'block';
                resultDiv.innerText = '';

                try {
                    // إذا كان المدخل يوزر فقط يتم تحويله لرابط حساب
                    let targetUrl = input;
                    if (!input.startsWith('http')) {
                        targetUrl = `https://www.tiktok.com/@${input}`;
                    }

                    const response = await fetch(`/api/get-tiktok?url=${encodeURIComponent(targetUrl)}`);
                    const data = await response.json();

                    loadingDiv.style.display = 'none';
                    resultDiv.innerText = JSON.stringify(data, null, 2);
                } catch (error) {
                    loadingDiv.style.display = 'none';
                    resultDiv.innerText = 'حدث خطأ أثناء جلب البيانات: ' + error.message;
                }
            }
        </script>
    </body>
    </html>
    """
    return html_content

# 2. نقطة الـ API لجلب البيانات من ZAPI
@app.get("/api/get-tiktok")
async def get_tiktok(url: str):
    try:
        encoded_url = urllib.parse.quote(url, safe="")
        api_url = f"https://zapi.ink/api/tiktok/video?api={ZAPI_KEY}&url={encoded_url}"
        
        response = requests.get(api_url, timeout=10)
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
