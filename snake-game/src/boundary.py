import pygame

class Boundary:
    def __init__(self, window_size, grid_size):
        self.window_size = window_size
        self.grid_size = grid_size
        self.grid_count = window_size // grid_size
        self.shrink_level = 0
        self.max_shrink_level = (self.grid_count // 2) - 2  # Çok fazla küçülmeyi engelle
        self.border_flash = False
        self.flash_counter = 0
        self.needs_update = False
        self.outside_color = (100, 0, 0)  # Dışarıda kalan alan için koyu kırmızı
        
        # Başlangıç sınır koordinatlarını tanımla (tam grid)
        self.update_boundaries()
    
    def update_boundaries(self):
        # Sol üst köşe
        self.min_x = 0 + self.shrink_level
        self.min_y = 0 + self.shrink_level
        
        # Sağ alt köşe (dahil)
        self.max_x = self.grid_count - 1 - self.shrink_level
        self.max_y = self.grid_count - 1 - self.shrink_level
        
        # Oynanabilir alanı güncelle
        self.playable_width = self.max_x - self.min_x + 1
        self.playable_height = self.max_y - self.min_y + 1
    
    def check_collision(self, position):
        """Verilen pozisyonun sınırlarla çarpışma kontrolünü yap"""
        x, y = position
        return (x < self.min_x or x > self.max_x or 
                y < self.min_y or y > self.max_y)
    
    def check_shrink(self, score):
        """Skora göre oyun alanının küçültülmesi gerekip gerekmediğini kontrol et"""
        should_shrink = score > 0 and score % 10 == 0 and self.shrink_level < self.max_shrink_level
        
        if should_shrink and not self.needs_update:
            self.needs_update = True
            return True
        return False
    
    def shrink(self):
        """Oyun alanını her kenardan bir grid hücresi küçült"""
        if self.shrink_level < self.max_shrink_level:
            self.shrink_level += 1
            self.update_boundaries()
            self.border_flash = True
            self.flash_counter = 0
            self.needs_update = False
            return True
        return False
    
    def reset(self):
        """Sınırları başlangıç boyutuna sıfırla"""
        self.shrink_level = 0
        self.update_boundaries()
        self.border_flash = False
        self.flash_counter = 0
        self.needs_update = False
    
    def draw(self, screen):
        """Sınırları dış alanı farklı bir renkle doldurarak çiz"""
        # Sadece tam oyun alanını kullanmıyorsak veya yanıp sönüyorsa çiz
        if self.shrink_level > 0 or self.border_flash:
            # Sınır rengini belirle (yeni küçüldüğünde yanıp sönen efekt)
            outside_color = self.outside_color
            border_color = (255, 0, 0)  # Varsayılan kırmızı
            
            # Yanıp sönme durumunda, her birkaç karede bir görünür ve görünmez arasında geçiş yap
            if self.border_flash:
                self.flash_counter += 1
                flash_intensity = abs(((self.flash_counter % 20) - 10) / 10)  # Nabız efekti oluşturur
                
                # Normal dış renk ve parlak kırmızı arasında interpolasyon yap
                r = int(self.outside_color[0] + (255 - self.outside_color[0]) * flash_intensity)
                g = int(self.outside_color[1] * (1 - flash_intensity))
                b = int(self.outside_color[2] * (1 - flash_intensity))
                
                outside_color = (r, g, b)
                
                # Kısa bir süre sonra yanıp sönmeyi durdur
                if self.flash_counter > 60:  # 60 FPS'te yaklaşık 1 saniye
                    self.border_flash = False
            
            # Dış alanları, dış renk ile doldurulmuş dikdörtgenler olarak çiz
            
            # Üst alan (köşeler dahil)
            if self.min_y > 0:
                pygame.draw.rect(screen, outside_color, 
                                (0, 0, 
                                 self.window_size, 
                                 self.min_y * self.grid_size))
            
            # Alt alan (köşeler dahil)
            if self.max_y < self.grid_count - 1:
                pygame.draw.rect(screen, outside_color, 
                                (0, (self.max_y + 1) * self.grid_size, 
                                 self.window_size, 
                                 (self.grid_count - self.max_y - 1) * self.grid_size))
            
            # Sol alan (zaten çizilmiş köşeler hariç)
            if self.min_x > 0:
                pygame.draw.rect(screen, outside_color, 
                                (0, self.min_y * self.grid_size, 
                                 self.min_x * self.grid_size, 
                                 (self.max_y - self.min_y + 1) * self.grid_size))
            
            # Sağ alan (zaten çizilmiş köşeler hariç)
            if self.max_x < self.grid_count - 1:
                pygame.draw.rect(screen, outside_color, 
                                ((self.max_x + 1) * self.grid_size, self.min_y * self.grid_size, 
                                 (self.grid_count - self.max_x - 1) * self.grid_size, 
                                 (self.max_y - self.min_y + 1) * self.grid_size))
            
            # Sınır kenarında ince kırmızı çizgi çiz
            pygame.draw.rect(screen, border_color, 
                            (self.min_x * self.grid_size, 
                             self.min_y * self.grid_size, 
                             (self.max_x - self.min_x + 1) * self.grid_size, 
                             (self.max_y - self.min_y + 1) * self.grid_size), 
                             2)  # 2 piksel kalınlığında sınır 