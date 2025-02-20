import logging
import os
import subprocess
from typing import Tuple

import AppKit
import cv2
import numpy as np
from PIL import Image

logging.basicConfig(level=logging.INFO)


def main():
    print("Hello from wallpaper-bot!")


class GradientImageGenerater:
    def __init__(self, use: str):
        self.use = use

    def generate(
        self,
        width: int,
        height: int,
        start_color: Tuple[int, int, int] | str,
        end_color: Tuple[int, int, int] | str,
    ) -> np.ndarray:
        if self.use == "cv":
            """使用 OpenCV 库生成渐变色图片"""
            pixels = self._generate_numpy(width, height, start_color, end_color)
            pixels_bgr = pixels[:, :, ::-1]
            return pixels_bgr
        elif self.use == "pillow":
            """使用 Pillow 库生成渐变色图片"""
            return self._generate_numpy(width, height, start_color, end_color)
        else:
            raise ValueError("Invalid use")

    def generate_and_show(
        self,
        width: int,
        height: int,
        start_color: Tuple[int, int, int] | str,
        end_color: Tuple[int, int, int] | str,
    ) -> None:
        """生成渐变色图片并显示"""
        pixels = self.generate(width, height, start_color, end_color)
        if self.use == "cv":
            cv2.imshow("Gradient Image", pixels)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        elif self.use == "pillow":
            image = Image.fromarray(pixels)
            image.show()
        else:
            raise ValueError("Invalid use")

    def _generate_numpy(
        self,
        width: int,
        height: int,
        start_color: Tuple[int, int, int] | str,
        end_color: Tuple[int, int, int] | str,
    ) -> np.ndarray:
        """生成渐变色图片 numpy 数组，可以供 openCV 或 Pillow 使用"""
        # 创建一个 numpy 数组来存储像素数据
        pixels = np.zeros((height, width, 3), dtype=np.uint8)

        # 如果颜色是字符串，将其转换为 RGB 元组
        if isinstance(start_color, str):
            if not start_color.startswith("#"):
                raise ValueError("Invalid color format")
            start_color = hex_to_rgb(start_color)
        if isinstance(end_color, str):
            if not end_color.startswith("#"):
                raise ValueError("Invalid color format")
            end_color = hex_to_rgb(end_color)

        # 将颜色转换为 numpy 数组
        start_color_np: np.ndarray = np.array(start_color)
        end_color_np: np.ndarray = np.array(end_color)

        # 使用 linspace 函数生成颜色梯度
        color_steps = np.linspace(start_color_np, end_color_np, height, endpoint=True)

        # 将颜色应用到像素数组，将梯度颜色复制到所有列
        pixels[:, :, :] = color_steps[:, None, :]
        return pixels


def set_wallpaper_for_macos(image: str):
    """设置壁纸(macos) 使用 osascript"""
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


def get_linux_desktop_environment() -> str | None:
    """获取Linux桌面环境"""
    desktop_env = os.environ.get("XDG_CURRENT_DESKTOP")
    if desktop_env:
        return desktop_env.lower()
    return None


def set_wallpaper_for_linux(image: str):
    """设置壁纸(linux) 使用 feh"""
    # 如果是 hyprland，使用 hyprpaper
    if get_linux_desktop_environment() == "hyprland":
        try:
            subprocess.run(
                [
                    "hyprpaper",
                    "-f",
                    image,
                ],
                check=True,
            )
            logging.info("壁纸设置成功")
        except subprocess.CalledProcessError as e:
            print(f"壁纸设置失败: {e}")
    # 如果是 sway
    elif get_linux_desktop_environment() == "sway":
        try:
            subprocess.run(
                [
                    "swaybg",
                    "-i",
                    image,
                ],
                check=True,
            )
            logging.info("壁纸设置成功")
        except subprocess.CalledProcessError as e:
            print(f"壁纸设置失败: {e}")
    # 如果是其他桌面环境
    else:
        try:
            subprocess.run(
                [
                    "feh",
                    "--bg-scale",
                    image,
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
    generater = GradientImageGenerater("cv")
    generater.generate_and_show(width, height, color[0], color[1])
