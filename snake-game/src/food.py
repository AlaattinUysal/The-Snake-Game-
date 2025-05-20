import pygame
import random
import math

# Renk Sabitleri
RED = (255, 0, 0)  # Elma kırmızısı
DARK_RED = (139, 0, 0)  # Koyu kırmızı (gölge için)
GREEN = (0, 100, 0)  # Yaprak için
GOLD = (255, 215, 0)  # Altın rengi
DARK_GOLD = (184, 134, 11)  # Koyu altın rengi (gölge için)
GRID_SIZE = 20

# Meyve türleri
APPLE = 0
CHERRY = 1
WATERMELON = 2
MELON = 3
GOLDEN_APPLE = 4  # Altın elma türü

class Food:
    def __init__(self, window_size):
        self.grid_count = window_size // GRID_SIZE
        self.position = self.generate_position()
        self.food_type = APPLE  # Ana yiyecek her zaman elma
        self.food_value = 1  # Elmanın puan değeri
        
        # Meyve resimleri
        self.food_images = {
            APPLE: self.create_apple(),
            CHERRY: self.create_cherry(),
            WATERMELON: self.create_watermelon(),
            MELON: self.create_melon(),
            GOLDEN_APPLE: self.create_golden_apple()  # Altın elma görseli
        }
        
        self.food_image = self.food_images[self.food_type]
        self.eat_effect_timer = 0
        self.eat_effect_duration = 10  # 10 frame sürecek efekt
        self.eating_position = None
        self.window_size = window_size
        self.score = 0  # Toplam skoru takip etmek için
        
        # Ekstra yiyecekler için değişkenler
        self.extra_foods = []  # (pozisyon, tür, değer) tuple'larını saklayacak
        self.max_extra_foods = 3  # Maksimum ekstra yiyecek sayısı
        
        # Altın elma değişkenleri
        self.golden_apple_active = False  # Altın elma aktif mi?
        self.golden_apple_position = None  # Altın elma pozisyonu
        self.golden_apple_spawn_chance = 20  # Her yemek yendikten sonra %20 ihtimalle çıksın
        self.golden_apple_timer = 0  # Altın elmanın aktif kalma süresi
        self.golden_apple_duration = 150  # 10 saniye (15 FPS'de)
        self.golden_apple_flash = 0  # Yanıp sönme efekti için sayaç
        
    def create_golden_apple(self):
        # Altın elma için yeni bir surface oluştur (şeffaf arka plan ile)
        surface = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
        
        # Elmanın merkezi
        center_x = GRID_SIZE // 2
        center_y = GRID_SIZE // 2
        radius = (GRID_SIZE - 4) // 2  # Elmanın yarıçapı
        
        # Ana elma şekli (altın renkli daire)
        pygame.draw.circle(surface, GOLD, (center_x, center_y), radius)
        
        # Gölge efekti (sol alt kısım)
        shadow_rect = pygame.Rect(center_x - radius, center_y, radius, radius)
        pygame.draw.ellipse(surface, DARK_GOLD, shadow_rect)
        
        # Yaprak (yeşil üçgen)
        leaf_points = [
            (center_x, center_y - radius),  # Üst
            (center_x - 2, center_y - radius - 2),  # Sol
            (center_x + 2, center_y - radius - 2)   # Sağ
        ]
        pygame.draw.polygon(surface, GREEN, leaf_points)
        
        # Sap (yeşil çizgi)
        pygame.draw.line(surface, GREEN, 
                        (center_x, center_y - radius),
                        (center_x, center_y - radius - 3), 2)
        
        # Altın elma parıltısı (küçük beyaz noktalar)
        for _ in range(5):
            angle = random.random() * 2 * math.pi
            shine_dist = random.randint(1, radius - 1)
            shine_x = center_x + int(shine_dist * math.cos(angle))
            shine_y = center_y + int(shine_dist * math.sin(angle))
            shine_size = random.randint(1, 2)
            pygame.draw.circle(surface, (255, 255, 255), (shine_x, shine_y), shine_size)
        
        return surface
        
    def create_apple(self):
        # Elma için yeni bir surface oluştur (şeffaf arka plan ile)
        surface = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
        
        # Elmanın merkezi
        center_x = GRID_SIZE // 2
        center_y = GRID_SIZE // 2
        radius = (GRID_SIZE - 4) // 2  # Elmanın yarıçapı
        
        # Ana elma şekli (kırmızı daire)
        pygame.draw.circle(surface, RED, (center_x, center_y), radius)
        
        # Gölge efekti (sol alt kısım)
        shadow_rect = pygame.Rect(center_x - radius, center_y, radius, radius)
        pygame.draw.ellipse(surface, DARK_RED, shadow_rect)
        
        # Yaprak (yeşil üçgen)
        leaf_points = [
            (center_x, center_y - radius),  # Üst
            (center_x - 2, center_y - radius - 2),  # Sol
            (center_x + 2, center_y - radius - 2)   # Sağ
        ]
        pygame.draw.polygon(surface, GREEN, leaf_points)
        
        # Sap (yeşil çizgi)
        pygame.draw.line(surface, GREEN, 
                        (center_x, center_y - radius),
                        (center_x, center_y - radius - 3), 2)
        
        return surface
        
    def create_cherry(self):
        # Kiraz için surface oluştur
        surface = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
        
        # Kirazın merkezi
        center_x = GRID_SIZE // 2
        center_y = GRID_SIZE // 2 + 2  # Biraz aşağıda
        
        # İki kiraz tanesi oluştur (kırmızı daireler)
        pygame.draw.circle(surface, (220, 20, 60), (center_x - 3, center_y), 5)  # Sol kiraz
        pygame.draw.circle(surface, (180, 0, 40), (center_x - 3, center_y), 5, 1)  # Gölge
        
        pygame.draw.circle(surface, (220, 20, 60), (center_x + 3, center_y), 5)  # Sağ kiraz
        pygame.draw.circle(surface, (180, 0, 40), (center_x + 3, center_y), 5, 1)  # Gölge
        
        # Sap (yeşil çizgi)
        pygame.draw.line(surface, GREEN, 
                        (center_x - 3, center_y - 5),
                        (center_x, center_y - 10), 1)
        pygame.draw.line(surface, GREEN, 
                        (center_x + 3, center_y - 5),
                        (center_x, center_y - 10), 1)
        pygame.draw.line(surface, GREEN, 
                        (center_x, center_y - 10),
                        (center_x, center_y - 14), 1)
        
        return surface
        
    def create_watermelon(self):
        # Karpuz için surface oluştur (daha detaylı çizim)
        surface = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
        
        # Karpuzun merkezi
        center_x = GRID_SIZE // 2
        center_y = GRID_SIZE // 2
        
        # Karpuz oval şekli (büyük yeşil oval)
        watermelon_rect = pygame.Rect(2, 4, 16, 14)
        pygame.draw.ellipse(surface, (30, 150, 50), watermelon_rect)  # Koyu yeşil dış kabuk
        
        # Daha açık yeşil desenler (çizgiler)
        for i in range(3):
            offset = 3 + i * 3
            pygame.draw.line(surface, (80, 200, 80), 
                          (offset, 5), 
                          (offset, 17), 1)
        
        # Karpuz dilimi kesik görünümü - iç kırmızı kısım
        inner_rect = pygame.Rect(4, 6, 12, 10)
        pygame.draw.ellipse(surface, (230, 50, 80), inner_rect)  # Parlak kırmızı
        
        # Karpuz çekirdekleri (siyah küçük oval noktalar)
        seeds = [
            (7, 8), (13, 8),     # Üst sıra
            (5, 11), (10, 11), (15, 11),  # Orta sıra
            (8, 14), (12, 14)     # Alt sıra
        ]
        
        for seed_pos in seeds:
            seed_rect = pygame.Rect(seed_pos[0], seed_pos[1], 2, 1)
            pygame.draw.ellipse(surface, (0, 0, 0), seed_rect)
        
        return surface
        
    def create_melon(self):
        # Kavun için surface oluştur
        surface = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
        
        # Kavunun merkezi ve boyutu
        center_x = GRID_SIZE // 2
        center_y = GRID_SIZE // 2
        
        # Kavun dış yeşil kısmı
        pygame.draw.circle(surface, (180, 210, 90), (center_x, center_y), 8)
        
        # Kavun içi açık yeşil
        pygame.draw.circle(surface, (220, 255, 180), (center_x, center_y), 6)
        
        # Kavun dilimleri
        for i in range(4):
            angle = i * math.pi / 4  # 45 derece açıyla
            end_x = center_x + int(8 * math.cos(angle))
            end_y = center_y + int(8 * math.sin(angle))
            pygame.draw.line(surface, (160, 190, 80),
                          (center_x, center_y),
                          (end_x, end_y),
                          1)
        
        # Kavun deseni (noktalar)
        for i in range(8):
            radius = random.randint(2, 5)
            angle = random.random() * 2 * math.pi
            dot_x = center_x + int(radius * math.cos(angle))
            dot_y = center_y + int(radius * math.sin(angle))
            pygame.draw.circle(surface, (200, 240, 160),
                             (dot_x, dot_y),
                             1)
        
        return surface
        
    def show_eat_effect(self, screen, position=None):
        # Yeme efekti başlat
        self.eat_effect_timer = self.eat_effect_duration
        self.eating_position = position if position else self.position
        
    def generate_position(self, snake_body=None, existing_positions=None, boundary=None, center=False):
        """Mevcut pozisyonlarla çakışmayan yeni bir pozisyon oluştur"""
        if existing_positions is None:
            existing_positions = []
            
        if snake_body is None:
            snake_body = []
            
        all_occupied = snake_body + existing_positions
        
        # Eğer bir sınır belirtilmişse, onun içinde pozisyon üret
        if boundary:
            min_x, max_x = boundary.min_x, boundary.max_x
            min_y, max_y = boundary.min_y, boundary.max_y
        else:
            # Sınır yoksa tam grid'i kullan
            min_x, max_x = 0, self.grid_count - 1
            min_y, max_y = 0, self.grid_count - 1
        
        # Eğer center=True ise, orta noktayı hesapla
        if center:
            center_x = (min_x + max_x) // 2
            center_y = (min_y + max_y) // 2
            new_position = (center_x, center_y)
            
            # Eğer orta nokta meşgulse, etrafında spiral şeklinde boş bir yer ara
            if new_position in all_occupied:
                dx = [0, 1, 0, -1]  # Sağ, aşağı, sol, yukarı için x değişimleri
                dy = [1, 0, -1, 0]  # Sağ, aşağı, sol, yukarı için y değişimleri
                x, y = center_x, center_y
                step = 1
                direction = 0
                
                while step <= max(max_x - min_x, max_y - min_y):
                    for _ in range(2):  # Her adımda iki yön
                        for _ in range(step):  # Her yönde step kadar hareket
                            x += dx[direction]
                            y += dy[direction]
                            
                            # Sınırlar içinde mi kontrol et
                            if min_x <= x <= max_x and min_y <= y <= max_y:
                                test_pos = (x, y)
                                if test_pos not in all_occupied:
                                    return test_pos
                                    
                        direction = (direction + 1) % 4
                    step += 1
            else:
                return new_position
        
        # Normal rastgele pozisyon oluştur
        attempts = 0
        max_attempts = 100
        
        while attempts < max_attempts:
            new_position = (random.randint(min_x, max_x),
                          random.randint(min_y, max_y))
            
            if new_position not in all_occupied:
                return new_position
                
            attempts += 1
        
        # Eğer rastgele pozisyon bulunamazsa, sistematik olarak boş yer ara
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                pos = (x, y)
                if pos not in all_occupied:
                    return pos
                    
        # Son çare: Merkeze en yakın boş pozisyonu bul
        center_x = (min_x + max_x) // 2
        center_y = (min_y + max_y) // 2
        min_distance = float('inf')
        best_position = None
        
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                pos = (x, y)
                if pos not in all_occupied:
                    distance = abs(x - center_x) + abs(y - center_y)  # Manhattan mesafesi
                    if distance < min_distance:
                        min_distance = distance
                        best_position = pos
        
        return best_position if best_position is not None else (center_x, center_y)
                
    def check_golden_apple_collision(self, head_position):
        """Yılanın başının altın elma ile çarpışma kontrolü"""
        if self.golden_apple_active and head_position == self.golden_apple_position:
            # Çarpışma var, altın elmayı deaktif et
            self.golden_apple_active = False
            self.golden_apple_position = None
            return True
        return False
        
    def try_spawn_golden_apple(self, snake_body, boundary=None, obstacles=None):
        """Belirli bir ihtimalle altın elma ortaya çıkar"""
        # Eğer zaten altın elma varsa, çıkma
        if self.golden_apple_active:
            return
            
        # Rastgele ihtimal kontrolü
        if random.randint(1, 100) <= self.golden_apple_spawn_chance:
            # Mevcut pozisyonları topla
            existing_positions = [self.position] + [pos for pos, _, _ in self.extra_foods] + snake_body
            
            # Engelleri de meşgul pozisyonlara ekle
            if obstacles:
                existing_positions.extend(obstacles.obstacles)
            
            # Yeni pozisyon oluştur
            new_pos = self.generate_position(snake_body, existing_positions, boundary)
            
            # Engellerle çakışma kontrolü
            if new_pos is not None and not (obstacles and obstacles.check_collision(new_pos)):
                self.golden_apple_active = True
                self.golden_apple_position = new_pos
                self.golden_apple_timer = self.golden_apple_duration  # Süreyi başlat
                self.golden_apple_flash = 0
        
    def update(self):
        """Her karede çağrılacak güncelleme fonksiyonu"""
        # Altın elma süresi kontrolü
        if self.golden_apple_active and self.golden_apple_timer > 0:
            self.golden_apple_timer -= 1
            
            # Yanıp sönme efekti için sayacı güncelle
            self.golden_apple_flash += 1
            
            # Süre bittiyse altın elmayı kaldır
            if self.golden_apple_timer <= 0:
                self.golden_apple_active = False
                self.golden_apple_position = None
                self.golden_apple_flash = 0
        
    def moving_food(self, snake_body=None, score=0, boundary=None, obstacles=None):
        """Ana yiyeceği (elmayı) yeniden konumlandır"""
        # Skoru kaydet
        self.score = score
        
        # Puanı kontrol et ve elmanın ortada çıkması gereken durum mu belirle
        # 9, 19, 29... gibi skorlarda elma ortada çıksın
        is_pre_shrink = (score + 1) % 10 == 0
        
        # Mevcut ekstra yiyecek pozisyonlarını al
        existing_positions = [pos for pos, _, _ in self.extra_foods]
        if self.golden_apple_active:
            existing_positions.append(self.golden_apple_position)
            
        # Engelleri de meşgul pozisyonlara ekle
        if obstacles:
            existing_positions.extend(obstacles.obstacles)
        
        # Yeni pozisyon oluşturmayı dene
        max_attempts = 3  # Maksimum deneme sayısı
        attempts = 0
        new_position = None
        
        while attempts < max_attempts and new_position is None:
            new_position = self.generate_position(snake_body, existing_positions, boundary, center=is_pre_shrink)
            if new_position is not None and not (boundary and boundary.check_collision(new_position)):
                # Engellerle çakışma kontrolü
                if not (obstacles and obstacles.check_collision(new_position)):
                    self.position = new_position
                    break
            attempts += 1
            
        # Eğer hala pozisyon bulunamadıysa, son çare olarak merkezi kullan
        if new_position is None:
            if boundary:
                center_x = (boundary.min_x + boundary.max_x) // 2
                center_y = (boundary.min_y + boundary.max_y) // 2
            else:
                center_x = center_y = self.grid_count // 2
            self.position = (center_x, center_y)
        
        # Puan 10'un katıysa ve maksimum ekstra yiyecek sayısına ulaşılmadıysa, ekstra yiyecek ekle
        if score > 0 and score % 10 == 0 and len(self.extra_foods) < self.max_extra_foods:
            self.add_extra_food(snake_body, boundary, obstacles)
            
        # Altın elma çıkarma ihtimali kontrol et
        self.try_spawn_golden_apple(snake_body, boundary, obstacles)
        
    def add_extra_food(self, snake_body, boundary=None, obstacles=None):
        """Ekstra bir yiyecek ekle - rastgele türde"""
        # Halihazırda mevcut olan pozisyonlar
        existing_positions = [self.position] + [pos for pos, _, _ in self.extra_foods]
        
        # Engelleri de meşgul pozisyonlara ekle
        if obstacles:
            existing_positions.extend(obstacles.obstacles)
        
        # Yeni pozisyon oluştur
        new_pos = self.generate_position(snake_body, existing_positions, boundary)
        
        # Engellerle çakışma kontrolü
        if obstacles and obstacles.check_collision(new_pos):
            return  # Eğer engelle çakışıyorsa ekstra yiyecek ekleme
        
        # Rastgele yiyecek türü seç (ana yiyecek elma değil)
        food_type = random.choice([CHERRY, WATERMELON, MELON])
        
        # Yiyecek değeri belirle
        if food_type == CHERRY:
            value = 2  # Kiraz: 2 puan
        elif food_type == WATERMELON:
            value = 5  # Karpuz: 5 puan
        else:  # MELON
            value = 3  # Kavun: 3 puan
            
        # Ekstra yiyecekler listesine ekle
        self.extra_foods.append((new_pos, food_type, value))
    
    def check_extra_food_collision(self, head_position):
        """Yılanın başının ekstra yiyeceklerle çarpışma kontrolü"""
        for i, (pos, food_type, value) in enumerate(self.extra_foods):
            if head_position == pos:
                # Çarpışma var, yiyeceği listeden çıkar ve değerini döndür
                self.extra_foods.pop(i)
                return True, food_type, value, pos
        return False, None, 0, None
        
    def draw(self, screen):
        # Ana yiyeceği (elma) çiz
        x = self.position[0] * GRID_SIZE
        y = self.position[1] * GRID_SIZE
        screen.blit(self.food_images[APPLE], (x, y))
        
        # Ekstra yiyecekleri çiz
        for pos, food_type, _ in self.extra_foods:
            x = pos[0] * GRID_SIZE
            y = pos[1] * GRID_SIZE
            screen.blit(self.food_images[food_type], (x, y))
        
        # Altın elma aktifse çiz
        if self.golden_apple_active and self.golden_apple_position:
            x = self.golden_apple_position[0] * GRID_SIZE
            y = self.golden_apple_position[1] * GRID_SIZE
            
            # Görünürlük için bayrak
            should_draw = True
            
            # Aşamaya göre yanıp sönme
            if self.golden_apple_timer > 90:
                # İlk aşamada sürekli göster
                should_draw = True
            elif self.golden_apple_timer > 45:
                # Orta aşamada yavaş yanıp sön
                should_draw = (self.golden_apple_flash % 24) < 16
            else:
                # Son aşamada hızlı yanıp sön
                should_draw = (self.golden_apple_flash % 16) < 8
                    
            # Ayrıca rastgele titreşim ekle - daha belirsiz yapacak
            if self.golden_apple_timer < 90 and random.randint(0, 100) < 5:  # %5 ihtimalle
                # Rastgele bir süre görünmez olsun
                should_draw = False
            elif self.golden_apple_timer < 45 and random.randint(0, 100) < 15:  # %15 ihtimalle
                # Son aşamada daha sık kaybolsun
                should_draw = False
            
            # Görünür olması gerekiyorsa çiz
            if should_draw:
                screen.blit(self.food_images[GOLDEN_APPLE], (x, y))
        
        # Yeme efektini göster
        if self.eat_effect_timer > 0:
            # Efekt için pozisyonu hesapla
            effect_x = self.eating_position[0] * GRID_SIZE
            effect_y = self.eating_position[1] * GRID_SIZE
            
            # Efekt büyüklüğü (zamanla büyüyen)
            effect_size = (self.eat_effect_duration - self.eat_effect_timer) * 3
            
            # Parçacık efekti (dağılan kırmızı noktalar)
            for _ in range(5):
                particle_x = effect_x + GRID_SIZE//2 + random.randint(-effect_size, effect_size)
                particle_y = effect_y + GRID_SIZE//2 + random.randint(-effect_size, effect_size)
                particle_size = random.randint(2, 5)
                
                # Ekranın dışına çıkmamasını sağla
                particle_x = max(0, min(particle_x, self.window_size - 1))
                particle_y = max(0, min(particle_y, self.window_size - 1))
                
                # Kırmızı parçacık çiz
                pygame.draw.circle(screen, RED, (particle_x, particle_y), particle_size)
            
            # Efekt sayacını azalt
            self.eat_effect_timer -= 1


