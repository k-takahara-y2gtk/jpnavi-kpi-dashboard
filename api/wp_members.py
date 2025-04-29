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

def fetch_wp_members_data() -> pd.DataFrame:
    load_dotenv()
    API_URL = os.getenv("WP_API_URL")
    API_KEY = os.getenv("WP_API_KEY")
    headers = {"X-API-KEY": API_KEY}

    all_users = []
    offset = 0
    limit = 5000

    while True:
        params = {"limit": limit, "offset": offset}
        response = requests.get(API_URL, headers=headers, params=params)
        if response.status_code != 200:
            raise RuntimeError(f"API取得に失敗しました（status: {response.status_code}）\n{response.text}")

        data = response.json()
        users = data.get("user_detail_list", [])
        if not users:
            break  # データが無くなったら終了

        all_users.extend(users)
        offset += limit  # 次のオフセットへ進む

    df_users = pd.DataFrame(all_users)

    if "roles" in df_users.columns:
        df_users["role"] = df_users["roles"].apply(lambda x: x[0] if isinstance(x, list) and len(x) > 0 else None)

    return df_users


# --- デバッグ用：直接実行時のみ走る ---
if __name__ == "__main__":
    try:
        df = fetch_wp_members_data()
        print("✅ データ取得 & 整形完了！")
        print(df.head())
    except Exception as e:
        print("❌ エラー:", e)
