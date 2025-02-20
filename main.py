import logging
import os
import subprocess
from typing import Tuple

import AppKit
import numpy as np
from PIL import Image

logging.basicConfig(level=logging.INFO)


def main():
    print("Hello from wallpaper-bot!")


def set_wallpaper_for_macos(image: str):
    """使用 osascript 设置壁纸"""
    try:
        subprocess.run(
            [
                "osascript",
                "-e",
                f'''tell application "System Events"
                        tell every desktop
                            set picture to "{image}"
                        end tell
                    end tell
                ''',
            ],
            check=True,
        )
        logging.info("壁纸设置成功")
    except subprocess.CalledProcessError as e:
        print(f"壁纸设置失败: {e}")


def get_screen_resolution_for_macos():
    """获取屏幕分辨率"""
    screen = AppKit.NSScreen.mainScreen()  # pyright: ignore
    rect = screen.frame()
    return int(rect.size.width), int(rect.size.height)


def generate_gradient_image(
    width: int,
    height: int,
    start_color: Tuple[int, int, int],
    end_color: Tuple[int, int, int],
) -> Image.Image:
    """生成渐变色图片"""
    img = Image.new("RGB", (width, height))

    # 创建一个 numpy 数组来存储像素数据
    pixels = np.zeros((height, width, 3), dtype=np.uint8)

    # 将颜色转换为 numpy 数组
    start_color_np: np.ndarray = np.array(start_color)
    end_color_np: np.ndarray = np.array(end_color)

    # 使用 linspace 函数生成颜色梯度
    color_steps = np.linspace(start_color_np, end_color_np, height, endpoint=True)

    # 将颜色应用到像素数组，将梯度颜色复制到所有列
    pixels[:, :, :] = color_steps[:, None, :]

    img = Image.fromarray(pixels)  # 将像素数组转换为 PIL 图像对象

    return img


def get_color(index: int):
    """获取指定索引的颜色"""
    # 定义渐变色，使用数组存储，颜色为十六进制字符串
    gradients = [
        ("#4FC3F7", "#29B6F6"),  # 活力海洋
        ("#9575CD", "#673AB7"),  # 梦幻紫霞
        ("#FF7043", "#E64A19"),  # 热情火花
        ("#A5D6A7", "#4CAF50"),  # 清新薄荷
        ("#FFB300", "#FF6F00"),  # 日落金橙
        ("#64B5F6", "#1E88E5"),  # 静谧蓝调
        ("#F48FB1", "#E1BEE7"),  # 柔和粉彩
        ("#81C784", "#388E3C"),  # 森林秘境
        ("#7E57C2", "#4527A0"),  # 宇宙星辰
        ("#FFE0B2", "#EF6C00"),  # 沙滩海岸
    ]
    return gradients[index % len(gradients)]


def hex_to_rgb(hex_color) -> Tuple[int, int, int]:
    """将十六进制颜色字符串转换为 RGB 元组"""
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return (r, g, b)


if __name__ == "__main__":
    main()
    width, height = get_screen_resolution_for_macos()
    print(f"屏幕分辨率: {width}x{height}")
    color = get_color(0)
    print(color)
    start_color = hex_to_rgb(color[0])
    end_color = hex_to_rgb(color[1])
    img = generate_gradient_image(width, height, start_color, end_color)
    # 保存到 img/ 目录下，递增的数字
    img_name = f"img/{len(os.listdir('img')) + 1}.png"
    # mkdir
    os.makedirs(os.path.dirname(img_name), exist_ok=True)
    img.save(img_name)
    # 设置为壁纸
    set_wallpaper_for_macos(img_name)
