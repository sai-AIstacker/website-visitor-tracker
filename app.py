from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from datetime import datetime
from user_agents import parse
import os
import json
import requests
import gspread
from google.oauth2.service_account import Credentials


app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GOOGLE SHEET SETUP 

# Load credentials from Render environment variable
creds_json = os.environ.get("GOOGLE_CREDS_JSON")
creds_dict = json.loads(creds_json)

scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

creds = Credentials.from_service_account_file(
    "visitor-tracker-api-053b3524faf8.json",
    scopes=scope
)

client = gspread.authorize(creds)

# Google Sheet Name (Make sure same name exists in your Google Drive)
SHEET_NAME = "VisitorTrackerData"
sheet = client.open(SHEET_NAME).sheet1

def get_location_info(ip):
    """Get location data from IP."""
    try:
        if ip in ['127.0.0.1', 'localhost', '::1']:
            return {'country': 'Local', 'city': 'Local', 'region': 'Local'}

        res = requests.get(f'http://ip-api.com/json/{ip}', timeout=3).json()
        if res.get('status') == 'success':
            return {
                'country': res.get('country', 'Unknown'),
                'city': res.get('city', 'Unknown'),
                'region': res.get('regionName', 'Unknown')
            }
    except:
        pass

    return {'country': 'Unknown', 'city': 'Unknown', 'region': 'Unknown'}

# Serve Frontend Files (Your HTML/CSS/JS)
app.mount("/", StaticFiles(directory="website", html=True), name="website")

@app.post("/track")
async def track_visitor(request: Request):
    try:
        # IP extraction
        ip = request.headers.get('X-Forwarded-For', request.client.host).split(',')[0]
        print(f" New visitor from IP: {ip}")

        # Location info
        location = get_location_info(ip)

        # User Agent
        user_agent_string = request.headers.get("User-Agent", "")
        user_agent = parse(user_agent_string)

        data = await request.json()

        row = [
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            ip,
            location['country'],
            location['city'],
            location['region'],
            f"{user_agent.browser.family} {user_agent.browser.version_string}",
            f"{user_agent.os.family} {user_agent.os.version_string}",
            user_agent.device.family,
            data.get('referrer', 'Direct'),
            data.get('page_url', 'Unknown')
        ]

        sheet.append_row(row)

        return JSONResponse({"status": "success", "message": "Visitor logged"})

    except Exception as e:
        print(f" Error: {str(e)}")
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)

@app.get("/stats")
def get_stats():
    try:
        total_visitors = len(sheet.get_all_values()) - 1
        return {"total_visitors": total_visitors}
    except:
        return {"total_visitors": 0}


print("\nFastAPI Visitor Tracker Running with Google Sheets Logging")
