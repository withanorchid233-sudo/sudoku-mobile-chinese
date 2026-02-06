"""
Sudoku Mobile - Main Entry Point
数独移动版 - 主入口
"""

import sys
from game_mobile import SudokuGameMobile

if __name__ == "__main__":
    # Auto-detect language or use default
    language = 'en'
    if len(sys.argv) > 1:
        if sys.argv[1] in ['zh', 'cn', 'chinese']:
            language = 'zh'
    
    game = SudokuGameMobile(language=language)
    game.run()
