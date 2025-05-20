import pygame
import sys
import os
from snake import Snake
from food import Food
from scoreboard import Score
from obstacles import Obstacles
from boundary import Boundary
from menu import Menu


# Pygame'i başlat
pygame.init()
pygame.mixer.init()  # Ses mikserini başlat

# Ses dosyaları için mutlak yolu al
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOUND_PATH = os.path.join(BASE_DIR, "sounds", "eat_apple.mp3")

# Sesleri yükle
eat_sound = pygame.mixer.Sound(SOUND_PATH)

# Sabitler
WINDOW_SIZE = 600
GRID_SIZE = 20
GRID_COUNT = WINDOW_SIZE // GRID_SIZE
FPS = 15  # Oyun hızı

# Renkler
GREEN = (34, 139, 34)  # Orman yeşili
DARK_GREEN = (0, 100, 0)  # Grid için koyu yeşil
RED = (255, 0, 0)  # Yemek rengi
BLACK = (0, 0, 0)  # Yılan rengi
WHITE = (255, 255, 255)  # Beyaz
GOLD = (255, 215, 0)  # Altın elma rengi

# Ekranı ayarla
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("THE SNAKE 🐍")  # Başlık güncellendi
clock = pygame.time.Clock()

# Oyun durumları
MENU = 0
PLAY = 1
SCOREBOARD = 2

def draw_game_title(screen):
    # Kahverengi kenarlığa uygun başlık paneli
    panel_width = 400  # Daha geniş panel
    panel_height = 60  # Daha yüksek panel
    title_panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
    title_panel.fill((0, 0, 0, 170))  # Biraz daha koyu
    
    # Paneli ekrana yerleştir - kahverengi kenarlık üzerine
    panel_x = WINDOW_SIZE // 2 - panel_width // 2
    panel_y = 15  # Daha aşağıda konumlandır
    screen.blit(title_panel, (panel_x, panel_y))
    
    # Başlık metni
    try:
        # Emoji destekli font kullan
        title_font = pygame.font.SysFont("Segoe UI Emoji", 32, bold=False)  # Daha büyük font
    except:
        # Segoe UI Emoji bulunamazsa alternatif fontlar dene
        try:
            title_font = pygame.font.SysFont("Arial Unicode MS", 32, bold=False)
        except:
            try:
                title_font = pygame.font.SysFont("Arial", 32, bold=True)
            except:
                # En son çare olarak varsayılan font kullan
                title_font = pygame.font.Font(None, 32)
    
    title_text = "THE SNAKE 🐍"
    
    # Önce gölgeyi çiz
    title_shadow = title_font.render(title_text, True, (0, 0, 0))
    shadow_rect = title_shadow.get_rect(center=(WINDOW_SIZE // 2 + 2, panel_y + panel_height // 2 + 2))
    screen.blit(title_shadow, shadow_rect)
    
    # Sonra esas metni çiz
    title_surface = title_font.render(title_text, True, WHITE)
    title_rect = title_surface.get_rect(center=(WINDOW_SIZE // 2, panel_y + panel_height // 2))
    screen.blit(title_surface, title_rect)

def draw_grid():
    # Yeşil çimen arka planı çiz
    screen.fill(GREEN)
    
    # Daha koyu yeşil grid çizgileri çiz
    for x in range(0, WINDOW_SIZE, GRID_SIZE):
        pygame.draw.line(screen, DARK_GREEN, (x, 0), (x, WINDOW_SIZE))
    for y in range(0, WINDOW_SIZE, GRID_SIZE):
        pygame.draw.line(screen, DARK_GREEN, (0, y), (WINDOW_SIZE, y))

def reset_game():
    # Oyunu baştan başlat
    snake = Snake(WINDOW_SIZE)
    food = Food(WINDOW_SIZE)
    score = Score(WINDOW_SIZE)
    obstacles = Obstacles(WINDOW_SIZE)
    boundary = Boundary(WINDOW_SIZE, GRID_SIZE)
    return snake, food, score, obstacles, boundary

def show_scoreboard(screen, score):
    # Menü nesnesi oluştur - yeni arka planı kullanacak
    menu = Menu(WINDOW_SIZE)
    
    # Arka plan resmi
    menu.draw_background(screen)
    
    # Başlığı çiz - menü başlığı ile aynı
    menu.draw_title(screen)
    
    # Font boyutlarını arttır
    font = pygame.font.SysFont("Arial", 40, bold=True)
    score_font = pygame.font.SysFont("Arial", 34, bold=True)
    
    # Skor metinleri - arka planla kontrast oluşturmak için gölgeli metin
    shadow_color = (0, 0, 0)  # Siyah gölge
    
    # Gölgeli skor metinleri
    # Önce gölgeleri çiz
    current_score_shadow = score_font.render(f"Mevcut Skor: {score.score}", True, shadow_color)
    high_score_shadow = score_font.render(f"En Yüksek Skor: {score.high_score}", True, shadow_color)
    back_shadow = pygame.font.SysFont("Arial", 26, bold=True).render("Menüye dönmek için ESC tuşuna basın", True, shadow_color)
    
    # Gölgeleri elemanlardan 2 piksel sağa/aşağıya yerleştir
    shadow_offset = 2
    screen.blit(current_score_shadow, (WINDOW_SIZE // 2 - current_score_shadow.get_width() // 2 + shadow_offset, 
                                      WINDOW_SIZE // 2 - 70 + shadow_offset))
    screen.blit(high_score_shadow, (WINDOW_SIZE // 2 - high_score_shadow.get_width() // 2 + shadow_offset, 
                                   WINDOW_SIZE // 2 - 20 + shadow_offset))
    screen.blit(back_shadow, (WINDOW_SIZE // 2 - back_shadow.get_width() // 2 + shadow_offset, 
                             WINDOW_SIZE // 2 + 30 + shadow_offset))
    
    # Sonra asıl metinleri çiz
    current_score = score_font.render(f"Mevcut Skor: {score.score}", True, (255, 255, 255))
    high_score = score_font.render(f"En Yüksek Skor: {score.high_score}", True, (255, 255, 255))
    back_text = pygame.font.SysFont("Arial", 26, bold=True).render("Menüye dönmek için ESC tuşuna basın", True, (255, 255, 255))
    
    # Elemanları ortalayarak yerleştir
    screen.blit(current_score, (WINDOW_SIZE // 2 - current_score.get_width() // 2, WINDOW_SIZE // 2 - 70))
    screen.blit(high_score, (WINDOW_SIZE // 2 - high_score.get_width() // 2, WINDOW_SIZE // 2 - 20))
    screen.blit(back_text, (WINDOW_SIZE // 2 - back_text.get_width() // 2, WINDOW_SIZE // 2 + 30))

def main():
    snake, food, score, obstacles, boundary = reset_game()
    game_is_paused = False
    
    # Menü oluştur - yeni arka planı kullanacak ve skoru aktar
    menu = Menu(WINDOW_SIZE, score)
    
    # Başlangıç oyun durumu
    game_state = MENU
    
    # Duvar geçişi zamanlayıcısı için değişkenler
    wall_pass_seconds_left = 0
    
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if game_state == PLAY:
                    if snake.dead and event.key == pygame.K_SPACE:
                        # Yeniden başlat
                        snake, food, score, obstacles, boundary = reset_game()
                    elif event.key == pygame.K_p:
                        # P tuşu ile oyunu duraklat/devam ettir
                        game_is_paused = not game_is_paused
                    elif event.key == pygame.K_ESCAPE:
                        # ESC tuşu ile menüye dön
                        game_state = MENU
                        # Menüyü güncelle - mevcut skoru aktar
                        menu = Menu(WINDOW_SIZE, score)
                    elif not snake.dead and not game_is_paused:
                        # Hareket kontrolü
                        if event.key in [pygame.K_UP, pygame.K_w]:
                            snake.up()
                        elif event.key in [pygame.K_DOWN, pygame.K_s]:
                            snake.down()
                        elif event.key in [pygame.K_LEFT, pygame.K_a]:
                            snake.left()
                        elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                            snake.right()
                elif game_state == SCOREBOARD:
                    if event.key == pygame.K_ESCAPE:
                        game_state = MENU
                        # Menüyü güncelle - mevcut skoru aktar
                        menu = Menu(WINDOW_SIZE, score)
        
        if game_state == MENU:
            # Menüyü işle ve çiz
            menu_action = menu.update(events)
            menu.draw(screen)
            
            # Menü butonlarını kontrol et
            if menu_action == "play":
                game_state = PLAY
                # Yeni oyun başlat
                snake, food, score, obstacles, boundary = reset_game()
                game_is_paused = False
            elif menu_action == "scoreboard":
                game_state = SCOREBOARD
                
        elif game_state == PLAY:
            if not snake.dead and not game_is_paused:
                # Yılanı hareket ettir
                snake.move()
                
                # Altın elma zamanlayıcısını güncelle
                food.update()
                
                # Altın elma çarpışma kontrolü
                if food.check_golden_apple_collision(snake.head):
                    # Altın elma yenildi, duvar geçiş özelliğini aktifleştir
                    snake.activate_wall_pass()
                    
                    # Yemek yeme sesi çal
                    eat_sound.play()
                    
                    # Duvar geçişi süresini takip et
                    wall_pass_seconds_left = snake.wall_pass_timer // 15  # FPS'e göre saniye hesapla
                    
                    # Yemek yeme efekti göster
                    food.show_eat_effect(screen, snake.head)
                
                # Sınır çarpışma kontrolü - duvar geçişi aktif değilse kontrol et
                if boundary.check_collision(snake.head) and not snake.wall_pass_active:
                    snake.dead = True
                
                # Engel çarpışma kontrolü - duvar geçişi olsa bile engellere çarpmayı kontrol et
                if obstacles.check_collision(snake.head):
                    snake.dead = True
                    
                # Ana yemek (elma) yeme kontrolü
                if snake.head == food.position:
                    # Elma standardı: 1 puan ekle
                    score.increase_score(1)
                    
                    # Her 10 puanda bir oyun alanını küçült
                    if boundary.check_shrink(score.score):
                        boundary.shrink()
                        
                        # Yiyecekleri ve engelleri sınırlar içinde tut
                        food_positions = [food.position] + [pos for pos, _, _ in food.extra_foods]
                        valid_food_positions = []
                        for pos in food_positions:
                            if not boundary.check_collision(pos):
                                valid_food_positions.append(pos)
                            else:
                                # Sınır dışındaki yiyecekleri yeniden konumlandır
                                food.moving_food(snake.body, score.score, boundary, obstacles)
                        
                        # Sınır dışındaki engelleri güncelle
                        obstacles.update_obstacles_for_boundary(boundary)
                    
                    # Engelleri kontrol et ve gerekirse ekle
                    food_positions = [food.position] + [pos for pos, _, _ in food.extra_foods]
                    obstacles.add_obstacles(score.score, snake.body, food_positions, boundary)
                    
                    # Yemeği yeniden konumlandır
                    food.moving_food(snake.body, score.score, boundary, obstacles)
                    
                    # Yılanı uzat
                    snake.extend()
                    
                    # Yemek yeme sesi çal
                    eat_sound.play()
                    
                    # Yemek yeme efekti göster
                    food.show_eat_effect(screen)
                
                # Ekstra yiyecek yeme kontrolü
                collision, food_type, value, position = food.check_extra_food_collision(snake.head)
                if collision:
                    # Ekstra yiyecek puanını ekle
                    score.increase_score(value)
                    
                    # Her 10 puanda bir oyun alanını küçült
                    if boundary.check_shrink(score.score):
                        boundary.shrink()
                        
                        # Sınır dışındaki engelleri güncelle
                        obstacles.update_obstacles_for_boundary(boundary)
                    
                    # Engelleri kontrol et ve gerekirse ekle
                    food_positions = [food.position] + [pos for pos, _, _ in food.extra_foods]
                    obstacles.add_obstacles(score.score, snake.body, food_positions, boundary)
                    
                    # Yılanı uzat
                    snake.extend()
                    
                    # Yemek yeme sesi çal
                    eat_sound.play()
                    
                    # Yemek yeme efekti göster (özel konumda)
                    food.show_eat_effect(screen, position)
            
            # Çizim işlemleri
            draw_grid()           # Önce arka plan grid'i çiz
            boundary.draw(screen) # Sonra sınırları çiz
            food.draw(screen)     # Ardından oyun öğelerini çiz
            snake.draw(screen)
            obstacles.draw(screen)
            
            # Skor gösterimi
            score.write_score(screen)
            
            # Duvar geçişi süre göstergesi (süre aktifse)
            if snake.wall_pass_active and snake.wall_pass_timer > 0:
                # Her 15 framede bir (1 saniyede bir) süreyi güncelle
                seconds_left = snake.wall_pass_timer // 15
                
                # Saniye değiştiğinde güncelle
                if seconds_left != wall_pass_seconds_left:
                    wall_pass_seconds_left = seconds_left
                
                # Arka plan için yarı-saydam kutucuk
                timer_box = pygame.Surface((140, 30), pygame.SRCALPHA)
                timer_box.fill((0, 0, 0, 160))  # Siyah, yarı-saydam
                screen.blit(timer_box, (WINDOW_SIZE - 145, 5))
                
                # Süre göstergesi metni
                timer_font = pygame.font.SysFont("Arial", 18, bold=True)
                timer_text = f"Duvar Geçişi: {wall_pass_seconds_left} sn"
                
                # Metin rengi - süre azaldıkça kırmızıya yaklaşan renk
                color_intensity = min(1.0, max(0.0, (snake.wall_pass_timer / snake.wall_pass_duration)))
                timer_color = (
                    int(255), 
                    int(215 * color_intensity),
                    int(0)
                )
                
                # Ana metin
                timer_surface = timer_font.render(timer_text, True, timer_color)
                
                # Ekranın sağ üst köşesine yerleştir
                timer_rect = timer_surface.get_rect(center=(WINDOW_SIZE - 75, 20))
                
                # Çiz
                screen.blit(timer_surface, timer_rect)
            
            # Oyun bitti mi kontrolü
            if snake.dead:
                score.game_over(screen)
        
        elif game_state == SCOREBOARD:
            # Skor tablosunu göster
            show_scoreboard(screen, score)
            
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()

