"""
使い方はこう：

from line_users import fetch_line_user_ids, build_line_users_df

# 友だち登録しているLINEユーザーのID一覧を取得
user_ids = fetch_line_user_ids(limit=1000)

# 各ユーザーのプロフィール情報を取得し、DataFrame化
df_users = build_line_users_df(user_ids)

"""

import requests
import pandas as pd
import os
from dotenv import load_dotenv
from tqdm import tqdm

def fetch_line_user_ids(limit=1000):
    """
    LINE APIから友だち登録者の userId を取得（最大1000件）
    """
    load_dotenv()
    ACCESS_TOKEN = os.getenv("LINE_ACCESS_TOKEN")
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

    url = "https://api.line.me/v2/bot/followers/ids"
    params = {"limit": limit}
    res = requests.get(url, headers=headers, params=params)

    if res.status_code != 200:
        raise RuntimeError(f"LINE APIエラー: {res.status_code}\n{res.text}")

    data = res.json()
    return data.get("userIds", [])

def build_line_users_df(user_ids):
    """
    ユーザーIDのリストからプロフィールを取得し、DataFrameを構築
    """
    ACCESS_TOKEN = os.getenv("LINE_ACCESS_TOKEN")
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

    profiles = []
    for uid in tqdm(user_ids, desc="Fetching profiles", unit="user"):
        url = f"https://api.line.me/v2/bot/profile/{uid}"
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            profiles.append(res.json())
        else:
            profiles.append({"userId": uid, "error": res.status_code})

    return pd.DataFrame(profiles)

# デバッグ用
if __name__ == "__main__":
    try:
        user_ids = fetch_line_user_ids()
        print(f"✅ 登録者数: {len(user_ids)}")
        df = build_line_users_df(user_ids)  # サンプル5件だけ
        print(df.head())
    except Exception as e:
        print("❌ エラー:", e)
