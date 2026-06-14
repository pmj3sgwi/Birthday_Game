import os
from rembg import remove, new_session
from PIL import Image

# 1. 設定你的「待處理」與「已完成」資料夾路徑
# 建議在 picture 資料夾下新建這兩個資料夾，把要處理的圖全丟進 input_folder
input_folder = r'C:\Users\YACHI\Documents\Antigravity\Game\picture\未去背'
output_folder = r'C:\Users\YACHI\Documents\Antigravity\Game\picture\已去背'

# 如果輸出資料夾不存在，程式會自動幫你建立
os.makedirs(output_folder, exist_ok=True)

print("正在喚醒 AI 模型進入記憶體，請稍候 (只需等待這一次)...")

# 2. 【核心關鍵】建立獨立的 Session，讓 AI 模型只載入一次！
session = new_session("u2net")

# 3. 掃描資料夾內所有的檔案
valid_extensions = ('.png', '.jpg', '.jpeg')
files_to_process = [f for f in os.listdir(input_folder) if f.lower().endswith(valid_extensions)]

if not files_to_process:
    print(f"⚠️ 在 {input_folder} 中沒有找到圖片喔！")
else:
    print(f"📦 找到 {len(files_to_process)} 張圖片，準備開始高速去背！")
    print("-" * 30)

    # 4. 開始自動批次處理
    for filename in files_to_process:
        input_path = os.path.join(input_folder, filename)
        
        # 自動產生新檔名 (例如: BB_T.png -> BB_T_去背.png)
        name, ext = os.path.splitext(filename)
        output_path = os.path.join(output_folder, f"{name}_去背.png")
        
        print(f"🔄 處理中: {filename} ...", end=" ")
        
        try:
            # 讀取並去背，記得傳入我們剛剛建立的 session
            original_image = Image.open(input_path).convert("RGBA")
            rembg_result = remove(original_image, session=session, post_process_mask=True)
            
            # 抽出高解析度遮罩，貼回原圖 (保留像素遊戲畫質)
            mask = rembg_result.split()[3]
            mask = mask.resize(original_image.size, Image.Resampling.LANCZOS)
            
            final_image = original_image.copy()
            final_image.putalpha(mask)
            final_image.save(output_path)
            
            print("✅ 成功！")
            
        except Exception as e:
            print(f"❌ 發生錯誤: {e}")

    print("-" * 30)
    print("🎉 全部圖片去背完成！可以收工啦！")