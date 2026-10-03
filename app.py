import requests

# API Key الخاص بك
ZAPI_KEY = "Zpi_8a7yqmgdtfnfspwcm81alss1nk"

# رابط الخدمة الخاصة بتيك توك في ZAPI (مثال لجلب بيانات فيديو)
# يمكنك مراجعة لوحة تحكم ZAPI للوصول للمسار الدقيق (Endpoint) الخاص بتيك توك
endpoint_url = "https://zapi.ink/api/tiktok/video"

# البيانات أو الرابط المراد سحبه
params = {
    "api": ZAPI_KEY,
    "url": "https://www.tiktok.com/@username/video/123456789"
}

response = requests.get(endpoint_url, params=params)

if response.status_code == 200:
    data = response.json()
    print("بيانات تيك توك:", data)
else:
    print("حدث خطأ:", response.status_code, response.text)
