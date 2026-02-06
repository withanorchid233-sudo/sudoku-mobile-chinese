"""
Sudoku Game - Mobile Compatible Version
数独游戏 - 移动端兼容版本
支持触摸屏操作
"""

import pygame
import sys
import time
from sudoku_logic import SudokuLogic
from sudoku_ui import SudokuUIManager

# Mobile-friendly constants
def get_screen_size():
    """获取屏幕尺寸（自适应）"""
    try:
        # 尝试获取实际屏幕尺寸
        info = pygame.display.Info()
        width = min(info.current_w, 800)
        height = min(info.current_h, 1200)
        return width, height
    except:
        # 默认尺寸
        return 800, 1200

SCREEN_WIDTH, SCREEN_HEIGHT = get_screen_size()
GRID_SIZE = min(int(SCREEN_WIDTH * 0.9), 500)
CELL_SIZE = GRID_SIZE // 9
GRID_X = (SCREEN_WIDTH - GRID_SIZE) // 2
GRID_Y = int(SCREEN_HEIGHT * 0.15)

# Colors
BG_COLOR = (10, 15, 30)
GRID_COLOR = (100, 150, 200)
FIXED_COLOR = (150, 200, 255)
USER_COLOR = (255, 255, 255)
SELECTED_COLOR = (0, 255, 255, 100)
ERROR_COLOR = (255, 100, 100)
CORRECT_COLOR = (100, 255, 150)

class SudokuGameMobile:
    def __init__(self, language='en'):
        pygame.init()
        
        # Mobile fullscreen
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Sudoku Mobile")
        self.clock = pygame.time.Clock()
        
        # Language setting
        self.language = language
        self.texts = self._get_texts()
        
        # Fonts (scaled for mobile)
        font_scale = SCREEN_WIDTH / 800
        self.title_font = pygame.font.SysFont("arial", int(40 * font_scale), bold=True)
        self.cell_font = pygame.font.SysFont("arial", int(28 * font_scale), bold=True)
        self.small_font = pygame.font.SysFont("arial", int(16 * font_scale), bold=True)
        self.button_font = pygame.font.SysFont("arial", int(18 * font_scale), bold=True)
        self.number_button_font = pygame.font.SysFont("arial", int(24 * font_scale), bold=True)
        
        # Managers
        self.logic = SudokuLogic()
        self.ui_manager = SudokuUIManager(self.screen)
        
        # Game state
        self.state = "menu"
        self.difficulty = "medium"
        self.puzzle = None
        self.solution = None
        self.current_board = None
        self.fixed_cells = set()
        self.selected_cell = None
        self.errors = set()
        self.history = []
        self.start_time = None
        self.elapsed_time = 0
        
        # Mobile-specific: Number pad buttons
        self.number_buttons = []
        self.setup_number_pad()
    
    def setup_number_pad(self):
        """设置触摸数字键盘"""
        pad_y = GRID_Y + GRID_SIZE + 10
        button_size = CELL_SIZE
        gap = 5
        
        # 计算按钮起始位置（居中）
        total_width = button_size * 9 + gap * 8
        start_x = (SCREEN_WIDTH - total_width) // 2
        
        self.number_buttons = []
        for i in range(1, 10):
            x = start_x + (i - 1) * (button_size + gap)
            rect = pygame.Rect(x, pad_y, button_size, button_size)
            self.number_buttons.append({'rect': rect, 'number': i})
        
        # Delete/Clear button
        self.delete_btn = pygame.Rect(GRID_X, pad_y + button_size + 10, 
                                       GRID_SIZE // 3, 40)
        self.hint_btn = pygame.Rect(GRID_X + GRID_SIZE // 3 + 5, pad_y + button_size + 10,
                                     GRID_SIZE // 3, 40)
        self.check_btn = pygame.Rect(GRID_X + 2 * GRID_SIZE // 3 + 10, pad_y + button_size + 10,
                                      GRID_SIZE // 3 - 10, 40)
    
    def _get_texts(self):
        """根据语言返回文本字典"""
        if self.language == 'zh':
            return {
                'title': '数独',
                'select_difficulty': '选择难度',
                'easy': '简单',
                'medium': '中等',
                'hard': '困难',
                'expert': '专家',
                'time': '时间',
                'hint': '提示',
                'check': '检查',
                'new_game': '新游戏',
                'delete': '删除',
                'victory': '胜利！',
                'difficulty_label': '难度',
                'press_to_continue': '点击继续',
                'tap_cell': '点击格子输入数字'
            }
        else:
            return {
                'title': 'SUDOKU',
                'select_difficulty': 'Select Difficulty',
                'easy': 'Easy',
                'medium': 'Medium',
                'hard': 'Hard',
                'expert': 'Expert',
                'time': 'Time',
                'hint': 'Hint',
                'check': 'Check',
                'new_game': 'New Game',
                'delete': 'Delete',
                'victory': 'VICTORY!',
                'difficulty_label': 'Difficulty',
                'press_to_continue': 'Tap to continue',
                'tap_cell': 'Tap cell to input number'
            }
    
    def new_game(self, difficulty):
        """开始新游戏"""
        self.difficulty = difficulty
        self.puzzle, self.solution = self.logic.generate_puzzle(difficulty)
        self.current_board = [row[:] for row in self.puzzle]
        
        self.fixed_cells = set()
        for i in range(9):
            for j in range(9):
                if self.puzzle[i][j] != 0:
                    self.fixed_cells.add((i, j))
        
        self.selected_cell = None
        self.errors = set()
        self.history = []
        self.start_time = time.time()
        self.state = "playing"
        self.setup_number_pad()
    
    def handle_input(self):
        """处理输入事件（触摸优化）"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.FINGERDOWN:
                if event.type == pygame.FINGERDOWN:
                    # Convert finger coordinates to pixel coordinates
                    pos = (int(event.x * SCREEN_WIDTH), int(event.y * SCREEN_HEIGHT))
                else:
                    pos = event.pos
                
                if self.state == "menu":
                    self.handle_menu_touch(pos)
                elif self.state == "playing":
                    self.handle_game_touch(pos)
                elif self.state == "won":
                    self.state = "menu"
    
    def handle_menu_touch(self, pos):
        """处理菜单触摸"""
        difficulties = ["easy", "medium", "hard", "expert"]
        button_height = 60
        button_width = int(SCREEN_WIDTH * 0.7)
        start_y = SCREEN_HEIGHT // 3
        
        for i, diff in enumerate(difficulties):
            btn_rect = pygame.Rect((SCREEN_WIDTH - button_width) // 2,
                                   start_y + i * (button_height + 15),
                                   button_width, button_height)
            if btn_rect.collidepoint(pos):
                self.new_game(diff)
    
    def handle_game_touch(self, pos):
        """处理游戏触摸"""
        # Check grid cells
        if GRID_X <= pos[0] < GRID_X + GRID_SIZE and \
           GRID_Y <= pos[1] < GRID_Y + GRID_SIZE:
            col = (pos[0] - GRID_X) // CELL_SIZE
            row = (pos[1] - GRID_Y) // CELL_SIZE
            if (row, col) not in self.fixed_cells:
                self.selected_cell = (row, col)
            return
        
        # Check number pad
        for btn in self.number_buttons:
            if btn['rect'].collidepoint(pos):
                if self.selected_cell:
                    self.place_number(self.selected_cell[0], self.selected_cell[1], btn['number'])
                return
        
        # Check control buttons
        if self.delete_btn.collidepoint(pos):
            if self.selected_cell:
                self.place_number(self.selected_cell[0], self.selected_cell[1], 0)
        elif self.hint_btn.collidepoint(pos):
            self.get_hint()
        elif self.check_btn.collidepoint(pos):
            self.check_solution()
    
    def place_number(self, row, col, num):
        """放置数字"""
        if (row, col) in self.fixed_cells:
            return
        
        old_num = self.current_board[row][col]
        self.history.append((row, col, old_num))
        self.current_board[row][col] = num
        
        if (row, col) in self.errors:
            self.errors.remove((row, col))
        
        if self.logic.check_complete(self.current_board):
            self.state = "won"
            self.elapsed_time = time.time() - self.start_time
    
    def get_hint(self):
        """获取提示"""
        row, col, num = self.logic.get_hint(self.current_board, self.solution)
        if row is not None:
            self.place_number(row, col, num)
            self.selected_cell = (row, col)
    
    def check_solution(self):
        """检查解答"""
        self.errors = set()
        for i in range(9):
            for j in range(9):
                if self.current_board[i][j] != 0:
                    if self.current_board[i][j] != self.solution[i][j]:
                        self.errors.add((i, j))
    
    def draw(self):
        """绘制游戏画面"""
        self.screen.fill(BG_COLOR)
        current_time = pygame.time.get_ticks()
        self.ui_manager.draw_particle_bg(current_time)
        
        if self.state == "menu":
            self.draw_menu()
        elif self.state == "playing":
            self.draw_game()
        elif self.state == "won":
            self.draw_won()
        
        pygame.display.flip()
    
    def draw_menu(self):
        """绘制菜单"""
        self.ui_manager.draw_neon_text(self.texts['title'], 
                                       (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6),
                                       self.title_font, (0, 255, 255))
        
        self.ui_manager.draw_3d_text(self.texts['select_difficulty'],
                                     (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4),
                                     self.small_font, (150, 200, 255), depth=2)
        
        difficulties = [
            (self.texts['easy'], "easy"),
            (self.texts['medium'], "medium"),
            (self.texts['hard'], "hard"),
            (self.texts['expert'], "expert")
        ]
        
        button_height = 60
        button_width = int(SCREEN_WIDTH * 0.7)
        start_y = SCREEN_HEIGHT // 3
        
        for i, (label, diff) in enumerate(difficulties):
            btn_rect = pygame.Rect((SCREEN_WIDTH - button_width) // 2,
                                   start_y + i * (button_height + 15),
                                   button_width, button_height)
            self.ui_manager.draw_button(btn_rect, label, self.button_font, False)
    
    def draw_game(self):
        """绘制游戏界面"""
        # Title
        title_str = f"{self.texts['title']} - {self.texts[self.difficulty]}"
        self.ui_manager.draw_3d_text(title_str, (SCREEN_WIDTH // 2, 30),
                                     self.small_font, (0, 255, 255), depth=2)
        
        # Timer
        if self.start_time:
            elapsed = int(time.time() - self.start_time)
            mins = elapsed // 60
            secs = elapsed % 60
            timer_str = f"{self.texts['time']}: {mins:02d}:{secs:02d}"
            self.ui_manager.draw_3d_text(timer_str, (SCREEN_WIDTH // 2, 60),
                                        self.small_font, (255, 255, 255), depth=2)
        
        # Grid
        self.draw_grid()
        
        # Number pad
        self.draw_number_pad()
        
        # Control buttons
        self.ui_manager.draw_button(self.delete_btn, self.texts['delete'],
                                    self.small_font, False)
        self.ui_manager.draw_button(self.hint_btn, self.texts['hint'],
                                    self.small_font, False)
        self.ui_manager.draw_button(self.check_btn, self.texts['check'],
                                    self.small_font, False)
    
    def draw_grid(self):
        """绘制网格（与PC版相同）"""
        grid_rect = pygame.Rect(GRID_X, GRID_Y, GRID_SIZE, GRID_SIZE)
        
        # Shadow
        shadow_rect = pygame.Rect(GRID_X + 4, GRID_Y + 4, GRID_SIZE, GRID_SIZE)
        shadow_surf = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
        shadow_surf.fill((0, 0, 0, 100))
        self.screen.blit(shadow_surf, shadow_rect.topleft)
        
        self.ui_manager.draw_glass_rect(grid_rect, color=(15, 25, 40), alpha=240)
        
        # Draw cells
        for i in range(9):
            for j in range(9):
                x = GRID_X + j * CELL_SIZE
                y = GRID_Y + i * CELL_SIZE
                cell_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                
                is_selected = self.selected_cell == (i, j)
                self.ui_manager.draw_3d_cell(cell_rect, is_selected)
                
                num = self.current_board[i][j]
                if num != 0:
                    if (i, j) in self.fixed_cells:
                        color = (150, 200, 255)
                    elif (i, j) in self.errors:
                        color = (255, 100, 100)
                    else:
                        color = (255, 255, 255)
                    
                    center_pos = (x + CELL_SIZE // 2, y + CELL_SIZE // 2)
                    self.ui_manager.draw_3d_number(num, center_pos, self.cell_font, color, depth=3)
        
        # Draw grid lines (simplified for mobile)
        for i in range(10):
            thickness = 4 if i % 3 == 0 else 1
            color = (0, 200, 255) if i % 3 == 0 else (80, 120, 160)
            
            # Horizontal
            pygame.draw.line(self.screen, color,
                           (GRID_X, GRID_Y + i * CELL_SIZE),
                           (GRID_X + GRID_SIZE, GRID_Y + i * CELL_SIZE), thickness)
            # Vertical
            pygame.draw.line(self.screen, color,
                           (GRID_X + i * CELL_SIZE, GRID_Y),
                           (GRID_X + i * CELL_SIZE, GRID_Y + GRID_SIZE), thickness)
    
    def draw_number_pad(self):
        """绘制数字键盘"""
        for btn in self.number_buttons:
            # Simple button style for numbers
            color = (40, 60, 90) if btn['rect'].collidepoint(pygame.mouse.get_pos()) else (30, 45, 70)
            pygame.draw.rect(self.screen, color, btn['rect'])
            pygame.draw.rect(self.screen, (0, 200, 255), btn['rect'], 2)
            
            # Number
            num_str = str(btn['number'])
            self.ui_manager.draw_3d_text(num_str, btn['rect'].center,
                                        self.number_button_font, (255, 255, 255), depth=2)
    
    def draw_won(self):
        """绘制胜利画面"""
        self.draw_game()
        
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        panel_rect = pygame.Rect(SCREEN_WIDTH // 10, SCREEN_HEIGHT // 4,
                                 SCREEN_WIDTH * 4 // 5, SCREEN_HEIGHT // 2)
        self.ui_manager.draw_glass_rect(panel_rect, alpha=230, border_color=(0, 255, 150))
        
        self.ui_manager.draw_neon_text(self.texts['victory'],
                                       (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3),
                                       self.title_font, (0, 255, 150), glow_color=(0, 200, 100))
        
        mins = int(self.elapsed_time // 60)
        secs = int(self.elapsed_time % 60)
        time_str = f"{self.texts['time']}: {mins:02d}:{secs:02d}"
        self.ui_manager.draw_3d_text(time_str, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
                                    self.button_font, (255, 255, 255), depth=2)
        
        diff_str = f"{self.texts['difficulty_label']}: {self.texts[self.difficulty]}"
        self.ui_manager.draw_3d_text(diff_str, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50),
                                    self.button_font, (150, 200, 255), depth=2)
        
        self.ui_manager.draw_3d_text(self.texts['press_to_continue'],
                                    (SCREEN_WIDTH // 2, SCREEN_HEIGHT * 2 // 3),
                                    self.small_font, (150, 150, 150), depth=1)
    
    def run(self):
        """主游戏循环"""
        while True:
            self.handle_input()
            self.draw()
            self.clock.tick(60)

if __name__ == "__main__":
    import sys
    language = 'en'
    if len(sys.argv) > 1:
        if sys.argv[1] in ['zh', 'cn', 'chinese']:
            language = 'zh'
    
    game = SudokuGameMobile(language=language)
    game.run()
