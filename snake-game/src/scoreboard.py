import pygame
import os
from menu import Menu

# Renk Sabitleri
WHITE = (255, 255, 255)  # Skor rengi

class Score:
    def __init__(self, window_size):
        self.score = 0
        self.window_size = window_size
        # Pygame fontu oluştur
        pygame.font.init()
        self.font = pygame.font.SysFont("Arial", 24, bold=True)
        # Yüksek skoru yükle
        self.high_score = self.load_high_score()
        
    def write_score(self, screen):
        score_text = self.font.render(f"Skor: {self.score}", True, WHITE)
        
        # Ekranın en üst kısmında ortada görüntüle
        text_rect = score_text.get_rect(center=(self.window_size // 2, 30))  # Daha yukarıda konumlandır
        
        screen.blit(score_text, text_rect)
        
    def game_over(self, screen):
        # Oyun sonunda yüksek skoru kontrol et ve kaydet
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()
        
        # Menü arka planını çiz
        menu = Menu(self.window_size)
        menu.draw_background(screen)
        
        # Başlığı çiz - menü başlığı ile aynı
        menu.draw_title(screen)
        
        # Font boyutlarını arttır
        game_over_font = pygame.font.SysFont("Arial", 46, bold=True)
        instruction_font = pygame.font.SysFont("Arial", 26, bold=True)
        score_font = pygame.font.SysFont("Arial", 34, bold=True)
        
        # Gölgeli metin için
        shadow_color = (0, 0, 0)  # Siyah gölge
        shadow_offset = 2
        
        # Gölgeli metinleri çiz - önce gölgeler
        game_over_shadow = game_over_font.render("OYUN BİTTİ", True, shadow_color)
        final_score_shadow = score_font.render(f"Son Skor: {self.score}", True, shadow_color)
        restart_shadow = instruction_font.render("Yeniden başlamak için SPACE tuşuna basın", True, shadow_color)
        
        # Gölge konumları
        go_rect = game_over_shadow.get_rect(center=(self.window_size // 2 + shadow_offset, self.window_size // 2 - 60 + shadow_offset))
        score_rect = final_score_shadow.get_rect(center=(self.window_size // 2 + shadow_offset, self.window_size // 2 - 10 + shadow_offset))
        restart_rect = restart_shadow.get_rect(center=(self.window_size // 2 + shadow_offset, self.window_size // 2 + 70 + shadow_offset))
        
        # Gölgeleri çiz
        screen.blit(game_over_shadow, go_rect)
        screen.blit(final_score_shadow, score_rect)
        screen.blit(restart_shadow, restart_rect)
        
        # Yüksek skor gölgesi (varsa)
        if self.score >= self.high_score:
            hs_shadow = score_font.render("Yeni Yüksek Skor!", True, shadow_color)
            hs_rect = hs_shadow.get_rect(center=(self.window_size // 2 + shadow_offset, self.window_size // 2 + 30 + shadow_offset))
            screen.blit(hs_shadow, hs_rect)
        
        # Normal metinleri çiz
        game_over_text = game_over_font.render("OYUN BİTTİ", True, WHITE)
        final_score = score_font.render(f"Son Skor: {self.score}", True, WHITE)
        restart_text = instruction_font.render("Yeniden başlamak için SPACE tuşuna basın", True, WHITE)
        
        # Normal konumlar
        screen.blit(game_over_text, game_over_text.get_rect(center=(self.window_size // 2, self.window_size // 2 - 60)))
        screen.blit(final_score, final_score.get_rect(center=(self.window_size // 2, self.window_size // 2 - 10)))
        screen.blit(restart_text, restart_text.get_rect(center=(self.window_size // 2, self.window_size // 2 + 70)))
        
        # Yüksek skor mesajı (varsa)
        if self.score >= self.high_score:
            new_high_score = score_font.render("Yeni Yüksek Skor!", True, WHITE)
            screen.blit(new_high_score, new_high_score.get_rect(center=(self.window_size // 2, self.window_size // 2 + 30)))
        
        pygame.display.flip()
        
    def increase_score(self, points=1):
        # Parametreli hale getirildi, varsayılan 1 puan
        self.score += points
        
    def save_high_score(self):
        # Yüksek skoru kaydet
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        high_score_file = os.path.join(base_dir, "high_score.txt")
        try:
            with open(high_score_file, "w") as file:
                file.write(str(self.high_score))
        except:
            pass  # Dosya yazılamadıysa sessizce devam et
            
    def load_high_score(self):
        # Yüksek skoru yükle
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        high_score_file = os.path.join(base_dir, "high_score.txt")
        try:
            if os.path.exists(high_score_file):
                with open(high_score_file, "r") as file:
                    return int(file.read().strip())
        except:
            pass  # Dosya okunamadıysa veya dönüştürülemezse varsayılan değeri döndür
        return 0

