'''from PIL import Image
import os


def fix_image(image_path):
    try:
        img = Image.open(image_path)
        img.save(image_path, format='PNG', quality=95)
        print(f"Fixed {image_path}")
    except Exception as e:
        print(f"Failed to fix {image_path}: {e}")


def main():
    image_paths = []
    for i in range(0, 18):
        image_paths.append(f"images/player's wife/sunflower{i}.png")  # 列出你需要修复的图像文件路径
    for path in image_paths:
        fix_image(path)


if __name__ == "__main__":
    main()
'''

import subprocess


def fix_image(image_path):
    output_path = image_path.replace('.png', '_fixed.png')
    try:
        subprocess.run(["convert", image_path, "-strip", output_path], check=True)
        print(f"Fixed {image_path}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to fix {image_path}: {e}")


def main():
    image_paths = []
    for i in range(0, 18):
        image_paths.append(f"images/player's wife/sunflower{i}.png")  # 列出你需要修复的图像文件路径
    for path in image_paths:
        fix_image(path)

if __name__ == "__main__":
    main()