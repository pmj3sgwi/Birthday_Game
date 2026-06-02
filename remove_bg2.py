from rembg import remove
from PIL import Image

# 1. 指定你的原始圖片路徑
input_path = r'C:\Users\YACHI\Documents\Antigravity\Game\picture\BB.png'
output_path = r'C:\Users\YACHI\Documents\Antigravity\Game\picture\BB_去背2.png'

print("正在努力去背中，請稍候...")

try:
    # 2. 讀取原始圖片，並確保轉換為帶有透明通道的 RGBA 模式
    original_image = Image.open(input_path).convert("RGBA")
    
    # 3. 使用 rembg 取得去背後的結果（此時畫質可能被壓縮）
    # post_process_mask=True 可以幫助平滑邊緣的雜訊
    rembg_result = remove(original_image, post_process_mask=True)
    
    # 4. 從 rembg 的結果中「單獨抽出」透明度通道（Alpha 遮罩）
    # split()[3] 代表 RGBA 中的 A (Alpha)
    mask = rembg_result.split()[3]
    
    # 確保遮罩大小與原始圖片完全一致
    mask = mask.resize(original_image.size, Image.Resampling.LANCZOS)
    
    # 5. 複製一張原圖，並把剛剛算出的高解析度遮罩「貼」上去
    final_image = original_image.copy()
    final_image.putalpha(mask)
    
    # 6. 存檔
    final_image.save(output_path)
    print(f"🎉 去背成功！原始畫質已保留並存為: {output_path}")

except Exception as e:
    print(f"發生錯誤: {e}")