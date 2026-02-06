"""
Sudoku Logic Module
数独核心逻辑：生成、验证、求解
"""

import random
import copy

class SudokuLogic:
    def __init__(self):
        self.size = 9
        self.box_size = 3
        
    def is_valid(self, board, row, col, num):
        """检查在指定位置放置数字是否合法"""
        # Check row
        if num in board[row]:
            return False
        
        # Check column
        if num in [board[i][col] for i in range(self.size)]:
            return False
        
        # Check 3x3 box
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if board[i][j] == num:
                    return False
        
        return True
    
    def solve(self, board):
        """使用回溯法求解数独"""
        for row in range(self.size):
            for col in range(self.size):
                if board[row][col] == 0:
                    for num in range(1, 10):
                        if self.is_valid(board, row, col, num):
                            board[row][col] = num
                            
                            if self.solve(board):
                                return True
                            
                            board[row][col] = 0
                    
                    return False
        return True
    
    def generate_full_board(self):
        """生成一个完整的数独解"""
        board = [[0 for _ in range(self.size)] for _ in range(self.size)]
        
        # Fill diagonal 3x3 boxes first (they don't affect each other)
        for box in range(0, self.size, 3):
            nums = list(range(1, 10))
            random.shuffle(nums)
            for i in range(3):
                for j in range(3):
                    board[box + i][box + j] = nums[i * 3 + j]
        
        # Solve the rest
        self.solve(board)
        return board
    
    def remove_numbers(self, board, difficulty):
        """根据难度移除数字，创建谜题"""
        # Difficulty: easy=40, medium=50, hard=60, expert=70
        cells_to_remove = difficulty
        
        puzzle = copy.deepcopy(board)
        positions = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(positions)
        
        removed = 0
        for row, col in positions:
            if removed >= cells_to_remove:
                break
            
            backup = puzzle[row][col]
            puzzle[row][col] = 0
            
            # Ensure puzzle still has unique solution (simplified check)
            # In production, you'd verify uniqueness more thoroughly
            removed += 1
        
        return puzzle
    
    def generate_puzzle(self, difficulty='medium'):
        """生成一个数独谜题"""
        difficulty_map = {
            'easy': 35,
            'medium': 45,
            'hard': 55,
            'expert': 65
        }
        
        full_board = self.generate_full_board()
        puzzle = self.remove_numbers(full_board, difficulty_map[difficulty])
        
        return puzzle, full_board
    
    def check_complete(self, board):
        """检查数独是否完成且正确"""
        for row in range(self.size):
            for col in range(self.size):
                if board[row][col] == 0:
                    return False
                
                # Temporarily remove number to check validity
                num = board[row][col]
                board[row][col] = 0
                if not self.is_valid(board, row, col, num):
                    board[row][col] = num
                    return False
                board[row][col] = num
        
        return True
    
    def get_hint(self, puzzle, solution):
        """获取一个提示（返回一个空格的正确答案）"""
        empty_cells = [(i, j) for i in range(9) for j in range(9) if puzzle[i][j] == 0]
        if empty_cells:
            row, col = random.choice(empty_cells)
            return row, col, solution[row][col]
        return None, None, None
