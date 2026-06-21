import numpy as np
from scipy.ndimage import label
from PIL import Image
from collections import Counter

# 1. 指定你的原始圖片路徑 (就是那張有灰白格子的圖)
input_path = r'C:\Users\YACHI\Documents\Antigravity\Game\picture\鑰匙.png'

# 2. 指定去背後的新檔案名稱
output_path = r'C:\Users\YACHI\Documents\Antigravity\Game\picture\鑰匙_去背.png'

# 與背景色的歐式距離門檻：低於此值視為背景。
# 太大會連同畫面內較深/較淺的陰影一起去除，太小則背景邊緣會留下殘留色。
THRESHOLD = 16

print("正在努力去背中，請稍候...")

# 3. 執行去背並存檔
try:
    input_image = Image.open(input_path).convert('RGBA')
    arr = np.array(input_image)

    rgb = arr[:, :, :3].astype(np.int32)

    # 自動取畫面四邊邊框中最常出現的顏色當作背景色，黑色、白色背景都適用。
    # 用「最常出現」而非單純 4 個角落像素，是為了避免角落剛好疊到裝飾物（例如小圖示）時誤判背景色。
    border_pixels = np.concatenate([rgb[0, :], rgb[-1, :], rgb[:, 0], rgb[:, -1]])
    mode_color = Counter(map(tuple, border_pixels)).most_common(1)[0][0]
    bg_color = np.array(mode_color)

    dist_from_bg = np.sqrt(((rgb - bg_color) ** 2).sum(axis=2))
    bg_like = dist_from_bg < THRESHOLD

    # 只去除「與畫面邊緣相連」的背景色區域，避免誤刪畫面內部本來就接近背景色的陰影
    labeled, _ = label(bg_like)
    border_labels = set(labeled[0, :]) | set(labeled[-1, :]) | set(labeled[:, 0]) | set(labeled[:, -1])
    border_labels.discard(0)
    bg_mask = np.isin(labeled, list(border_labels))

    arr[:, :, 3] = np.where(bg_mask, 0, arr[:, :, 3])
    output_image = Image.fromarray(arr, 'RGBA')
    output_image.save(output_path)
    print(f"🎉 去背成功！真正的透明圖已存為: {output_path}")
except Exception as e:
    print(f"發生錯誤: {e}")