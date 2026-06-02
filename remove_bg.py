from rembg import remove
from PIL import Image

# 1. 指定你的原始圖片路徑 (就是那張有灰白格子的圖)
input_path = r'C:\Users\YACHI\Documents\Antigravity\Game\picture\鏡子_微霧.png'

# 2. 指定去背後的新檔案名稱
output_path = r'C:\Users\YACHI\Documents\Antigravity\Game\picture\鏡子_微霧_去背.png'

print("正在努力去背中，請稍候...")

# 3. 執行去背並存檔
try:
    input_image = Image.open(input_path)
    output_image = remove(input_image)
    output_image.save(output_path)
    print(f"🎉 去背成功！真正的透明圖已存為: {output_path}")
except Exception as e:
    print(f"發生錯誤: {e}")