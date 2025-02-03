import tkinter as tk
from transformers import BertModel, BertTokenizer
import torch

# グローバル変数として入力フィールドを定義
company_name_entry = None
product_title_entry = None
product_name_entry = None
total_types_entry = None
total_types_2_entry = None
size_entry = None
copyright_entry = None
materials_entry = None
box_bonus_entry = None
chara_badge_entry = None
chara_square_badge_entry = None
date_entry = None

class BertLayoutOptimizer:
    def __init__(self):
        self.model_name = "cl-tohoku/bert-base-japanese-whole-word-masking"
        self.tokenizer = BertTokenizer.from_pretrained(self.model_name)
        self.model = BertModel.from_pretrained(self.model_name)
        
        # 重要度の基準値
        self.importance_threshold = 0.6
        self.base_font_size = 12
    
    def analyze_content(self, text):
        # テキストをトークン化
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        
        # BERTモデルで分析
        with torch.no_grad():
            outputs = self.model(**inputs)
        
        # 文章の特徴量を取得
        embeddings = outputs.last_hidden_state.mean(dim=1)
        
        # 重要度スコアの計算
        importance_score = torch.sigmoid(embeddings.mean()).item()
        
        return {
            'importance': importance_score,
            'length': len(text)
        }
    
    def get_layout_params(self, label, content):
        # コンテンツを分析
        analysis = self.analyze_content(content)
        
        # フォントサイズの決定
        font_size = self.base_font_size
        if analysis['importance'] > self.importance_threshold:
            font_size += 2
        if analysis['length'] > 30:
            font_size -= 1
        
        # 強調表示の決定
        emphasis = analysis['importance'] > self.importance_threshold
        
        # 間隔の計算
        spacing = 10 + (analysis['importance'] * 5)
        
        return {
            'font_size': int(font_size),
            'spacing': int(spacing),
            'emphasis': emphasis
        }

def generate_layout():
    layout_optimizer = BertLayoutOptimizer()
    
    # プレビューウィンドウの設定
    preview_window = tk.Toplevel(root)
    preview_window.title("自動レイアウト生成プレビュー")
    preview_window.geometry("800x600")
    
    # 左側のカラム
    left_frame = tk.Frame(preview_window)
    left_frame.pack(side=tk.LEFT, padx=50, pady=20)
    
    # 入力値を取得し、BERTで最適化
    fields_left = [
        ("会社名", company_name_entry.get()),
        ("作品名", product_title_entry.get()),
        ("商品名", product_name_entry.get()),
        ("全種類+特典1種", total_types_entry.get()),
        ("全種類+特典2種", total_types_2_entry.get())
    ]
    
    for label, value in fields_left:
        if value.strip():
            # BERTによるレイアウト最適化
            params = layout_optimizer.get_layout_params(label, value)
            
            # フォント設定
            font = ("Arial", params['font_size'], 
                   "bold" if params['emphasis'] else "normal")
            
            # ラベルの作成
            label_widget = tk.Label(
                left_frame, 
                text=f"{label}: {value}",
                font=font,
                anchor="w"
            )
            label_widget.pack(pady=params['spacing'], fill=tk.X)
    
    # 右側のカラム
    right_frame = tk.Frame(preview_window)
    right_frame.pack(side=tk.LEFT, padx=50, pady=20)
    
    fields_right = [
        ("コピーライト", copyright_entry.get()),
        ("使用素材", materials_entry.get()),
        ("BOX購入特典", box_bonus_entry.get())
    ]
    
    for label, value in fields_right:
        if value.strip():
            params = layout_optimizer.get_layout_params(label, value)
            font = ("Arial", params['font_size'])
            tk.Label(
                right_frame,
                text=f"{label}: {value}",
                font=font,
                anchor="w"
            ).pack(pady=params['spacing'], fill=tk.X)

def create_gui():
    global company_name_entry, product_title_entry, product_name_entry
    global total_types_entry, total_types_2_entry
    global size_entry, copyright_entry, materials_entry, box_bonus_entry
    global chara_badge_entry, chara_square_badge_entry, date_entry
    
    # メインウィンドウの設定
    root = tk.Tk()
    root.title("監修用画像生成")
    root.geometry("600x800")

    # 入力フォームをグリッドレイアウトで整理
    tk.Label(root, text="入力フォーマット", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=20)

    # 2列のグリッドレイアウトで入力フォームを配置
    fields = [
        ("会社名", "company_name_entry"),
        ("作品名", "product_title_entry"),
        ("商品名", "product_name_entry"),
        ("全種類+特典1種", "total_types_entry"),
        ("全種類+特典2種", "total_types_2_entry"),
        ("サイズ:(約)各種〇〇mm", "size_entry"),
        ("コピーライト:", "copyright_entry"),
        ("使用素材:", "materials_entry"),
        ("BOX購入特典\n※内容含む", "box_bonus_entry"),
        ("キャラ名 缶バッジ\nAMNIBUS限定特典", "chara_badge_entry"),
        ("キャラ名 スクエア缶バッジ\nAMNIBUS限定特典", "chara_square_badge_entry")
    ]

    for i, (label_text, entry_name) in enumerate(fields):
        row = (i // 2) + 1
        col = i % 2 * 2
        
        tk.Label(root, text=label_text).grid(row=row, column=col, pady=5, padx=10, sticky="e")
        entry = tk.Entry(root, width=30)
        entry.grid(row=row, column=col+1, pady=5, padx=10, sticky="w")
        globals()[entry_name] = entry

    # 完了ボタン
    generate_button = tk.Button(root, text="完了", command=generate_layout)
    generate_button.grid(row=len(fields)//2 + 2, column=0, columnspan=4, pady=20)

    return root

if __name__ == "__main__":
    root = create_gui()
    root.mainloop()
