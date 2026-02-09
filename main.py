"""
Sudoku Mobile - Main Entry Point
数独移动版 - 主入口
"""

import os
import sys

# 路径保护：确保在安卓环境下的依赖加载
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

import pygame
from game_mobile import SudokuGameMobile

if __name__ == "__main__":
    # 初始化
    pygame.init()
    
    # 语言检测
    language = 'zh' # 既然是在国内，默认设为中文最稳
    
    try:
        game = SudokuGameMobile(language=language)
        game.run()
    except Exception as e:
        # 如果崩溃，将错误记录在本地，方便日后排查
        with open(os.path.join(current_dir, "crash_log.txt"), "w") as f:
            f.write(f"Crash detected: {str(e)}")
        pygame.quit()
        sys.exit()
