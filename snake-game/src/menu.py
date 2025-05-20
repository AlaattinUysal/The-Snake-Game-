import pygame
import os
import sys
import random

# Renk Sabitleri
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)  # Orman yeşili
DARK_GREEN = (0, 100, 0)  # Koyu yeşil
BLACK = (0, 0, 0)
BUTTON_COLOR = (34, 139, 34)  # Buton rengi - arka planla uyumlu
BUTTON_HOVER_COLOR = (50, 168, 82)  # Buton üzerine gelindiğinde renk
BUTTON_BORDER_COLOR = WHITE  # Buton kenar rengi - beyaz

class Button:
    def __init__(self, x, y, width, height, text, font_size=32):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.SysFont("Arial", font_size, bold=True)
        self.color = BUTTON_COLOR
        self.hover_color = BUTTON_HOVER_COLOR
        self.border_color = BUTTON_BORDER_COLOR
        self.text_color = WHITE
        self.shadow_color = (0, 0, 0)
        self.is_hovered = False
        
        # Gölge efekti için
        self.shadow_offset = 6  # Daha belirgin gölge
        self.shadow_rect = pygame.Rect(
            self.rect.x + self.shadow_offset,
            self.rect.y + self.shadow_offset,
            self.rect.width,
            self.rect.height
        )
    
    def draw(self, screen):
        # Buton gölgesini çiz
        pygame.draw.rect(screen, self.shadow_color, self.shadow_rect, border_radius=12)
        
        # Buton arka planını çiz
        pygame.draw.rect(screen, self.hover_color if self.is_hovered else self.color, self.rect, border_radius=12)
        
        # Buton kenarını çiz - kalın beyaz çerçeve
        pygame.draw.rect(screen, self.border_color, self.rect, width=3, border_radius=12)
        
        # İkinci iç çerçeve (daha ince) - derinlik hissi için
        inner_rect = pygame.Rect(
            self.rect.x + 3,
            self.rect.y + 3,
            self.rect.width - 6,
            self.rect.height - 6
        )
        pygame.draw.rect(screen, self.hover_color if self.is_hovered else self.color, inner_rect, width=1, border_radius=9)
        
        # Buton metnini çiz - önce gölge
        text_shadow = self.font.render(self.text, True, self.shadow_color)
        text_shadow_rect = text_shadow.get_rect(center=(self.rect.center[0] + 3, self.rect.center[1] + 3))
        screen.blit(text_shadow, text_shadow_rect)
        
        # Sonra normal metin
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def check_hover(self, pos):
        # Fare butonun üzerindeyken buton rengini ve gölge ofsetini değiştir
        was_hovered = self.is_hovered
        self.is_hovered = self.rect.collidepoint(pos)
        
        # Buton hover durumu değiştiğinde gölgeyi güncelle
        if was_hovered != self.is_hovered:
            offset = 4 if self.is_hovered else 6  # Buton üzerine gelindiğinde gölge azalır (basılmış gibi)
            self.shadow_rect = pygame.Rect(
                self.rect.x + offset,
                self.rect.y + offset,
                self.rect.width,
                self.rect.height
            )
        
        return self.is_hovered
    
    def is_clicked(self, pos, clicked):
        return self.rect.collidepoint(pos) and clicked

class Menu:
    def __init__(self, window_size, score=None):
        self.window_size = window_size
        self.score = score  # Skor değişkeni eklendi
        
        # Başlık için font
        pygame.font.init()
        try:
            # Emoji destekli font kullan
            self.title_font = pygame.font.SysFont("Segoe UI Emoji", 72, bold=False)
        except:
            # Segoe UI Emoji bulunamazsa alternatif fontlar dene
            try:
                self.title_font = pygame.font.SysFont("Arial Unicode MS", 72, bold=False)
            except:
                try:
                    self.title_font = pygame.font.SysFont("Arial", 72, bold=True)
                except:
                    # En son çare olarak varsayılan font kullan
                    self.title_font = pygame.font.Font(None, 72)
        
        # Skor fontu
        self.score_font = pygame.font.SysFont("Arial", 28, bold=True)
        
        # Butonları oluştur - daha büyük boyutta
        button_width, button_height = 260, 70
        button_x = window_size // 2 - button_width // 2
        
        # Play butonu ekranın ortasında
        play_y = window_size // 2 - 50
        self.play_button = Button(button_x, play_y, button_width, button_height, "Oyna")
        
        # Scoreboard butonu Play butonunun altında
        scoreboard_y = play_y + button_height + 40
        self.scoreboard_button = Button(button_x, scoreboard_y, button_width, button_height, "Skor Tablosu")
        
        # Arka plan resmi
        self.background_image = self.load_background_image()

    def load_background_image(self):
        # Belirtilen özel arka plan resmini yükle
        custom_bg_path = r"C:\Users\OMEN\Desktop\CURSOR\SideProjects\snake-game\images\menu_arka_plan\snake_background.png"
        
        if os.path.exists(custom_bg_path):
            try:
                return pygame.image.load(custom_bg_path)
            except:
                pass
                
        # Eğer özel arka plan yüklenemezse, alternatif olarak nature_1 ya da nature_2 kullan
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        images_dir = os.path.join(base_dir, "images")
        
        # Nature 1 büyük arka plan (yedek)
        nature1_path = os.path.join(images_dir, "nature_1", "origbig.png")
        if os.path.exists(nature1_path):
            try:
                return pygame.image.load(nature1_path)
            except:
                pass
        
        return None

    def draw_background(self, screen):
        # Arka plan resmini çiz
        if self.background_image:
            # Resmi ekran boyutuna ölçekle
            scaled_bg = pygame.transform.scale(self.background_image, (self.window_size, self.window_size))
            screen.blit(scaled_bg, (0, 0))
        else:
            # Eğer arka plan resmi yoksa yedek olarak yeşil arka planı kullan
            screen.fill(GREEN)
            
            # Daha koyu yeşil grid çizgileri çiz
            for x in range(0, self.window_size, 20):
                pygame.draw.line(screen, DARK_GREEN, (x, 0), (x, self.window_size))
            for y in range(0, self.window_size, 20):
                pygame.draw.line(screen, DARK_GREEN, (0, y), (self.window_size, y))

    def draw_title(self, screen):
        # Kahverengi kenarlığa uygun başlık paneli
        panel_width = 400  # Daha dar panel
        panel_height = 80  # Daha kısa panel
        title_panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        title_panel.fill((0, 0, 0, 170))  # Biraz daha koyu
        
        # Paneli ekrana yerleştir - kahverengi kutucuk üzerine
        panel_x = self.window_size // 2 - panel_width // 2
        panel_y = 15  # Yukarıda konumlandır
        screen.blit(title_panel, (panel_x, panel_y))
        
        # Başlık metni - daha küçük font
        self.title_font = pygame.font.SysFont("Segoe UI Emoji", 56, bold=False)  # Font boyutunu küçült
        title_text = "THE SNAKE 🐍"
        
        # Önce gölgeyi çiz - daha belirgin gölge
        title_shadow = self.title_font.render(title_text, True, (0, 0, 0))
        shadow_rect = title_shadow.get_rect(center=(self.window_size // 2 + 3, panel_y + panel_height // 2 + 3))
        screen.blit(title_shadow, shadow_rect)
        
        # Sonra esas metni çiz
        title_surface = self.title_font.render(title_text, True, WHITE)
        title_rect = title_surface.get_rect(center=(self.window_size // 2, panel_y + panel_height // 2))
        screen.blit(title_surface, title_rect)

    def draw(self, screen):
        # Arka planı çiz
        self.draw_background(screen)
        
        # Başlığı çiz
        self.draw_title(screen)
        
        # Skoru çiz (eğer varsa)
        if self.score is not None:
            # Skor paneli için yarı-saydam arka plan
            panel_width = 200
            panel_height = 40
            panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
            panel_surface.fill((0, 0, 0, 170))  # Siyah, yarı-saydam
            
            # Paneli ekranın üst kısmına yerleştir
            panel_x = self.window_size // 2 - panel_width // 2
            panel_y = 100  # Başlığın altında
            screen.blit(panel_surface, (panel_x, panel_y))
            
            # Skor metnini hazırla
            score_text = self.score_font.render(f"Mevcut Skor: {self.score.score}", True, WHITE)
            score_rect = score_text.get_rect(center=(self.window_size // 2, panel_y + panel_height // 2))
            
            # Skoru çiz
            screen.blit(score_text, score_rect)
        
        # Butonları doğrudan arka plan üzerine çiz
        self.play_button.draw(screen)
        self.scoreboard_button.draw(screen)
    
    def update(self, events):
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_clicked = True
        
        # Butonları güncelle
        self.play_button.check_hover(mouse_pos)
        self.scoreboard_button.check_hover(mouse_pos)
        
        # Buton tıklamalarını kontrol et
        if self.play_button.is_clicked(mouse_pos, mouse_clicked):
            return "play"
        elif self.scoreboard_button.is_clicked(mouse_pos, mouse_clicked):
            return "scoreboard"
            
        return None 