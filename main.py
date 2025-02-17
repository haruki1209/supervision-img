import tkinter as tk
from transformers import BertModel, BertJapaneseTokenizer
import torch
from tkinter import ttk  # Combobox用

class TemplateGenerator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("監修用画像テンプレート生成")
        self.root.geometry("800x1000")
        
        # メインフレーム
        self.template_frame = tk.Frame(self.root, relief='solid', borderwidth=1)
        self.template_frame.pack(padx=20, pady=20, fill='both', expand=True)
        
        # 固定の会社名を表示
        self.company_label = tk.Label(self.template_frame, text="株式会社arma bianca")
        self.company_label.place(x=10, y=10)
        
        # プレビュー用のラベルを初期化
        self.preview_frame = tk.Frame(self.root, relief='solid', borderwidth=1)
        self.preview_frame.pack(padx=20, pady=5, fill='x')

        # 円の数を入力するためのボックス
        self.create_circle_input()

        # 権利表記の種類選択
        self.create_rights_selection()
        
        # 商品表示オプションのチェックボックス
        self.create_display_options()
        
        # 全ての入力フィールド
        self.create_input_fields()
        
        # プレビューと保存ボタン
        self.create_buttons()

        # 円の数を保持する変数
        self.circle_count = 0

    def create_circle_input(self):
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="円の数 (1-10):").pack(side='left', padx=5)
        self.circle_count_var = tk.StringVar()
        self.circle_count_entry = tk.Entry(input_frame, textvariable=self.circle_count_var, width=5)
        self.circle_count_entry.pack(side='left', padx=5)

    def create_rights_selection(self):
        rights_frame = tk.LabelFrame(self.root, text="権利表記の種類")
        rights_frame.pack(padx=20, pady=5, fill='x')
        
        # ラジオボタンで権利表記の種類を選択
        self.rights_type = tk.StringVar(value="copyright")
        tk.Radiobutton(rights_frame, 
                      text="コピーライト", 
                      variable=self.rights_type, 
                      value="copyright").pack(side='left', padx=10)
        tk.Radiobutton(rights_frame, 
                      text="権利表記 確認用", 
                      variable=self.rights_type, 
                      value="rights").pack(side='left', padx=10)

    def create_display_options(self):
        options_frame = tk.LabelFrame(self.root, text="商品表示オプション")
        options_frame.pack(padx=20, pady=5, fill='x')
        
        # チェックボックス用の変数
        self.single_item_var = tk.BooleanVar()
        self.bonus1_var = tk.BooleanVar()
        self.bonus2_var = tk.BooleanVar()
        
        # チェックボックスの作成
        tk.Checkbutton(options_frame, 
                      text="単品売り", 
                      variable=self.single_item_var,
                      command=self.update_preview).pack(side='left', padx=10)
        
        tk.Checkbutton(options_frame, 
                      text="全○種+特典1種", 
                      variable=self.bonus1_var,
                      command=self.update_preview).pack(side='left', padx=10)
        
        tk.Checkbutton(options_frame, 
                      text="全○種+特典2種", 
                      variable=self.bonus2_var,
                      command=self.update_preview).pack(side='left', padx=10)

    def update_preview(self):
        # すべてのラベルを非表示にする
        for label in self.preview_labels.values():
            label.pack_forget()
        
        # チェックされた項目を表示する
        if self.single_item_var.get():
            self.preview_labels['single'].pack(side='left', padx=10)
        if self.bonus1_var.get():
            self.preview_labels['bonus1'].pack(side='left', padx=10)
        if self.bonus2_var.get():
            self.preview_labels['bonus2'].pack(side='left', padx=10)

    def create_input_fields(self):
        fields = [
            ("作品名:", "work_name"),
            ("商品名:", "product_name"),
            ("権利表記:", "rights_text"),
            ("使用素材:", "materials"),
            ("サイズ:", "size"),
            ("BOX購入特典:", "box_bonus"),
        ]
        
        self.entries = {}
        input_frame = tk.Frame(self.root)
        input_frame.pack(padx=20, pady=10)
        
        # 2列レイアウトで入力フィールドを配置
        for i, (label, field_name) in enumerate(fields):
            row = i // 2
            col = (i % 2) * 2
            
            tk.Label(input_frame, text=label).grid(row=row, column=col, sticky='e', padx=5, pady=2)
            self.entries[field_name] = tk.Entry(input_frame, width=40)
            self.entries[field_name].grid(row=row, column=col+1, sticky='w', padx=5, pady=2)

    def create_buttons(self):
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        preview_button = tk.Button(button_frame, text="プレビュー生成", command=self.generate_preview)
        preview_button.pack(side='left', padx=5)
        
        save_button = tk.Button(button_frame, text="テンプレート保存", command=self.save_template)
        save_button.pack(side='left', padx=5)

    def generate_preview(self):
        preview = tk.Toplevel(self.root)
        preview.title("テンプレートプレビュー")
        preview.geometry("800x600")
        
        main_frame = tk.Frame(preview, relief='solid', borderwidth=1)
        main_frame.pack(padx=20, pady=20, fill='both', expand=True)
        
        # 固定の会社名
        company_label = tk.Label(main_frame, text="株式会社arma bianca")
        company_label.place(x=10, y=10)
        
        # 作品名と商品名のフレーム
        title_frame = tk.Frame(main_frame, relief='solid', borderwidth=1)
        title_frame.place(x=10, y=40)
        
        # 作品名と商品名を横に配置
        work_label = tk.Label(title_frame, text=f'作品名: {self.entries["work_name"].get()}')
        work_label.pack(side='left', padx=5, pady=2)
        
        separator = tk.Label(title_frame, text="|")
        separator.pack(side='left', padx=2)
        
        product_label = tk.Label(title_frame, text=f'商品名: {self.entries["product_name"].get()}')
        product_label.pack(side='left', padx=5)
        
        # 円を描画
        self.draw_circles_in_preview(main_frame)

        # 権利表記の種類に応じて表示位置を変更
        rights_text = self.entries["rights_text"].get()
        materials_text = self.entries["materials"].get()
        size_text = self.entries["size"].get()

        info_frame_top = tk.Frame(main_frame)
        info_frame_top.place(x=10, y=120)
        
        tk.Label(info_frame_top, text=f'■権利表記: {rights_text}').pack(side='left', padx=(0,20))
        tk.Label(info_frame_top, text=f'■使用素材: {materials_text}').pack(side='left')
        tk.Label(info_frame_top, text=f'■サイズ:(約){size_text}').pack(side='left')

        # BOX購入特典をより下に配置
        if self.entries["box_bonus"].get():
            bonus_y = 400  # y座標を400に変更
            tk.Label(main_frame, text="【BOX購入特典】", fg='#FF69B4').place(x=10, y=bonus_y)
            tk.Label(main_frame, text=self.entries["box_bonus"].get()).place(x=10, y=bonus_y+25)

    def draw_circles_in_preview(self, main_frame):
        # 円の数を取得
        try:
            self.circle_count = int(self.circle_count_var.get())
        except ValueError:
            self.circle_count = 0

        # 円のパラメータ
        radius = 30
        spacing = 20
        max_columns = 5  # 最大列数
        max_rows = 2     # 最大行数
        canvas_width = (radius * 2 + spacing) * max_columns  # キャンバスの幅
        canvas_height = (radius * 2 + spacing) * max_rows    # キャンバスの高さ

        # プレビュー用のキャンバスを作成
        canvas = tk.Canvas(main_frame, width=canvas_width, height=canvas_height)
        canvas.place(x=10, y=200)

        # 円を描画
        for i in range(min(self.circle_count, max_columns * max_rows)):
            x0 = (radius * 2 + spacing) * (i % max_columns) + spacing // 2
            y0 = (radius * 2 + spacing) * (i // max_columns) + spacing // 2
            x1 = x0 + radius * 2
            y1 = y0 + radius * 2
            canvas.create_oval(x0, y0, x1, y1, outline="black", fill="white")

    def save_template(self):
        # テンプレート保存機能（今後実装）
        pass

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = TemplateGenerator()
    app.run()