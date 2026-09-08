from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import re

app = FastAPI()

ZENROWS_API_KEY = '17876db80843f219a6ae0e17c20cbf66b7097109'

class LinkRequest(BaseModel):
    url: str

@app.post("/key/links")
def get_key_from_link(data: LinkRequest):
    params = {
        'url': data.url,
        'apikey': ZENROWS_API_KEY,
        'js_render': 'true',
        'premium_proxy': 'true',
    }
    
    try:
        response = requests.get('https://api.zenrows.com/v1/', params=params, timeout=25)
        
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="فشل الاتصال بالرابط")

        html_content = response.text
        key_match = re.search(r'[a-zA-Z0-9_-]{32,64}', html_content)
        
        if key_match:
            return {"status": "success", "key": key_match.group(0)}
        else:
            return {"status": "success", "raw_html": html_content}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
