"""
使い方はこう：

from contracts_excel import fetch_contracts_sheets

# SharePoint 上の契約状況 Excel ファイルを全シート取得
dfs = fetch_contracts_sheets()

df_sheet1 = dfs['営業・導入状況シート']
df_sheet2 = dfs['ぐるーぷID管理シート']
"""

import os
import json
import io
import pandas as pd
import requests
from msal import ConfidentialClientApplication
from dotenv import load_dotenv


def fetch_contracts_sheets() -> dict:
    """
    SharePoint 上の Excel ファイルから、すべてのシートを取得して辞書形式で返す関数。
    Returns:
        dict: {"シート名": pd.DataFrame, ...}
    """
    # --- .env 読み込み & 認証情報の取得 ---
    load_dotenv(override=True)
    client_id = os.getenv("MS_CLIENT_ID")
    client_secret = os.getenv("MS_CLIENT_SECRET")
    tenant_id = os.getenv("MS_TENANT_ID")
    site_domain = os.getenv("MS_SITE_DOMAIN")
    site_name = os.getenv("MS_SITE_NAME")
    sharepoint_directory = os.getenv("MS_SHAREPOINT_DIRECTORY")
    excel_filename = os.getenv("EXCEL_FILENAME")

    # --- 認証 ---
    authority_url = f"https://login.microsoftonline.com/{tenant_id}"
    scope = ["https://graph.microsoft.com/.default"]
    app = ConfidentialClientApplication(
        client_id=client_id,
        client_credential=client_secret,
        authority=authority_url
    )
    result = app.acquire_token_for_client(scopes=scope)
    if "access_token" not in result:
        raise Exception("アクセストークン取得に失敗しました")
    access_token = result["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    # --- サイト ID 取得 ---
    site_url = f"https://graph.microsoft.com/v1.0/sites/{site_domain}:/sites/{site_name}"
    site_resp = requests.get(site_url, headers=headers)
    site_resp.raise_for_status()
    site_id = site_resp.json()["id"]

    # --- フォルダ ID を再帰的に取得 ---
    def get_folder_id_from_tree(site_id, folder_path_list, folder_id="root"):
        for folder in folder_path_list:
            url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/items/{folder_id}/children"
            resp = requests.get(url, headers=headers)
            resp.raise_for_status()
            items = resp.json().get("value", [])
            match = next((item for item in items if item["name"] == folder), None)
            if not match:
                raise FileNotFoundError(f"フォルダ '{folder}' が見つかりません")
            folder_id = match["id"]
        return folder_id

    # --- フォルダ ID の取得とファイルダウンロード ---
    folder_path_list = sharepoint_directory.strip("/").split("/")
    folder_id = get_folder_id_from_tree(site_id, folder_path_list)
    file_url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/items/{folder_id}:/{excel_filename}:/content"
    file_resp = requests.get(file_url, headers=headers)
    file_resp.raise_for_status()

    # --- Excel バイナリ → 全シートを読み込んで dict で返す ---
    excel_bytes = io.BytesIO(file_resp.content)
    dfs = pd.read_excel(excel_bytes, sheet_name=None)  # 全シート読み込み

    return dfs


# --- 実行用 ---
if __name__ == "__main__":
    dfs = fetch_contracts_sheets()
    print("✅ Excel 全シート取得完了！")
    for sheet_name, df in dfs.items():
        print(f"\n📄 Sheet: {sheet_name}")
        print(df.head())
