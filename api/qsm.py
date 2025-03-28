"""

使い方はこう：
from qsm_metadata import get_all_quiz_metadata
# クイズのメタデータを取得（例: 上限1000件）
df_quizzes = get_all_quiz_metadata(limit=1000)

"""

import requests
import os
from dotenv import load_dotenv
import json
import pandas as pd

load_dotenv()

BASE_URL = os.getenv("QSM_API_URL")  # 例: https://www.jpnnavi.com/wp-json/qsm
API_KEY = os.getenv("QSM_API_KEY")
if not API_KEY:
    raise ValueError("QSM_API_KEY is not set in the environment variables.")
API_KEY = API_KEY.strip()

def debug_print_request(response):
    req = response.request
    print("----- REQUEST INFO -----")
    print("URL:", req.url)
    print("Method:", req.method)
    print("Headers:", req.headers)
    if req.body:
        print("Body:", req.body)
    print("------------------------")
    print("📦 レスポンスコード:", response.status_code)
    try:
        resp_json = response.json()
        print("📦 レスポンスボディ (JSON):", json.dumps(resp_json, indent=2, ensure_ascii=False))
    except Exception as e:
        print("📦 レスポンスボディ (raw):", response.text)
    print("================================\n")

def get_all_quiz_metadata(limit=1000):
    """
    QSM API の /quiz エンドポイントから、すべてのクイズのメタデータを取得し、
    削除されていないクイズ（deleted==0）のみ DataFrame として返す。
    """
    url = f"{BASE_URL}/quiz"
    headers = {
        "authorization": API_KEY,  # プレーンテキストのAPIキー
        "Content-Type": "application/json"
    }
    params = {
        "limit": limit
    }
    
    print("----- get_all_quiz_metadata -----")
    print("URL:", url)
    print("Headers:", headers)
    print("Params:", params)
    
    response = requests.get(url, headers=headers, params=params)
    debug_print_request(response)
    
    if response.status_code == 200:
        data = response.json()
        if data.get("success") == True:
            # 取得可能な項目をできるだけ多く抽出
            quiz_list = [
                {
                    "quizId": q.get("quizId"),
                    "quiz_name": q.get("quiz_name"),
                    "last_activity": q.get("last_activity"),
                    "quiz_views": q.get("quiz_views"),
                    "quiz_taken": q.get("quiz_taken"),
                    "deleted": q.get("deleted"),
                    "require_log_in": q.get("require_log_in"),
                    "theme_selected": q.get("theme_selected"),
                    "quiz_author_id": q.get("quiz_author_id"),
                    "pagination": q.get("pagination"),
                    "timer_limit": q.get("timer_limit"),
                    "message_before": q.get("message_before"),
                    "message_after": q.get("message_after")
                }
                for q in data.get("data", [])
            ]
            df = pd.DataFrame(quiz_list)
            # 削除されているクイズ（deleted != 0）を除外する
            df = df[df["deleted"] == 0]
            return df
        else:
            print("❌ APIレスポンスが success: false です。")
            return pd.DataFrame()
    else:
        print(f"❌ クイズ一覧取得失敗: {response.status_code}")
        return pd.DataFrame()

if __name__ == "__main__":
    df_quizzes = get_all_quiz_metadata(limit=1000)
    print("✅ クイズのメタデータ取得結果:")
    print(df_quizzes.head())
    print("\n--- DataFrame Columns ---")
    print(df_quizzes.columns.tolist())
