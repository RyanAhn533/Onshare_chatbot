from PIL import Image
from pathlib import Path

# 리사이즈 대상 폴더들
folders = [
    r"C:\chat_bot_aac_final\data\hand",
    r"C:\chat_bot_aac_final\data\ingredients",
    r"C:\chat_bot_aac_final\data\menu",
    r"C:\chat_bot_aac_final\data\tools",
]

# 저장 크기
target_size = (256, 256)

for folder in folders:
    path = Path(folder)
    if not path.exists():
        print(f"폴더 없음: {folder}")
        continue

    for img_file in path.glob("*"):
        if img_file.suffix.lower() not in [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"]:
            continue
        try:
            img = Image.open(img_file).convert("RGBA")  # 투명 배경 유지
            img_resized = img.resize(target_size, Image.LANCZOS)
            img_resized.save(img_file)  # 원본 덮어쓰기
            print(f"[OK] {img_file} → {target_size}")
        except Exception as e:
            print(f"[ERROR] {img_file}: {e}")

print("✅ 모든 이미지 리사이즈 완료")
