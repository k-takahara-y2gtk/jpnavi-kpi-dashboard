import streamlit as st
import sys
import os
import dotenv
print("=== sys.path ===")
print("\n".join(sys.path))
print("dotenv is imported from:", getattr(dotenv, "__file__", "None"))
print("dotenv.load_dotenv:", getattr(dotenv, "load_dotenv", "Not found"))

from dotenv import load_dotenv
load_dotenv()
from integrate.customer import get_member_metrics

def main():
    st.title("KPI確認画面")
    
    # KPI セクション
    st.header("JPNAVI会員")
    metrics = get_member_metrics()
    
    col1, col2 = st.columns(2)
    col1.metric("WordPress総登録者数", metrics["wp_total"])
    col2.metric("LINE総登録者数", metrics["line_total"])
    
    # グループID別登録人数をプルダウン表示
    with st.expander("グループID別登録人数"):
        group_counts = metrics.get("group_counts", {})
        if group_counts:
            for group_id, count in group_counts.items():
                st.write(f"{group_id}: {count}")
        else:
            st.write("グループ情報がありません。")
    
    # 権限(role)別登録人数をプルダウン表示
    with st.expander("権限別登録人数"):
        role_counts = metrics.get("role_counts", {})
        if role_counts:
            for role, count in role_counts.items():
                st.write(f"{role}: {count}")
        else:
            st.write("権限情報がありません。")

if __name__ == "__main__":
    main()