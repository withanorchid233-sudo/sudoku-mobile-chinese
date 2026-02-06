"""
Sudoku UI Manager
数独UI管理器 - 玻璃态设计
"""

import pygame
import random

class SudokuUIManager:
    def __init__(self, screen):
        self.screen = screen
        self.particles = []
        self.init_particles()
    
    def init_particles(self):
        """初始化背景粒子"""
        for _ in range(50):
            self.particles.append({
                'x': random.random() * 800,
                'y': random.random() * 600,
                'vx': (random.random() - 0.5) * 0.5,
                'vy': (random.random() - 0.5) * 0.5,
                'size': random.random() * 2 + 1
            })
    
    def draw_particle_bg(self, current_time):
        """绘制动态粒子背景"""
        import math
        for particle in self.particles:
            # Update position
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            
            # Wrap around
            if particle['x'] < 0: particle['x'] = 800
            if particle['x'] > 800: particle['x'] = 0
            if particle['y'] < 0: particle['y'] = 600
            if particle['y'] > 600: particle['y'] = 0
            
            # Draw
            alpha = int((math.sin(current_time / 1000 + particle['x']) + 1) * 50 + 50)
            pygame.draw.circle(self.screen, (100, 150, 200, alpha), 
                             (int(particle['x']), int(particle['y'])), 
                             int(particle['size']))
    
    def draw_glass_rect(self, rect, color=(20, 30, 50), alpha=200, border_color=(0, 200, 255), border_width=2):
        """绘制玻璃态矩形"""
        # Create surface with alpha
        surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        surf.fill((*color, alpha))
        
        # Draw to screen
        self.screen.blit(surf, rect.topleft)
        
        # Draw border
        if border_width > 0:
            pygame.draw.rect(self.screen, border_color, rect, border_width)
    
    def draw_neon_text(self, text, pos, font, color=(0, 255, 255), glow_color=None):
        """绘制霓虹文字"""
        if glow_color is None:
            glow_color = tuple(max(0, c - 100) for c in color)
        
        # Draw glow layers
        for i in range(3, 0, -1):
            glow_surf = font.render(text, True, glow_color)
            glow_rect = glow_surf.get_rect(center=pos)
            glow_surf.set_alpha(50 * i)
            self.screen.blit(glow_surf, (glow_rect.x - i, glow_rect.y - i))
        
        # Draw main text
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect(center=pos)
        self.screen.blit(text_surf, text_rect)
    
    def draw_button(self, rect, text, font, is_hover=False, active=False):
        """绘制3D按钮"""
        # Button background with gradient for 3D effect
        if active:
            top_color = (60, 255, 160)
            bottom_color = (30, 200, 120)
            border_color = (0, 255, 200)
        elif is_hover:
            top_color = (40, 70, 100)
            bottom_color = (20, 40, 60)
            border_color = (0, 200, 255)
        else:
            top_color = (30, 40, 60)
            bottom_color = (15, 20, 35)
            border_color = (100, 150, 200)
        
        # Draw gradient background
        for i in range(rect.height):
            progress = i / rect.height
            r = int(top_color[0] + (bottom_color[0] - top_color[0]) * progress)
            g = int(top_color[1] + (bottom_color[1] - top_color[1]) * progress)
            b = int(top_color[2] + (bottom_color[2] - top_color[2]) * progress)
            pygame.draw.line(self.screen, (r, g, b), 
                           (rect.left, rect.top + i), 
                           (rect.right, rect.top + i))
        
        # 3D border effect
        # Top and left highlight (lighter)
        highlight_color = tuple(min(255, c + 40) for c in top_color)
        pygame.draw.line(self.screen, highlight_color, rect.topleft, rect.topright, 2)
        pygame.draw.line(self.screen, highlight_color, rect.topleft, rect.bottomleft, 2)
        
        # Bottom and right shadow (darker)
        shadow_color = tuple(max(0, c - 40) for c in bottom_color)
        pygame.draw.line(self.screen, shadow_color, rect.bottomleft, rect.bottomright, 2)
        pygame.draw.line(self.screen, shadow_color, rect.topright, rect.bottomright, 2)
        
        # Outer border
        pygame.draw.rect(self.screen, border_color, rect, 1)
        
        # Button text with 3D effect
        text_color = (255, 255, 255) if is_hover or active else (200, 220, 255)
        self.draw_3d_text(text, rect.center, font, text_color)
    
    def draw_3d_text(self, text, pos, font, color=(255, 255, 255), depth=2):
        """绘制3D文字（带深度阴影）"""
        # Draw shadow layers from deep to shallow
        shadow_color = (0, 0, 0)
        for i in range(depth, 0, -1):
            alpha = 100 - (i * 20)
            shadow_surf = font.render(text, True, shadow_color)
            shadow_surf.set_alpha(alpha)
            shadow_rect = shadow_surf.get_rect(center=(pos[0] + i, pos[1] + i))
            self.screen.blit(shadow_surf, shadow_rect)
        
        # Draw main text with highlight
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect(center=pos)
        self.screen.blit(text_surf, text_rect)
        
        # Top-left highlight for extra depth
        highlight_color = tuple(min(255, c + 60) for c in color)
        highlight_surf = font.render(text, True, highlight_color)
        highlight_surf.set_alpha(80)
        highlight_rect = highlight_surf.get_rect(center=(pos[0] - 1, pos[1] - 1))
        self.screen.blit(highlight_surf, highlight_rect)
    
    def draw_3d_number(self, number, pos, font, color=(255, 255, 255), depth=3):
        """绘制超立体数字"""
        text = str(number)
        
        # Deep shadow (最深的阴影)
        for i in range(depth, 0, -1):
            shadow_alpha = 150 - (i * 30)
            shadow_surf = font.render(text, True, (0, 0, 0))
            shadow_surf.set_alpha(shadow_alpha)
            shadow_rect = shadow_surf.get_rect(center=(pos[0] + i * 2, pos[1] + i * 2))
            self.screen.blit(shadow_surf, shadow_rect)
        
        # Dark outline for definition
        outline_color = (0, 0, 0)
        for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1), (-2, 0), (2, 0), (0, -2), (0, 2)]:
            outline_surf = font.render(text, True, outline_color)
            outline_surf.set_alpha(150)
            outline_rect = outline_surf.get_rect(center=(pos[0] + dx, pos[1] + dy))
            self.screen.blit(outline_surf, outline_rect)
        
        # Main number
        main_surf = font.render(text, True, color)
        main_rect = main_surf.get_rect(center=pos)
        self.screen.blit(main_surf, main_rect)
        
        # Top-left highlight (高光)
        highlight_color = tuple(min(255, int(c * 1.3)) for c in color)
        highlight_surf = font.render(text, True, highlight_color)
        highlight_surf.set_alpha(120)
        highlight_rect = highlight_surf.get_rect(center=(pos[0] - 1.5, pos[1] - 1.5))
        self.screen.blit(highlight_surf, highlight_rect)
    
    def draw_3d_cell(self, rect, is_selected=False):
        """绘制超强3D格子（深度效果增强版）"""
        # Base colors based on selection
        if is_selected:
            base_color = (35, 55, 80)
            inner_color = (25, 45, 70)
        else:
            base_color = (25, 35, 55)
            inner_color = (15, 25, 45)
        
        # 1. Draw deep outer shadow first (给格子加外阴影)
        shadow_offset = 3
        shadow_rect = pygame.Rect(rect.x + shadow_offset, rect.y + shadow_offset, 
                                  rect.width, rect.height)
        shadow_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        for i in range(shadow_offset):
            alpha = 60 - (i * 15)
            pygame.draw.rect(shadow_surf, (0, 0, 0, alpha), 
                           (shadow_offset - i, shadow_offset - i, 
                            rect.width - 2*(shadow_offset - i), 
                            rect.height - 2*(shadow_offset - i)))
        self.screen.blit(shadow_surf, rect.topleft)
        
        # 2. Main body with gradient (渐变填充主体)
        for i in range(rect.height):
            progress = i / rect.height
            # Create gradient from top (lighter) to bottom (darker)
            r = int(base_color[0] + (inner_color[0] - base_color[0]) * progress)
            g = int(base_color[1] + (inner_color[1] - base_color[1]) * progress)
            b = int(base_color[2] + (inner_color[2] - base_color[2]) * progress)
            pygame.draw.line(self.screen, (r, g, b),
                           (rect.left, rect.top + i),
                           (rect.right - 1, rect.top + i))
        
        # 3. Embossed effect - strong bevels (超强斜面效果)
        bevel_size = 5  # 增加斜面宽度
        
        # Top bevel (highlight) - 顶部高光斜面
        for i in range(bevel_size):
            alpha_factor = 1 - (i / bevel_size)
            brightness = int(40 * alpha_factor)
            color = tuple(min(255, c + brightness) for c in base_color)
            pygame.draw.line(self.screen, color,
                           (rect.left + i, rect.top + i),
                           (rect.right - i - 1, rect.top + i))
        
        # Left bevel (highlight) - 左侧高光斜面
        for i in range(bevel_size):
            alpha_factor = 1 - (i / bevel_size)
            brightness = int(35 * alpha_factor)
            color = tuple(min(255, c + brightness) for c in base_color)
            pygame.draw.line(self.screen, color,
                           (rect.left + i, rect.top + i),
                           (rect.left + i, rect.bottom - i - 1))
        
        # Bottom bevel (shadow) - 底部阴影斜面
        for i in range(bevel_size):
            alpha_factor = 1 - (i / bevel_size)
            darkness = int(40 * alpha_factor)
            color = tuple(max(0, c - darkness) for c in inner_color)
            pygame.draw.line(self.screen, color,
                           (rect.left + i, rect.bottom - i - 1),
                           (rect.right - i - 1, rect.bottom - i - 1))
        
        # Right bevel (shadow) - 右侧阴影斜面
        for i in range(bevel_size):
            alpha_factor = 1 - (i / bevel_size)
            darkness = int(35 * alpha_factor)
            color = tuple(max(0, c - darkness) for c in inner_color)
            pygame.draw.line(self.screen, color,
                           (rect.right - i - 1, rect.top + i),
                           (rect.right - i - 1, rect.bottom - i - 1))
        
        # 4. Inner shadow for depth (内阴影增加深度)
        inner_shadow_size = 4
        inner_shadow_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        for i in range(inner_shadow_size):
            alpha = 80 - (i * 15)
            # Top inner shadow
            pygame.draw.line(inner_shadow_surf, (0, 0, 0, alpha),
                           (i, i), (rect.width - i, i))
            # Left inner shadow
            pygame.draw.line(inner_shadow_surf, (0, 0, 0, alpha),
                           (i, i), (i, rect.height - i))
        self.screen.blit(inner_shadow_surf, rect.topleft)
        
        # 5. Outer highlight for extra pop (外部高光)
        highlight_color = tuple(min(255, c + 60) for c in base_color)
        pygame.draw.line(self.screen, highlight_color, 
                        (rect.left, rect.top), (rect.right - 1, rect.top), 2)
        pygame.draw.line(self.screen, highlight_color, 
                        (rect.left, rect.top), (rect.left, rect.bottom - 1), 2)
        
        # 6. Outer shadow edge (外部阴影边缘)
        shadow_edge_color = tuple(max(0, c - 60) for c in inner_color)
        pygame.draw.line(self.screen, shadow_edge_color, 
                        (rect.left + 1, rect.bottom - 1), (rect.right, rect.bottom - 1), 2)
        pygame.draw.line(self.screen, shadow_edge_color, 
                        (rect.right - 1, rect.top + 1), (rect.right - 1, rect.bottom), 2)
        
        # 7. Selection glow (enhanced for selected cells)
        if is_selected:
            # Multiple layers of glow
            for i in range(3):
                glow_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
                glow_alpha = 80 - (i * 20)
                glow_surf.fill((0, 255, 255, glow_alpha))
                self.screen.blit(glow_surf, rect.topleft)
            
            # Bright outline for selected cell
            pygame.draw.rect(self.screen, (0, 255, 255), rect, 2)
