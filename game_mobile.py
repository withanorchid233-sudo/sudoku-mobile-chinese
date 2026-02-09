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

# Mobile-friendly helpers
def get_safe_fonts(size, bold=False):
    """安卓兼容的字体获取逻辑"""
    test_fonts = ["sans-serif", "noto sans cjk jp", "arial", "droid sans fallback", None]
    for font_name in test_fonts:
        try:
            return pygame.font.SysFont(font_name, size, bold=bold)
        except:
            continue
    return pygame.font.Font(None, size)

# Colors (Static)
BG_COLOR = (10, 15, 30)
GRID_COLOR = (100, 150, 200)
FIXED_COLOR = (150, 200, 255)
USER_COLOR = (255, 255, 255)
SELECTED_COLOR = (0, 255, 255, 100)
ERROR_COLOR = (255, 100, 100)
CORRECT_COLOR = (100, 255, 150)

class SudokuGameMobile:
    def __init__(self, language='en'):
        # 确保 pygame 已初始化
        if not pygame.get_init():
            pygame.init()
        
        # 1. 设置屏幕（强制使用 SCALED 模式，提高安卓兼容性）
        info = pygame.display.Info()
        self.width = info.current_w if info.current_w > 0 else 800
        self.height = info.current_h if info.current_h > 0 else 1200
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.SCALED | pygame.FULLSCREEN)
        
        pygame.display.set_caption("Sudoku 3D")
        self.clock = pygame.time.Clock()
        
        # 2. 语言设置
        self.language = language
        self.texts = self._get_texts()
        
        # 3. 字体延迟加载优化
        font_scale = self.width / 400
        self.title_font = get_safe_fonts(int(24 * font_scale), bold=True)
        self.cell_font = get_safe_fonts(int(18 * font_scale), bold=True)
        self.small_font = get_safe_fonts(int(10 * font_scale), bold=True)
        self.button_font = get_safe_fonts(int(12 * font_scale), bold=True)
        self.number_button_font = get_safe_fonts(int(16 * font_scale), bold=True)
        
        # 4. 逻辑引擎
        self.logic = SudokuLogic()
        
        # 🚀 关键修改：UI 管理器现在不带参数，稍后手动启动背景
        self.ui_manager = SudokuUIManager(self.screen)
        
        # 5. 布局参数计算
        self.grid_size = min(int(self.width * 0.92), 520)
        self.cell_size = self.grid_size // 9
        self.grid_x = (self.width - self.grid_size) // 2
        self.grid_y = int(self.height * 0.12)
        
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
        pad_y = self.grid_y + self.grid_size + 15
        button_size = self.cell_size
        gap = 4
        
        # 计算按钮起始位置（居中）
        total_width = button_size * 9 + gap * 8
        start_x = (self.width - total_width) // 2
        
        self.number_buttons = []
        for i in range(1, 10):
            x = start_x + (i - 1) * (button_size + gap)
            rect = pygame.Rect(x, pad_y, button_size, button_size)
            self.number_buttons.append({'rect': rect, 'number': i})
        
        # 功能按钮
        btn_y = pad_y + button_size + 15
        btn_w = self.grid_size // 3 - 5
        self.delete_btn = pygame.Rect(self.grid_x, btn_y, btn_w, 45)
        self.hint_btn = pygame.Rect(self.grid_x + btn_w + 5, btn_y, btn_w, 45)
        self.check_btn = pygame.Rect(self.grid_x + 2 * (btn_w + 5), btn_y, btn_w, 45)
    
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
            
                if event.type == pygame.FINGERDOWN:
                    # 获取手指触屏的相对坐标并转换为像素坐标
                    pos = (int(event.x * self.width), int(event.y * self.height))
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
        button_width = int(self.width * 0.7)
        start_y = self.height // 3
        
        for i, diff in enumerate(difficulties):
            btn_rect = pygame.Rect((self.width - button_width) // 2,
                                   start_y + i * (button_height + 15),
                                   button_width, button_height)
            if btn_rect.collidepoint(pos):
                self.new_game(diff)
    
    def handle_game_touch(self, pos):
        """处理游戏触摸"""
        # Check grid cells
        if self.grid_x <= pos[0] < self.grid_x + self.grid_size and \
           self.grid_y <= pos[1] < self.grid_y + self.grid_size:
            col = (pos[0] - self.grid_x) // self.cell_size
            row = (pos[1] - self.grid_y) // self.cell_size
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
                                       (self.width // 2, self.height // 6),
                                       self.title_font, (0, 255, 255))
        
        self.ui_manager.draw_3d_text(self.texts['select_difficulty'],
                                     (self.width // 2, self.height // 4),
                                     self.small_font, (150, 200, 255), depth=2)
        
        difficulties = [
            (self.texts['easy'], "easy"),
            (self.texts['medium'], "medium"),
            (self.texts['hard'], "hard"),
            (self.texts['expert'], "expert")
        ]
        
        button_height = 60
        button_width = int(self.width * 0.7)
        start_y = self.height // 3
        
        for i, (label, diff) in enumerate(difficulties):
            btn_rect = pygame.Rect((self.width - button_width) // 2,
                                   start_y + i * (button_height + 15),
                                   button_width, button_height)
            self.ui_manager.draw_button(btn_rect, label, self.button_font, False)
    
    def draw_game(self):
        """绘制游戏界面"""
        # Title
        title_str = f"{self.texts['title']} - {self.texts[self.difficulty]}"
        self.ui_manager.draw_3d_text(title_str, (self.width // 2, 30),
                                     self.small_font, (0, 255, 255), depth=2)
        
        # Timer
        if self.start_time:
            elapsed = int(time.time() - self.start_time)
            mins = elapsed // 60
            secs = elapsed % 60
            timer_str = f"{self.texts['time']}: {mins:02d}:{secs:02d}"
            self.ui_manager.draw_3d_text(timer_str, (self.width // 2, 60),
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
        """绘制网格（自适应布局）"""
        grid_rect = pygame.Rect(self.grid_x, self.grid_y, self.grid_size, self.grid_size)
        
        # 阴影
        shadow_rect = pygame.Rect(self.grid_x + 3, self.grid_y + 3, self.grid_size, self.grid_size)
        shadow_surf = pygame.Surface((self.grid_size, self.grid_size), pygame.SRCALPHA)
        shadow_surf.fill((0, 0, 0, 80))
        self.screen.blit(shadow_surf, shadow_rect.topleft)
        
        self.ui_manager.draw_glass_rect(grid_rect, color=(15, 25, 40), alpha=240)
        
        # 绘制格子
        for i in range(9):
            for j in range(9):
                x = self.grid_x + j * self.cell_size
                y = self.grid_y + i * self.cell_size
                cell_rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                
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
                    
                    center_pos = (x + self.cell_size // 2, y + self.cell_size // 2)
                    self.ui_manager.draw_3d_number(num, center_pos, self.cell_font, color, depth=3)
        
        # 绘制网格线
        for i in range(10):
            thickness = 3 if i % 3 == 0 else 1
            color = (0, 200, 255) if i % 3 == 0 else (60, 100, 140)
            
            # 横线
            pygame.draw.line(self.screen, color,
                           (self.grid_x, self.grid_y + i * self.cell_size),
                           (self.grid_x + self.grid_size, self.grid_y + i * self.cell_size), thickness)
            # 纵线
            pygame.draw.line(self.screen, color,
                           (self.grid_x + i * self.cell_size, self.grid_y),
                           (self.grid_x + i * self.cell_size, self.grid_y + self.grid_size), thickness)
    
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
        
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        panel_rect = pygame.Rect(self.width // 10, self.height // 4,
                                 self.width * 4 // 5, self.height // 2)
        self.ui_manager.draw_glass_rect(panel_rect, alpha=230, border_color=(0, 255, 150))
        
        self.ui_manager.draw_neon_text(self.texts['victory'],
                                       (self.width // 2, self.height // 3),
                                       self.title_font, (0, 255, 150), glow_color=(0, 200, 100))
        
        mins = int(self.elapsed_time // 60)
        secs = int(self.elapsed_time % 60)
        time_str = f"{self.texts['time']}: {mins:02d}:{secs:02d}"
        self.ui_manager.draw_3d_text(time_str, (self.width // 2, self.height // 2),
                                    self.button_font, (255, 255, 255), depth=2)
        
        diff_str = f"{self.texts['difficulty_label']}: {self.texts[self.difficulty]}"
        self.ui_manager.draw_3d_text(diff_str, (self.width // 2, self.height // 2 + 50),
                                    self.button_font, (150, 200, 255), depth=2)
        
        self.ui_manager.draw_3d_text(self.texts['press_to_continue'],
                                    (self.width // 2, self.height * 2 // 3),
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
