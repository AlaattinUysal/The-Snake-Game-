import pygame
import random

# Renk Sabitleri
WALL_COLOR = (139, 69, 19)  # Kahverengi duvar
WALL_BORDER = (90, 40, 10)  # Daha koyu kahverengi kenar
GRID_SIZE = 20

class Obstacles:
    def __init__(self, window_size):
        self.grid_count = window_size // GRID_SIZE
        self.obstacles = []  # Engellerin pozisyonlarını saklayacak liste
        self.window_size = window_size
        self.last_score_milestone = 0  # Son engel eklenen skor
    
    def generate_obstacle_position(self, snake_body, food_positions, boundary=None):
        """Snake ve yiyeceklerle çakişmayan yeni bir engel pozisyonu oluştur"""
        all_occupied = snake_body + food_positions + self.obstacles
        
        # Eğer sınır varsa, sınır içinde rastgele pozisyon üret
        if boundary:
            min_x, max_x = boundary.min_x, boundary.max_x
            min_y, max_y = boundary.min_y, boundary.max_y
        else:
            # Sınır yoksa tam grid'i kullan
            min_x, max_x = 0, self.grid_count - 1
            min_y, max_y = 0, self.grid_count - 1
            
        new_position = (random.randint(min_x, max_x),
                       random.randint(min_y, max_y))
                      
        # Yeni pozisyon çakışmıyor mu kontrol et
        attempts = 0
        while new_position in all_occupied and attempts < 100:
            new_position = (random.randint(min_x, max_x),
                           random.randint(min_y, max_y))
            attempts += 1
            
        # Eğer 100 denemede bulamazsak, boş bir pozisyon bulana kadar adım adım ilerle
        if attempts >= 100:
            for x in range(min_x, max_x + 1):
                for y in range(min_y, max_y + 1):
                    pos = (x, y)
                    if pos not in all_occupied:
                        return pos
                        
        return new_position
    
    def get_obstacle_pattern(self, start_pos, pattern_type, boundary=None):
        """Belirli bir baslangic noktasından 3'lü engel deseni oluştur"""
        x, y = start_pos
        
        # Desen türüne göre 3'lü engel koordinatlarını hesapla
        if pattern_type == 0:  # Yatay sıra (yan yana)
            return [(x, y), (x+1, y), (x+2, y)]
        elif pattern_type == 1:  # Dikey sıra (alt alta)
            return [(x, y), (x, y+1), (x, y+2)]
        elif pattern_type == 2:  # Sağ çapraz aşağı
            return [(x, y), (x+1, y+1), (x+2, y+2)]
        elif pattern_type == 3:  # Sol çapraz aşağı
            return [(x, y), (x-1, y+1), (x-2, y+2)]
        elif pattern_type == 4:  # L şekli
            return [(x, y), (x, y+1), (x+1, y+1)]
        elif pattern_type == 5:  # Ters L şekli
            return [(x, y), (x, y+1), (x-1, y+1)]
    
    def is_valid_pattern(self, pattern, snake_body, food_positions, boundary=None):
        """Oluşturulan desenin geçerli olup olmadığını kontrol et"""
        # Tüm engellerin ekran içinde olduğunu kontrol et
        for pos in pattern:
            x, y = pos
            
            # Eğer sınır varsa, sınır içinde olduğunu kontrol et
            if boundary:
                if boundary.check_collision(pos):
                    return False
            else:
                # Yoksa ekran sınırlarını kontrol et
                if x < 0 or x >= self.grid_count or y < 0 or y >= self.grid_count:
                    return False
        
        # Engellerin yılan veya yiyeceklerle çakışmadığını kontrol et
        all_occupied = snake_body + food_positions + self.obstacles
        for pos in pattern:
            if pos in all_occupied:
                return False
                
        return True
    
    def add_obstacles(self, score, snake_body, food_positions, boundary=None):
        """Belirli skor artışlarında yeni engel desenleri ekle"""
        # Her 5 puanda bir yeni engeller eklenir
        current_milestone = score // 5
        
        if current_milestone > self.last_score_milestone:
            self.last_score_milestone = current_milestone
            
            # Rastgele bir desen türü seç (0-5 arası)
            pattern_type = random.randint(0, 5)
            
            # Geçerli bir desen bulana kadar dene
            max_attempts = 100
            attempts = 0
            
            while attempts < max_attempts:
                # Rastgele bir başlangıç pozisyonu al
                start_pos = self.generate_obstacle_position(snake_body, food_positions, boundary)
                
                # Bu pozisyondan itibaren desen oluştur
                pattern = self.get_obstacle_pattern(start_pos, pattern_type, boundary)
                
                # Desen geçerli mi kontrol et
                if self.is_valid_pattern(pattern, snake_body, food_positions, boundary):
                    # Desendeki tüm pozisyonları engel listesine ekle
                    for pos in pattern:
                        if pos not in self.obstacles:  # Tekrarları önle
                            self.obstacles.append(pos)
                    break
                
                attempts += 1
                
                # Eğer çok deneme yapıldıysa desen türünü değiştir
                if attempts % 20 == 0:
                    pattern_type = (pattern_type + 1) % 6
    
    def update_obstacles_for_boundary(self, boundary):
        """Sınır değiştiğinde engelleri güncelle ve sınır dışında kalanları kaldır"""
        if not boundary:
            return
            
        # Sınır dışında kalan engelleri listeden çıkar
        updated_obstacles = []
        for pos in self.obstacles:
            if not boundary.check_collision(pos):
                updated_obstacles.append(pos)
        
        # Engelleri güncelle
        self.obstacles = updated_obstacles
    
    def check_collision(self, position):
        """Belirli bir pozisyonun engellerle çakışıp çakışmadığını kontrol et"""
        return position in self.obstacles
    
    def draw(self, screen):
        """Tüm engelleri çiz"""
        for pos in self.obstacles:
            x = pos[0] * GRID_SIZE
            y = pos[1] * GRID_SIZE
            
            # Duvar bloğu çiz (kahverengi dikdörtgen)
            wall_rect = pygame.Rect(x + 1, y + 1, GRID_SIZE - 2, GRID_SIZE - 2)
            pygame.draw.rect(screen, WALL_COLOR, wall_rect)
            
            # Duvar bloğunun kenarlarını çiz
            pygame.draw.rect(screen, WALL_BORDER, wall_rect, 2)
            
            # Duvar dokusu ekle (küçük noktalar)
            for i in range(3):
                for j in range(3):
                    dot_x = x + 5 + i * 5
                    dot_y = y + 5 + j * 5
                    dot_size = 1 if (i + j) % 2 == 0 else 2
                    pygame.draw.circle(screen, WALL_BORDER, (dot_x, dot_y), dot_size)
    
    def reset(self):
        """Tüm engelleri temizle"""
        self.obstacles = []
        self.last_score_milestone = 0 