import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from api.excel import fetch_contracts_sheets

# SharePoint 上の契約状況 Excel ファイルを全シート取得
dfs = fetch_contracts_sheets()

# シートごとの DataFrame を取得
df_sheet1 = dfs['営業・導入状況シート']
df_sheet2 = dfs['ぐるーぷID管理シート']

# CSV ファイルとして保存
df_sheet1.to_csv("contracts_status_sheet.csv", index=False)
df_sheet2.to_csv("group_id_management_sheet.csv", index=False)

print("✅ CSVファイルに書き出しました！")
