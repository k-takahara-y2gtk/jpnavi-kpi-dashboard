"""
返す値：
会員の登録状況に関するKPIの集計：
・WordPress総登録者数
    ・詳細情報入力済み人数（name, email, group が全て入力されている）
    ・LINE連携済み人数（WordPress側で sll_lineid が存在する）
    ・グループ別登録人数
    ・role別登録人数
・LINE総登録者数

使い方はこう：
from member_metrics import get_member_metrics
metrics = get_member_metrics()
print(metrics)
"""

import sys
import os

# プロジェクトのルートディレクトリを PYTHONPATH に追加（data/ から実行する場合）
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from api.wp_members import fetch_wp_members_data
from api.line import fetch_line_user_ids

def get_member_metrics() -> dict:
    """
    会員登録状況のKPIを計算して辞書形式で返す関数。

    返す値：
        {
            "wp_total": int,           # WordPress総登録者数
            "wp_detail_count": int,    # 詳細情報入力済み人数（name, email, group が全て入力されている）
            "wp_line_linked": int,     # LINE連携済み人数（WordPress側で sll_lineid が存在する）
            "group_counts": dict,      # グループ別登録人数（group 列でカウント）
            "role_counts": dict,       # role 別登録人数（role 列でカウント）
            "line_total": int          # LINE総登録者数（LINE APIから取得した友だち数）
        }
    """
    # --- WordPress のメンバー情報取得 ---
    df_wp = fetch_wp_members_data()
    # カラム名を確認
    print("利用可能なカラム:", list(df_wp.columns))
    
    wp_total = len(df_wp)
    
    # 詳細情報入力済み：カラムの存在を確認してから処理
    detail_columns = ["display_name", "user_email", "group"] 
    # 存在するカラムだけをsubsetに指定
    available_detail_columns = [col for col in detail_columns if col in df_wp.columns]
    
    if available_detail_columns:
        wp_detail_count = df_wp.dropna(subset=available_detail_columns).shape[0]
    else:
        wp_detail_count = 0
        print("警告: 詳細情報のカラムが見つかりません")
    
    # LINE連携済み：sll_lineid が存在するユーザー数
    wp_line_linked = df_wp["sll_lineid"].notna().sum() if "sll_lineid" in df_wp.columns else 0
    
    # グループ別登録人数：group 列でカウント
    group_counts = df_wp.groupby("group").size().to_dict() if "group" in df_wp.columns else {}
    
    # role 別登録人数：role 列でカウント
    role_counts = df_wp.groupby("role").size().to_dict() if "role" in df_wp.columns else {}

    # --- LINE のユーザー情報取得 ---
    line_ids = fetch_line_user_ids(limit=1000)
    line_total = len(line_ids)

    return {
        "wp_total": wp_total,
        "wp_detail_count": wp_detail_count,
        "wp_line_linked": wp_line_linked,
        "group_counts": group_counts,
        "role_counts": role_counts,
        "line_total": line_total
    }

if __name__ == "__main__":
    metrics = get_member_metrics()
    print("【会員登録状況 KPI】")
    print("WordPress総登録者数:", metrics["wp_total"])
    print("詳細情報入力済み人数:", metrics["wp_detail_count"])
    print("LINE連携済み人数:", metrics["wp_line_linked"])
    print("グループ別登録人数:")
    for group, count in metrics["group_counts"].items():
        print(f"  {group}: {count}")
    print("role別登録人数:")
    for role, count in metrics["role_counts"].items():
        print(f"  {role}: {count}")
    print("LINE総登録者数:", metrics["line_total"])
