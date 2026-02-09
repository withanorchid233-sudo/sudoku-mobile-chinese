"""
Sudoku Mobile - Main Entry Point
数独移动版 - 主入口
"""

import os
import sys

# 1. 强制设置安卓环境环境变量，防止视频驱动崩溃
os.environ['SDL_VIDEODRIVER'] = 'android'
os.environ['KIVY_NO_ARGS'] = '1'

import pygame

def main():
    # 2. 在导入游戏逻辑前先初始化 Pygame
    try:
        pygame.init()
    except Exception as e:
        print(f"Pygame init failed: {e}")
        return

    # 3. 延迟导入，确保 Pygame 环境已稳定
    # 这样可以防止在安卓上产生循环导入或资源锁死
    from game_mobile import SudokuGameMobile
    
    try:
        # 直接启动中文版
        game = SudokuGameMobile(language='zh')
        game.run()
    except Exception as e:
        # 记录崩溃日志（尝试写在私有目录）
        try:
            with open("crash_log.txt", "w") as f:
                f.write(str(e))
        except:
            pass
        pygame.quit()

if __name__ == "__main__":
    main()
