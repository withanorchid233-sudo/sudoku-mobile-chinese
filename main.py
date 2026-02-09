"""
Sudoku Mobile - SAFE MODE
数独移动版 - 极简排错版
"""

import os
import sys

# 1. 强制使用安卓最基础的驱动，禁用所有加速
os.environ['SDL_VIDEODRIVER'] = 'android'
os.environ['SDL_VIDEO_ALLOW_SCREENSAVER'] = '1'

import pygame

def main():
    try:
        # 非常重要：在某些安卓版本上，必须先启动这个
        pygame.display.init()
        pygame.font.init()
        
        # 获取屏幕但不请求全屏或硬件加速，只求“能动”
        info = pygame.display.Info()
        screen = pygame.display.set_mode((info.current_w, info.current_h))
        
        # 此时再导入剥离了复杂UI的游戏类
        from game_mobile import SudokuGameMobile
        
        game = SudokuGameMobile(manual_screen=screen)
        game.run()
    except Exception as e:
        # 如果还是崩，这行字一定会救命
        import traceback
        error_msg = traceback.format_exc()
        try:
            with open("crash_log.txt", "w") as f:
                f.write(error_msg)
        except:
            pass
        pygame.quit()

if __name__ == "__main__":
    main()
