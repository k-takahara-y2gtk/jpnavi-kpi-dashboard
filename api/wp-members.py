"""
使い方はこう：
from wp_members import fetch_wp_members_data
# WordPress メンバー情報を取得して DataFrame 形式で扱う
df_members = fetch_wp_members_data()
"""

import requests
from dotenv import load_dotenv
import os
import pandas as pd

# --- API 呼び出しと整形処理 ---
def fetch_wp_members_data() -> pd.DataFrame:
    # .env 読み込み
    load_dotenv()

    API_URL = os.getenv("WP_API_URL") # .env必要です
    API_KEY = os.getenv("WP_API_KEY") # .env必要です

    headers = {"X-API-KEY": API_KEY}
    response = requests.get(API_URL, headers=headers)

    if response.status_code != 200:
        raise RuntimeError(f"API取得に失敗しました（status: {response.status_code}）\n{response.text}")

    data = response.json()

    # --- ユーザー詳細データをDataFrameに変換 ---
    users = data.get("user_detail_list", [])
    df_users = pd.DataFrame(users)

    # --- 権限とグループを個別列で持たせる（roles[0] 展開） ---
    if "roles" in df_users.columns:
        df_users["role"] = df_users["roles"].apply(lambda x: x[0] if isinstance(x, list) and len(x) > 0 else None)

    # 必要なら他の整形処理もここで追加
    return df_users


# --- デバッグ用：直接実行時のみ走る ---
if __name__ == "__main__":
    try:
        df = fetch_wp_members_data()
        print("✅ データ取得 & 整形完了！")
        print(df.head())
    except Exception as e:
        print("❌ エラー:", e)
