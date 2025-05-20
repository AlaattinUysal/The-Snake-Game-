import pygame

# Sabitler
MOVE_DISTANCE = 20
GRID_SIZE = 20

# Renkler
HEAD_COLOR = (0, 0, 0)  # Siyah (baş için)
BODY_COLOR = (40, 40, 40)  # Koyu gri (gövde için)
WALL_PASS_COLOR = (255, 215, 0)  # Altın rengi (duvar geçişi etkinken)

class Snake:
    def __init__(self, window_size):
        self.grid_count = window_size // GRID_SIZE
        # Başlangıçta 3 kare uzunluğunda yılan oluştur
        center = self.grid_count // 2
        self.body = [
            (center, center),         # Baş
            (center - 1, center),     # Gövde
            (center - 2, center)      # Kuyruk
        ]
        self.direction = [1, 0]  # Başlangıç yönü: sağ
        self.pending_direction = None  # Bekleyen yön değişikliği
        self.grow = False
        self.head = self.body[0]
        self.dead = False
        
        # Duvar geçiş özelliği için değişkenler
        self.wall_pass_active = False  # Duvar geçişi başlangıçta kapalı
        self.wall_pass_timer = 0       # Duvar geçişi süresi sayacı
        self.wall_pass_duration = 105  # 105 kare sürecek (7 saniye - 15 FPS'de)
        self.glow_effect = 0           # Parıldama efekti için sayaç

    def move(self):
        if self.dead:
            return
        
        # Eğer bekleyen bir yön değişikliği varsa ve geçerli ise uygula
        if self.pending_direction is not None:
            # Zıt yöne dönüş kontrolü
            if not ((self.pending_direction[0] == -self.direction[0] and self.pending_direction[1] == -self.direction[1])):
                self.direction = self.pending_direction
            self.pending_direction = None
            
        head = self.body[0]
        new_head = (
            (head[0] + self.direction[0]),
            (head[1] + self.direction[1])
        )
        
        # Duvar geçişi etkinse, karşı duvardan çık
        if self.wall_pass_active and self.wall_pass_timer > 0:
            # Duvar geçişi süresini azalt
            self.wall_pass_timer -= 1
            
            # Süre bittiyse duvar geçişini kapat
            if self.wall_pass_timer <= 0:
                self.wall_pass_active = False
            
            # Parıldama efekti için sayacı güncelle
            self.glow_effect = (self.glow_effect + 1) % 20
            
            # Ekran kenarlarında geçiş yap
            new_x, new_y = new_head
            if new_x < 0:
                new_x = self.grid_count - 1
            elif new_x >= self.grid_count:
                new_x = 0
            
            if new_y < 0:
                new_y = self.grid_count - 1
            elif new_y >= self.grid_count:
                new_y = 0
                
            new_head = (new_x, new_y)
        
        # Kendine çarpma kontrolü    
        if new_head in self.body:
            self.dead = True
            return
            
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
            
        self.body.insert(0, new_head)
        self.head = self.body[0]

    def extend(self):
        self.grow = True
        
    def activate_wall_pass(self):
        """Duvar geçişi özelliğini etkinleştir"""
        self.wall_pass_active = True
        self.wall_pass_timer = self.wall_pass_duration

    def up(self):
        # Aşağı gidiyorsa yukarı dönemez
        if self.direction != [0, 1]:
            self.pending_direction = [0, -1]
            
    def down(self):
        # Yukarı gidiyorsa aşağı dönemez
        if self.direction != [0, -1]:
            self.pending_direction = [0, 1]
            
    def left(self):
        # Sağa gidiyorsa sola dönemez
        if self.direction != [1, 0]:
            self.pending_direction = [-1, 0]
            
    def right(self):
        # Sola gidiyorsa sağa dönemez
        if self.direction != [-1, 0]:
            self.pending_direction = [1, 0]
            
    def draw(self, screen):
        for i, segment in enumerate(self.body):
            snake_rect = pygame.Rect(
                segment[0] * GRID_SIZE + 1,  # 1 pixel offset
                segment[1] * GRID_SIZE + 1,
                GRID_SIZE - 2,  # Kenarlardan 1 pixel boşluk bırak
                GRID_SIZE - 2
            )
            
            # Duvar geçişi aktifse, yılanı altın renginde göster (parıldama efekti ile)
            if self.wall_pass_active and i == 0:  # Sadece başı altın renk olsun
                # Parıldama efekti için rengi değiştir
                glow_intensity = abs(((self.glow_effect % 20) - 10) / 10)  # 0 ile 1 arasında salınım
                
                # Ana renk ile parlak sarı arasında geçiş
                r = int(255)  # Altın sarısı
                g = int(215 * (0.7 + 0.3 * glow_intensity))  # Parıldama
                b = int(0 + 128 * glow_intensity)  # Parlak efekt
                
                head_color = (r, g, b)
                pygame.draw.rect(screen, head_color, snake_rect, border_radius=5)
                
                # Işık efekti için çember çiz
                glow_size = int(4 + 2 * glow_intensity)
                glow_center = (segment[0] * GRID_SIZE + GRID_SIZE // 2, 
                              segment[1] * GRID_SIZE + GRID_SIZE // 2)
                glow_color = (255, 255, 100, int(150 * glow_intensity))
                
                # Işık çemberi için yeni surface
                glow_surface = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
                pygame.draw.circle(glow_surface, glow_color, (glow_size, glow_size), glow_size)
                screen.blit(glow_surface, (glow_center[0] - glow_size, glow_center[1] - glow_size))
            else:
                # Baş için tam siyah, gövde için koyu gri
                color = HEAD_COLOR if i == 0 else BODY_COLOR
                pygame.draw.rect(screen, color, snake_rect, border_radius=5)
