import tkinter as tk

def generate_layout():
    # ユーザー入力を取得
    product_name = product_name_entry.get()
    date = date_entry.get()
    
    # プレビューウィンドウを作成してレイアウトを表示
    preview_window = tk.Toplevel(root)
    preview_window.title("自動レイアウト生成プレビュー")
    
    # 商品名を指定した位置に配置
    tk.Label(preview_window, text=f"商品名: {product_name}", font=("Arial", 20)).place(x=100, y=100)
    # 日付を指定した位置に配置
    tk.Label(preview_window, text=f"日付: {date}", font=("Arial", 15)).place(x=100, y=150)

# メインウィンドウを作成
root = tk.Tk()
root.title("監修用画像生成")

# フォーマット形式として表示
tk.Label(root, text="入力フォーマット").pack()

# 商品名入力フォーム
tk.Label(root, text="商品名").pack()
product_name_entry = tk.Entry(root)
product_name_entry.pack()

# 日付入力フォーム
tk.Label(root, text="日付").pack()
date_entry = tk.Entry(root)
date_entry.pack()

# レイアウト生成ボタン
generate_button = tk.Button(root, text="完了", command=generate_layout)
generate_button.pack()

root.mainloop()
