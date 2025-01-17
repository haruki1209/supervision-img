import tkinter as tk

def update_canvas(event):
    # 選択されたテンプレートを取得
    selected_index = listbox.curselection()
    if selected_index:
        selected_text = listbox.get(selected_index)
        # キャンバスをクリア
        canvas.delete("all")
        # テキストをキャンバスの中央に配置
        canvas.create_text(canvas_width / 2, canvas_height / 2, text=selected_text, font=("Helvetica", 16, "bold"))

def create_window():
    global listbox, canvas, canvas_width, canvas_height

    # ウィンドウの作成
    window = tk.Tk()
    window.title("テンプレート選択と表示")

    # ウィンドウのサイズを設定
    window.geometry("600x300")

    # フレームの作成
    frame = tk.Frame(window)
    frame.pack(fill=tk.BOTH, expand=True)

    # リストボックスの作成
    listbox = tk.Listbox(frame)
    listbox.pack(side=tk.LEFT, fill=tk.Y)

    # テンプレートの追加
    templates = ["株式会社arma bianca", "テンプレート1", "テンプレート2", "テンプレート3"]
    for template in templates:
        listbox.insert(tk.END, template)

    # キャンバスの作成
    canvas = tk.Canvas(frame, width=400, height=300)
    canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # キャンバスの幅と高さを取得
    canvas_width = 400
    canvas_height = 300

    # リストボックスの選択イベントにバインド
    listbox.bind("<<ListboxSelect>>", update_canvas)

    # ウィンドウの表示
    window.mainloop()

if __name__ == "__main__":
    create_window() 