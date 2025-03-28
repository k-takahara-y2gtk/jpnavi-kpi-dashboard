# 実装記録
## まず、各データソースのAPI連携をローカルで検証
https://chatgpt.com/c/67e4a7bb-1f44-800d-9b66-0a9c894cc5c5?model=gpt-4o
・WordPress
→


### データ取得モジュール
- **excel.py**  
  SharePoint 上にある契約状況 Excel ファイルを取得し、複数シートを pandas の DataFrame で扱えるようにする。
- **line.py**  
  LINE公式アカウントと連携し、友だちユーザーのID一覧およびプロフィール情報を取得して DataFrame 化する。
- **qsm.py**  
  QSM（クイズ管理）APIを用いて、クイズ一覧とそのメタ情報（閲覧数・回答数など）を取得する。
- **wp-members.py**  
  WordPress の REST API を通じて、ユーザーアカウント情報を取得し、DataFrame として整形する。