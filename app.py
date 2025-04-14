
from flask import Flask, request, render_template
import pandas as pd
import requests
import os
import time

app = Flask(__name__)

NOTION_TOKEN = os.environ.get("NOTION_TOKEN", "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")
DATABASE_ID = "1d555b3f92ba8104a80eda4755e07e54"
NOTION_API_URL = f"https://api.notion.com/v1/pages"
HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def create_notion_page(row):
    properties = {
        "제품모델명": {
            "title": [{"text": {"content": str(row['제품모델명'])}}]
        },
        "모델명": {
            "rich_text": [{"text": {"content": str(row['모델명'])}}]
        },
        "품명": {
            "rich_text": [{"text": {"content": str(row['품명'])}}]
        },
        "규격": {
            "rich_text": [{"text": {"content": str(row['규격'])}}]
        },
        "수량": {
            "rich_text": [{"text": {"content": str(row['수량'])}}]
        },
        "원산지": {
            "rich_text": [{"text": {"content": str(row['원산지'])}}]
        },
        "비고": {
            "rich_text": [{"text": {"content": str(row['비고'])}}]
        }
    }
    return {
        "parent": {"database_id": DATABASE_ID},
        "properties": properties
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_excel_notion', methods=['GET', 'POST'])
def upload_excel_notion():
    if request.method == 'POST':
        file = request.files['file']
        filepath = os.path.join("/mnt/data", file.filename)
        file.save(filepath)

        df = pd.read_excel(filepath, sheet_name='영상감시시스템')
        df = df.fillna("")

        for i, row in df.iterrows():
            payload = create_notion_page(row)
            res = requests.post(NOTION_API_URL, headers=HEADERS, json=payload)
            print("[{}] 응답: {}".format(i, res.text))
            time.sleep(0.5)

        return 'Notion 업로드 완료!'
    return render_template('upload_excel_notion.html')
