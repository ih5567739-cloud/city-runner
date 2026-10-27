import pygame
import sys
import random
import math
import os

# -----------------------------------------------------------------------------
# 1. إعدادات محرك اللعبة والثوابت الأساسية
# -----------------------------------------------------------------------------
pygame.init()
pygame.font.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("City Runner - Ocean Odyssey Mobile Edition")
clock = pygame.time.Clock()

# لوحة الألوان السينمائية والبحرية
COLOR_SKY_TOP = (10, 20, 45)
COLOR_SKY_BOT = (55, 90, 150)
COLOR_SEA_TOP = (20, 80, 140)
COLOR_SEA_BOT = (5, 25, 60)
COLOR_GOLD = (255, 215, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_MUTED = (160, 180, 215)

def get_font(size, bold=False):
    try:
        return pygame.font.SysFont("arial", size, bold=bold)
    except:
        return pygame.font.Font(None, size)

FONT_TITLE = get_font(52, bold=True)
FONT_MEDIUM = get_font(24, bold=True)
FONT_SMALL = get_font(16, bold=False)

# حالات اللعبة (Game States)
STATE_MENU = "MENU"
STATE_LEVEL_SELECT = "LEVEL_SELECT"
STATE_SHOP = "SHOP"
STATE_UPGRADES = "UPGRADES"
STATE_ACHIEVEMENTS = "ACHIEVEMENTS"
STATE_SETTINGS = "SETTINGS"
STATE_PLAYING = "PLAYING"
STATE_PAUSE = "PAUSE"
STATE_WIN = "WIN"
STATE_LOSE = "LOSE"

# -----------------------------------------------------------------------------
# 2. نظام حفظ وتخزين البيانات المتطور
# -----------------------------------------------------------------------------
SAVE_FILE = "city_runner_ocean_save.txt"

def load_game_data():
    data = {
        "max_level": 1,
        "total_coins": 0,
        "unlocked_skins": ["Runner Boy"],
        "current_skin": "Runner Boy",
        "speed_lvl": 1,
        "jump_lvl": 1,
        "magnet_lvl": 1,
        "total_jumps": 0,
        "games_played": 0
    }
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as f:
                lines = [line.strip() for line in f.readlines()]
                if len(lines) >= 1 and lines[0].isdigit(): data["max_level"] = int(lines[0])
                if len(lines) >= 2 and lines[1].isdigit(): data["total_coins"] = int(lines[1])
                if len(lines) >= 3 and lines[2]: data["unlocked_skins"] = lines[2].split(",")
                if len(lines) >= 4 and lines[3]: data["current_skin"] = lines[3]
                if len(lines) >= 5 and lines[4].isdigit(): data["speed_lvl"] = int(lines[4])
                if len(lines) >= 6 and lines[5].isdigit(): data["jump_lvl"] = int(lines[5])
                if len(lines) >= 7 and lines[6].isdigit(): data["magnet_lvl"] = int(lines[6])
                if len(lines) >= 8 and lines[7].isdigit(): data["total_jumps"] = int(lines[7])
                if len(lines) >= 9 and lines[8].isdigit(): data["games_played"] = int(lines[8])
        except Exception as e:
            print(f"Error loading save: {e}")
    return data

def save_game_data(data_dict):
    try:
        with open(SAVE_FILE, "w") as f:
            f.write(f"{data_dict['max_level']}\n")
            f.write(f"{data_dict['total_coins']}\n")
            f.write(f"{','.join(data_dict['unlocked_skins'])}\n")
            f.write(f"{data_dict['current_skin']}\n")
            f.write(f"{data_dict['speed_lvl']}\n")
            f.write(f"{data_dict['jump_lvl']}\n")
            f.write(f"{data_dict['magnet_lvl']}\n")
            f.write(f"{data_dict['total_jumps']}\n")
            f.write(f"{data_dict['games_played']}\n")
    except Exception as e:
        print(f"Error saving data: {e}")

# -----------------------------------------------------------------------------
# 3. قاعدة بيانات الشخصيات الـ 12 المتقدمة
# -----------------------------------------------------------------------------
SKINS_DATABASE = {
    "Runner Boy": {"price": 0, "name": "Runner Boy", "desc": "البطل الأساسي السريع", "body": (240, 80, 80), "glow": (255, 255, 255)},
    "Cyber Ninja": {"price": 300, "name": "Cyber Ninja", "desc": "رشيق وخفيف الحركات", "body": (40, 45, 55), "glow": (220, 40, 40)},
    "Neon Mage": {"price": 700, "name": "Neon Mage", "desc": "ساحر طاقات النيون", "body": (110, 50, 200), "glow": (100, 240, 255)},
    "Gold Knight": {"price": 1500, "name": "Gold Knight", "desc": "فارس الذهب الأسطوري", "body": (230, 180, 40), "glow": (255, 255, 150)},
    "Shadow Assassin": {"price": 2800, "name": "Shadow Assassin", "desc": "سيد الظلال الخفي", "body": (20, 20, 25), "glow": (150, 50, 255)},
    "Cyberpunk Cop": {"price": 4500, "name": "Cyberpunk Cop", "desc": "حارس المستقبل القاسي", "body": (40, 90, 180), "glow": (255, 100, 100)},
    "Flame Phoenix": {"price": 7000, "name": "Flame Phoenix", "desc": "روح النيران المشتعلة", "body": (250, 120, 30), "glow": (255, 230, 50)},
    "Galaxy Emperor": {"price": 12000, "name": "Galaxy Emperor", "desc": "إمبراطور الفضاء المطلق", "body": (80, 20, 120), "glow": (200, 100, 255)},
    "Aqua Triton": {"price": 18000, "name": "Aqua Triton", "desc": "سيد المحيطات والبحار", "body": (0, 150, 200), "glow": (150, 255, 255)},
    "Storm Bringer": {"price": 25000, "name": "Storm Bringer", "desc": "صانع العواصف الرعدية", "body": (90, 90, 110), "glow": (255, 255, 0)},
    "Solar Titan": {"price": 35000, "name": "Solar Titan", "desc": "طاقة الشمس المشتعلة", "body": (255, 140, 0), "glow": (255, 255, 100)},
    "Void Walker": {"price": 50000, "name": "Void Walker", "desc": "مسافر الأبعاد الخفية", "body": (15, 15, 20), "glow": (200, 50, 255)}
}

# -----------------------------------------------------------------------------
# 4. أزرار تفاعلية
# -----------------------------------------------------------------------------
class TexturedButton:
    def __init__(self, x, y, width, height, text, is_locked=False):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.is_locked = is_locked
        self.hover_progress = 0.0

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        is_hover = self.rect.collidepoint(mouse_pos)

        if is_hover and not self.is_locked:
            self.hover_progress = min(1.0, self.hover_progress + 0.12)
        else:
            self.hover_progress = max(0.0, self.hover_progress - 0.12)

        if self.is_locked:
            top_col, bot_col, border_col, text_col = (45, 48, 60), (25, 28, 36), (60, 65, 80), (110, 120, 140)
        else:
            r1 = int(60 + self.hover_progress * 35)
            g1 = int(95 + self.hover_progress * 45)
            b1 = int(150 + self.hover_progress * 55)
            r2 = int(35 + self.hover_progress * 25)
            g2 = int(60 + self.hover_progress * 35)
            b2 = int(105 + self.hover_progress * 45)
            top_col, bot_col = (r1, g1, b1), (r2, g2, b2)
            border_col = (230, 240, 255) if is_hover else (130, 160, 205)
            text_col = COLOR_WHITE

        for y_off in range(self.rect.height):
            inter = y_off / self.rect.height
            cr = int(top_col[0] * (1 - inter) + bot_col[0] * inter)
            cg = int(top_col[1] * (1 - inter) + bot_col[1] * inter)
            cb = int(top_col[2] * (1 - inter) + bot_col[2] * inter)
            pygame.draw.line(surface, (cr, cg, cb), (self.rect.x, self.rect.y + y_off), (self.rect.right, self.rect.y + y_off))

        pygame.draw.rect(surface, border_col, self.rect, 2, border_radius=14)
        display_str = f"Locked: {self.text}" if self.is_locked else self.text
        text_surf = FONT_MEDIUM.render(display_str, True, text_col)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, event):
        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.FINGERDOWN):
            pos = event.pos if event.type == pygame.MOUSEBUTTONDOWN else (event.x * SCREEN_WIDTH, event.y * SCREEN_HEIGHT)
            if self.rect.collidepoint(pos) and not self.is_locked:
                return True
        return False

# -----------------------------------------------------------------------------
# 5. نظام المؤثرات السينمائية والجسيمات
# -----------------------------------------------------------------------------
class CinematicFX:
    def __init__(self):
        self.particles = []
        self.shake_time = 0
        self.shake_power = 0

    def trigger_shake(self, duration, power):
        self.shake_time = duration
        self.shake_power = power

    def spawn_particles(self, x, y, color=COLOR_GOLD, count=16):
        for _ in range(count):
            self.particles.append({
                'x': x, 'y': y,
                'vx': random.uniform(-4.0, 4.0),
                'vy': random.uniform(-5.5, 1.5),
                'life': random.randint(30, 50),
                'color': color,
                'size': random.randint(3, 8)
            })

    def update_and_render(self, surface, camera_x):
        for p in self.particles[:]:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['vy'] += 0.25
            p['life'] -= 1
            if p['life'] <= 0:
                self.particles.remove(p)
            else:
                dx = int(p['x'] - camera_x)
                dy = int(p['y'])
                pygame.draw.circle(surface, p['color'], (dx, dy), p['size'])

    def get_shake_offset(self):
        if self.shake_time > 0:
            self.shake_time -= 1
            return random.randint(-self.shake_power, self.shake_power), random.randint(-self.shake_power, self.shake_power)
        return 0, 0

fx_manager = CinematicFX()

# -----------------------------------------------------------------------------
# 6. كلاس اللاعب مع دعم الكيبورد واللمس (Touch Controls)
# -----------------------------------------------------------------------------
class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 34, 46)
        self.vel_x = 0
        self.vel_y = 0
        self.is_jumping = False
        self.facing = 1

    def update(self, solid_objs, coins, goal, game, touch_left, touch_right, touch_jump):
        speed_bonus = (game.save_data_dict["speed_lvl"] - 1) * 0.4
        current_speed = 5.2 + speed_bonus

        keys = pygame.key.get_pressed()
        self.vel_x = 0
        
        # دعم الكيبورد + أزرار اللمس الشفافة على الشاشة
        if keys[pygame.K_LEFT] or keys[pygame.K_a] or touch_left:
            self.vel_x = -current_speed
            self.facing = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d] or touch_right:
            self.vel_x = current_speed
            self.facing = 1

        jump_bonus = (game.save_data_dict["jump_lvl"] - 1) * 0.5
        jump_power = -13.5 - jump_bonus

        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w] or touch_jump) and not self.is_jumping:
            self.vel_y = jump_power
            self.is_jumping = True
            game.save_data_dict["total_jumps"] += 1
            game.save_data()

        # الحركة الأفقية
        self.rect.x += self.vel_x
        for obj in solid_objs:
            if self.rect.colliderect(obj.rect):
                if self.vel_x > 0: self.rect.right = obj.rect.left
                elif self.vel_x < 0: self.rect.left = obj.rect.right

        # الحركة الرأسية والجاذبية
        self.vel_y += 0.58
        if self.vel_y > 13.0: self.vel_y = 13.0
            
        self.rect.y += self.vel_y
        for obj in solid_objs:
            if self.rect.colliderect(obj.rect):
                if self.vel_y > 0:
                    self.rect.bottom = obj.rect.top
                    self.vel_y = 0
                    self.is_jumping = False
                elif self.vel_y < 0:
                    self.rect.top = obj.rect.bottom
                    self.vel_y = 0

        # مغناطيس العملات
        magnet_range = 60 + (game.save_data_dict["magnet_lvl"] - 1) * 35
        for coin in coins[:]:
            dist_sq = (self.rect.centerx - coin.centerx)**2 + (self.rect.centery - coin.centery)**2
            if dist_sq < magnet_range**2:
                if coin.centerx < self.rect.centerx: coin.x += 3
                elif coin.centerx > self.rect.centerx: coin.x -= 3
                if coin.centery < self.rect.centery: coin.y += 3
                elif coin.centery > self.rect.centery: coin.y -= 3

            if self.rect.colliderect(coin):
                coins.remove(coin)
                game.save_data_dict["total_coins"] += 1
                fx_manager.spawn_particles(coin.centerx, coin.centery, COLOR_GOLD, 12)
                fx_manager.trigger_shake(5, 2)
                game.save_data()

        # السقوط في البحر
        if self.rect.y > SCREEN_HEIGHT - 100:
            fx_manager.trigger_shake(25, 8)
            game.trigger_lose()

        # الفوز والوصول للبوابة
        if self.rect.colliderect(goal):
            fx_manager.trigger_shake(15, 4)
            game.trigger_win()

    def respawn(self, x, y):
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0

    def draw(self, surface, camera_x, skin_name):
        draw_rect = pygame.Rect(self.rect.x - camera_x, self.rect.y, self.rect.width, self.rect.height)
        skin_info = SKINS_DATABASE.get(skin_name, SKINS_DATABASE["Runner Boy"])
        pygame.draw.rect(surface, skin_info["body"], draw_rect, border_radius=10)
        eye_x = draw_rect.x + (20 if self.facing == 1 else 6)
        pygame.draw.ellipse(surface, skin_info["glow"], (eye_x, draw_rect.y + 12, 6, 9))

# -----------------------------------------------------------------------------
# 7. الأجسام والمنصات والسيارات الواقفة
# -----------------------------------------------------------------------------
class WorldObject:
    def __init__(self, x, y, width, height, obj_type, palette=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.obj_type = obj_type
        self.palette = palette if palette else ((90, 110, 140), (145, 175, 210))

    def draw(self, surface, camera_x):
        dr = pygame.Rect(self.rect.x - camera_x, self.rect.y, self.rect.width, self.rect.height)
        if dr.right > 0 and dr.left < SCREEN_WIDTH:
            if self.obj_type == 'car':
                car_color = random.choice([(220, 50, 50), (40, 130, 240), (240, 180, 40)])
                pygame.draw.rect(surface, car_color, dr, border_radius=7)
                roof = pygame.Rect(dr.x + 14, dr.y - 16, dr.width - 28, 17)
                pygame.draw.rect(surface, car_color, roof, border_radius=5)
                pygame.draw.rect(surface, (220, 240, 255), (roof.x + 5, roof.y + 3, roof.width - 10, 9))
                pygame.draw.circle(surface, (25, 25, 25), (dr.left + 15, dr.bottom), 8)
                pygame.draw.circle(surface, (25, 25, 25), (dr.right - 15, dr.bottom), 8)
            else:
                pygame.draw.rect(surface, self.palette[0], dr, border_radius=7)
                pygame.draw.rect(surface, self.palette[1], (dr.x, dr.y, dr.width, 8), border_radius=7)

# -----------------------------------------------------------------------------
# 8. إدارة اللعبة الكبرى ومحرك 500 مستوى والتطويرات
# -----------------------------------------------------------------------------
class MasterGameController:
    def __init__(self):
        self.state = STATE_MENU
        saved = load_game_data()
        self.save_data_dict = saved
        
        self.current_level = 1
        self.world_width = 6500
        self.player = Player(80, 250)
        self.solid_objects = []
        self.coins = []
        self.buildings = []
        self.clouds = []
        self.goal = pygame.Rect(0, 0, 35, 80)
        self.player_start = (80, 250)
        self.current_palette = ((90, 110, 140), (145, 175, 210))
        self.wave_timer = 0.0

        # حدود أزرار التحكم باللمس على الشاشة للموبايل
        self.btn_touch_left = pygame.Rect(30, 580, 90, 90)
        self.btn_touch_right = pygame.Rect(140, 580, 90, 90)
        self.btn_touch_jump = pygame.Rect(1150, 580, 100, 90)

        self.setup_ui()

    def save_data(self):
        save_game_data(self.save_data_dict)

    def setup_ui(self):
        cx = SCREEN_WIDTH // 2 - 190
        self.btn_start = TexturedButton(cx, 160, 380, 52, "Start Game")
        self.btn_levels = TexturedButton(cx, 225, 380, 52, "Level Select")
        self.btn_shop = TexturedButton(cx, 290, 380, 52, "Characters Shop")
        self.btn_upgrades = TexturedButton(cx, 355, 380, 52, "Upgrades & Skills")
        self.btn_achievements = TexturedButton(cx, 420, 380, 52, "Achievements & Stats")
        self.btn_settings = TexturedButton(cx, 485, 380, 52, "Settings")
        self.btn_quit = TexturedButton(cx, 550, 380, 52, "Quit Game")

        self.btn_back_menu = TexturedButton(cx, 630, 380, 48, "Main Menu")
        
        self.btn_next_level = TexturedButton(cx, 260, 380, 52, "Next Level")
        self.btn_win_menu = TexturedButton(cx, 330, 380, 52, "Main Menu")
        
        self.btn_restart_lose = TexturedButton(cx, 260, 380, 52, "Restart Level")
        self.btn_lose_menu = TexturedButton(cx, 330, 380, 52, "Main Menu")

        self.btn_resume = TexturedButton(cx, 220, 380, 52, "Resume Game")
        self.btn_pause_menu = TexturedButton(cx, 290, 380, 52, "Main Menu")
        self.btn_pause_quit = TexturedButton(cx, 360, 380, 52, "Quit Game")

    def load_level(self, lvl):
        self.current_level = lvl
        random.seed(lvl * 999)
        self.save_data_dict["games_played"] += 1
        self.save_data()
        
        self.solid_objects = []
        self.coins = []
        self.buildings = []
        self.clouds = []
        
        self.world_width = 5800 + (lvl * 45)

        palettes = [
            ((90, 110, 140), (145, 175, 210)),
            ((130, 85, 60), (185, 120, 90)),
            ((55, 130, 90), (90, 185, 125)),
            ((120, 55, 130), (175, 95, 185)),
            ((50, 105, 140), (85, 155, 195))
        ]
        self.current_palette = palettes[(lvl - 1) % len(palettes)]

        for _ in range(20):
            self.clouds.append([random.randint(0, self.world_width), random.randint(30, 160), random.randint(90, 180)])

        bx = 0
        while bx < self.world_width + 1000:
            bw = random.randint(100, 175)
            bh = random.randint(220, 400)
            self.buildings.append((bx, SCREEN_HEIGHT - 120 - bh, bw, bh))
            bx += bw + random.randint(18, 35)

        self.solid_objects.append(WorldObject(50, 420, 230, 35, 'platform', self.current_palette))
        self.player_start = (80, 350)

        cx = 320
        last_py = 350
        while cx < self.world_width - 180:
            pw = random.randint(130, 180)
            ph = 28
            py = random.randint(max(230, last_py - 95), min(450, last_py + 95))
            last_py = py
            
            obj_type = 'car' if random.random() < 0.3 else 'platform'
            if obj_type == 'car':
                pw, ph = 76, 36
                self.solid_objects.append(WorldObject(cx, py + 4, pw, ph, 'car'))
            else:
                self.solid_objects.append(WorldObject(cx, py, pw, ph, 'platform', self.current_palette))
            
            if random.random() < 0.85:
                self.coins.append(pygame.Rect(cx + pw//2 - 9, py - 48, 18, 18))

            cx += pw + random.randint(95, 135)

        self.goal = pygame.Rect(self.world_width - 130, 320, 35, 95)
        self.player.respawn(self.player_start[0], self.player_start[1])

    def trigger_win(self):
        next_lvl = self.current_level + 1
        if next_lvl > self.save_data_dict["max_level"] and next_lvl <= 500:
            self.save_data_dict["max_level"] = next_lvl
        self.save_data()
        self.state = STATE_WIN

    def trigger_lose(self):
        self.state = STATE_LOSE

    def run(self):
        running = True
        while running:
            clock.tick(FPS)
            events = pygame.event.get()

            # تتبع حالة اللمس على الأزرار الشفافة على شاشة الهاتف
            touch_left = False
            touch_right = False
            touch_jump = False

            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.FINGERDOWN):
                    pos = event.pos if event.type == pygame.MOUSEBUTTONDOWN else (event.x * SCREEN_WIDTH, event.y * SCREEN_HEIGHT)
                    if self.btn_touch_left.collidepoint(pos): touch_left = True
                    if self.btn_touch_right.collidepoint(pos): touch_right = True
                    if self.btn_touch_jump.collidepoint(pos): touch_jump = True

            # تتبع مستمر للاختيار عبر شاشات اللمس المتعددة (Multi-touch)
            if pygame.mouse.get_pressed()[0]:
                m_pos = pygame.mouse.get_pos()
                if self.btn_touch_left.collidepoint(m_pos): touch_left = True
                if self.btn_touch_right.collidepoint(m_pos): touch_right = True
                if self.btn_touch_jump.collidepoint(m_pos): touch_jump = True

            if self.state == STATE_MENU:
                screen.fill(COLOR_SKY_BOT)
                title_surf = FONT_TITLE.render("CITY RUNNER - OCEAN ODYSSEY", True, COLOR_WHITE)
                screen.blit(title_surf, (SCREEN_WIDTH//2 - title_surf.get_width()//2, 45))

                coins_surf = FONT_MEDIUM.render(f"Coins: {self.save_data_dict['total_coins']} 🪙", True, COLOR_GOLD)
                screen.blit(coins_surf, (SCREEN_WIDTH - 220, 25))

                self.btn_start.draw(screen)
                self.btn_levels.draw(screen)
                self.btn_shop.draw(screen)
                self.btn_upgrades.draw(screen)
                self.btn_achievements.draw(screen)
                self.btn_settings.draw(screen)
                self.btn_quit.draw(screen)

                ev = events[0] if events else pygame.event.Event(pygame.NOEVENT)
                if self.btn_start.is_clicked(ev):
                    self.load_level(self.current_level)
                    self.state = STATE_PLAYING
                elif self.btn_levels.is_clicked(ev):
                    self.state = STATE_LEVEL_SELECT
                elif self.btn_shop.is_clicked(ev):
                    self.state = STATE_SHOP
                elif self.btn_upgrades.is_clicked(ev):
                    self.state = STATE_UPGRADES
                elif self.btn_achievements.is_clicked(ev):
                    self.state = STATE_ACHIEVEMENTS
                elif self.btn_settings.is_clicked(ev):
                    self.state = STATE_SETTINGS
                elif self.btn_quit.is_clicked(ev):
                    running = False

            elif self.state == STATE_LEVEL_SELECT:
                screen.fill(COLOR_SKY_BOT)
                title_surf = FONT_TITLE.render("Select Level (1 - 500)", True, COLOR_WHITE)
                screen.blit(title_surf, (SCREEN_WIDTH//2 - title_surf.get_width()//2, 20))

                for i in range(1, 11):
                    bx = 130 + ((i - 1) % 5) * 210
                    by = 110 + ((i - 1) // 5) * 85
                    is_locked = i > self.save_data_dict["max_level"]
                    btn = TexturedButton(bx, by, 190, 52, f"Level {i}", is_locked=is_locked)
                    btn.draw(screen)

                    for event in events:
                        if btn.is_clicked(event) and not is_locked:
                            self.load_level(i)
                            self.state = STATE_PLAYING

                adv_lvls = [20, 50, 100, 200, 300, 400, 500]
                for idx, lvl_num in enumerate(adv_lvls):
                    bx = 130 + (idx % 4) * 265
                    by = 300 + (idx // 4) * 85
                    is_locked = lvl_num > self.save_data_dict["max_level"]
                    btn = TexturedButton(bx, by, 235, 52, f"Level {lvl_num}", is_locked=is_locked)
                    btn.draw(screen)

                    for event in events:
                        if btn.is_clicked(event) and not is_locked:
                            self.load_level(lvl_num)
                            self.state = STATE_PLAYING

                self.btn_back_menu.rect.y = 630
                self.btn_back_menu.draw(screen)
                ev = events[0] if events else pygame.event.Event(pygame.NOEVENT)
                if self.btn_back_menu.is_clicked(ev): self.state = STATE_MENU

            elif self.state == STATE_SHOP:
                screen.fill(COLOR_SKY_BOT)
                title_surf = FONT_TITLE.render("Characters Roster & Shop (12 Heroes)", True, COLOR_WHITE)
                screen.blit(title_surf, (SCREEN_WIDTH//2 - title_surf.get_width()//2, 20))

                coins_surf = FONT_MEDIUM.render(f"Coins: {self.save_data_dict['total_coins']} 🪙", True, COLOR_GOLD)
                screen.blit(coins_surf, (35, 25))

                skin_keys = list(SKINS_DATABASE.keys())
                for idx, skin_key in enumerate(skin_keys):
                    skin_info = SKINS_DATABASE[skin_key]
                    is_owned = skin_key in self.save_data_dict["unlocked_skins"]
                    is_active = skin_key == self.save_data_dict["current_skin"]

                    col = idx % 3
                    row = idx // 3
                    bx = 80 + col * 400
                    by = 95 + row * 135

                    card_rect = pygame.Rect(bx, by, 380, 122)
                    pygame.draw.rect(screen, (32, 45, 68), card_rect, border_radius=14)
                    pygame.draw.rect(screen, COLOR_GOLD if is_active else (80, 105, 145), card_rect, 2, border_radius=14)

                    icon_rect = pygame.Rect(bx + 18, by + 30, 40, 58)
                    pygame.draw.rect(screen, skin_info["body"], icon_rect, border_radius=6)
                    pygame.draw.ellipse(screen, skin_info["glow"], (icon_rect.x + 24, icon_rect.y + 16, 7, 10))

                    name_surf = FONT_MEDIUM.render(skin_info["name"], True, COLOR_WHITE)
                    desc_surf = FONT_SMALL.render(skin_info["desc"], True, COLOR_MUTED)
                    screen.blit(name_surf, (bx + 75, by + 20))
                    screen.blit(desc_surf, (bx + 75, by + 48))

                    status_str = "Equipped" if is_active else ("Select" if is_owned else f"Buy: {skin_info['price']} 🪙")
                    btn = TexturedButton(bx + 225, by + 72, 142, 38, status_str)
                    btn.draw(screen)

                    for event in events:
                        if btn.is_clicked(event):
                            if is_owned:
                                self.save_data_dict["current_skin"] = skin_key
                                self.save_data()
                            else:
                                if self.save_data_dict["total_coins"] >= skin_info["price"]:
                                    self.save_data_dict["total_coins"] -= skin_info["price"]
                                    self.save_data_dict["unlocked_skins"].append(skin_key)
                                    self.save_data_dict["current_skin"] = skin_key
                                    self.save_data()

                self.btn_back_menu.rect.y = 635
                self.btn_back_menu.draw(screen)
                ev = events[0] if events else pygame.event.Event(pygame.NOEVENT)
                if self.btn_back_menu.is_clicked(ev): self.state = STATE_MENU

            elif self.state == STATE_UPGRADES:
                screen.fill(COLOR_SKY_BOT)
                title_surf = FONT_TITLE.render("Character Skills & Upgrades", True, COLOR_WHITE)
                screen.blit(title_surf, (SCREEN_WIDTH//2 - title_surf.get_width()//2, 40))

                coins_surf = FONT_MEDIUM.render(f"Coins: {self.save_data_dict['total_coins']} 🪙", True, COLOR_GOLD)
                screen.blit(coins_surf, (35, 25))

                upgrades_info = [
                    ("Speed Boost", self.save_data_dict["speed_lvl"], 250 * self.save_data_dict["speed_lvl"], 180),
                    ("Super Jump", self.save_data_dict["jump_lvl"], 300 * self.save_data_dict["jump_lvl"], 290),
                    ("Coin Magnet", self.save_data_dict["magnet_lvl"], 400 * self.save_data_dict["magnet_lvl"], 400)
                ]

                up_buttons = []
                for idx, (up_name, lvl_val, cost, py) in enumerate(upgrades_info):
                    card_rect = pygame.Rect(SCREEN_WIDTH//2 - 300, py, 600, 95)
                    pygame.draw.rect(screen, (32, 45, 68), card_rect, border_radius=14)
                    pygame.draw.rect(screen, (80, 105, 145), card_rect, 2, border_radius=14)

                    t_surf = FONT_MEDIUM.render(f"{up_name} (Level {lvl_val}/5)", True, COLOR_WHITE)
                    screen.blit(t_surf, (card_rect.x + 25, card_rect.y + 20))

                    btn = TexturedButton(card_rect.right - 180, card_rect.y + 28, 150, 42, f"Upgrade: {cost}" if lvl_val < 5 else "MAX")
                    btn.draw(screen)
                    up_buttons.append((idx, cost, lvl_val, btn))

                self.btn_back_menu.rect.y = 540
                self.btn_back_menu.draw(screen)
                ev = events[0] if events else pygame.event.Event(pygame.NOEVENT)
                if self.btn_back_menu.is_clicked(ev): self.state = STATE_MENU

                for event in events:
                    for idx, cost, lvl_val, btn in up_buttons:
                        if btn.is_clicked(event) and lvl_val < 5:
                            if self.save_data_dict["total_coins"] >= cost:
                                self.save_data_dict["total_coins"] -= cost
                                if idx == 0: self.save_data_dict["speed_lvl"] += 1
                                elif idx == 1: self.save_data_dict["jump_lvl"] += 1
                                elif idx == 2: self.save_data_dict["magnet_lvl"] += 1
                                self.save_data()

            elif self.state == STATE_ACHIEVEMENTS:
                screen.fill(COLOR_SKY_BOT)
                title_surf = FONT_TITLE.render("Achievements & Stats Dashboard", True, COLOR_WHITE)
                screen.blit(title_surf, (SCREEN_WIDTH//2 - title_surf.get_width()//2, 80))

                st_1 = FONT_MEDIUM.render(f"Total Games Played: {self.save_data_dict['games_played']}", True, COLOR_WHITE)
                st_2 = FONT_MEDIUM.render(f"Total Jumps Made: {self.save_data_dict['total_jumps']}", True, COLOR_WHITE)
                st_3 = FONT_MEDIUM.render(f"Max Level Unlocked: {self.save_data_dict['max_level']} / 500", True, COLOR_GOLD)
                st_4 = FONT_MEDIUM.render(f"Heroes Unlocked: {len(self.save_data_dict['unlocked_skins'])} / {len(SKINS_DATABASE)}", True, COLOR_WHITE)

                screen.blit(st_1, (SCREEN_WIDTH//2 - st_1.get_width()//2, 220))
                screen.blit(st_2, (SCREEN_WIDTH//2 - st_2.get_width()//2, 280))
                screen.blit(st_3, (SCREEN_WIDTH//2 - st_3.get_width()//2, 340))
                screen.blit(st_4, (SCREEN_WIDTH//2 - st_4.get_width()//2, 400))

                self.btn_back_menu.rect.y = 520
                self.btn_back_menu.draw(screen)
                ev = events[0] if events else pygame.event.Event(pygame.NOEVENT)
                if self.btn_back_menu.is_clicked(ev): self.state = STATE_MENU

            elif self.state == STATE_SETTINGS:
                screen.fill(COLOR_SKY_BOT)
                title_surf = FONT_TITLE.render("Settings & Controls", True, COLOR_WHITE)
                screen.blit(title_surf, (SCREEN_WIDTH//2 - title_surf.get_width()//2, 90))

                info_1 = FONT_MEDIUM.render("Movement: Touch Buttons on Screen or A/D Keys", True, COLOR_WHITE)
                info_2 = FONT_MEDIUM.render("Jump: On-screen Jump Button or Space/W Keys", True, COLOR_WHITE)
                info_3 = FONT_MEDIUM.render("Jump on Platforms & Cars, Avoid the Beautiful Ocean!", True, COLOR_MUTED)

                screen.blit(info_1, (SCREEN_WIDTH//2 - info_1.get_width()//2, 220))
                screen.blit(info_2, (SCREEN_WIDTH//2 - info_2.get_width()//2, 280))
                screen.blit(info_3, (SCREEN_WIDTH//2 - info_3.get_width()//2, 340))

                self.btn_back_menu.rect.y = 480
                self.btn_back_menu.draw(screen)
                ev = events[0] if events else pygame.event.Event(pygame.NOEVENT)
                if self.btn_back_menu.is_clicked(ev): self.state = STATE_MENU

            elif self.state == STATE_PLAYING:
                for event in events:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.state = STATE_PAUSE

                self.player.update(self.solid_objects, self.coins, self.goal, self, touch_left, touch_right, touch_jump)

                camera_x = self.player.rect.centerx - SCREEN_WIDTH // 2
                camera_x = max(0, min(camera_x, self.world_width - SCREEN_WIDTH))

                shake_x, shake_y = fx_manager.get_shake_offset()
                self.wave_timer += 0.05

                # --- رسم خلفية وتدرجات السماء ---
                for y_coord in range(SCREEN_HEIGHT - 120):
                    inter = y_coord / (SCREEN_HEIGHT - 120)
                    r = int(COLOR_SKY_TOP[0] * (1 - inter) + COLOR_SKY_BOT[0] * inter)
                    g = int(COLOR_SKY_TOP[1] * (1 - inter) + COLOR_SKY_BOT[1] * inter)
                    b = int(COLOR_SKY_TOP[2] * (1 - inter) + COLOR_SKY_BOT[2] * inter)
                    pygame.draw.line(screen, (r, g, b), (0, y_coord), (SCREEN_WIDTH, y_coord))

                for cx, cy, cw in self.clouds:
                    draw_cx = cx - (camera_x * 0.18)
                    if draw_cx + cw > 0 and draw_cx < SCREEN_WIDTH:
                        pygame.draw.ellipse(screen, (245, 250, 255, 175), (draw_cx + shake_x, cy + shake_y, cw, 26))

                for bx, by, bw, bh in self.buildings:
                    draw_x = bx - (camera_x * 0.42)
                    if draw_x + bw > 0 and draw_x < SCREEN_WIDTH:
                        pygame.draw.rect(screen, (20, 30, 50), (draw_x + shake_x, by + shake_y, bw, bh))
                        for wx in range(int(draw_x) + 12, int(draw_x + bw) - 15, 22):
                            for wy in range(by + 18, by + bh - 20, 28):
                                pygame.draw.rect(screen, (255, 235, 150), (wx + shake_x, wy + shake_y, 8, 12))

                # --- رسم البحر والأمواج المتحركة في الأسفل ---
                sea_start_y = SCREEN_HEIGHT - 120
                for y_coord in range(sea_start_y, SCREEN_HEIGHT):
                    inter = (y_coord - sea_start_y) / 120
                    sr = int(COLOR_SEA_TOP[0] * (1 - inter) + COLOR_SEA_BOT[0] * inter)
                    sg = int(COLOR_SEA_TOP[1] * (1 - inter) + COLOR_SEA_BOT[1] * inter)
                    sb = int(COLOR_SEA_TOP[2] * (1 - inter) + COLOR_SEA_BOT[2] * inter)
                    pygame.draw.line(screen, (sr, sg, sb), (0, y_coord + shake_y), (SCREEN_WIDTH, y_coord + shake_y))

                wave_points = []
                for x in range(0, SCREEN_WIDTH + 40, 30):
                    wy = sea_start_y + int(math.sin(x * 0.02 + self.wave_timer) * 8)
                    wave_points.append((x + shake_x, wy + shake_y))
                if len(wave_points) > 1:
                    pygame.draw.aalines(screen, (120, 200, 255), False, wave_points)

                for obj in self.solid_objects:
                    obj.draw(screen, camera_x - shake_x)

                for coin in self.coins:
                    draw_rect = pygame.Rect(coin.x - camera_x + shake_x, coin.y + shake_y, coin.width, coin.height)
                    if draw_rect.right > 0 and draw_rect.left < SCREEN_WIDTH:
                        pygame.draw.ellipse(screen, COLOR_GOLD, draw_rect)

                fx_manager.update_and_render(screen, camera_x - shake_x)

                goal_draw = pygame.Rect(self.goal.x - camera_x + shake_x, self.goal.y + shake_y, self.goal.width, self.goal.height)
                if goal_draw.right > 0 and goal_draw.left < SCREEN_WIDTH:
                    pygame.draw.rect(screen, (75, 230, 135), goal_draw, border_radius=6)
                    pygame.draw.rect(screen, COLOR_WHITE, goal_draw, 2, border_radius=6)

                self.player.draw(screen, camera_x - shake_x, self.save_data_dict["current_skin"])

                # --- رسم أزرار التحكم باللمس الشفافة على شاشة الموبايل أثناء اللعب ---
                pygame.draw.rect(screen, (255, 255, 255), self.btn_touch_left, 2, border_radius=15)
                l_surf = FONT_MEDIUM.render("◀", True, COLOR_WHITE)
                screen.blit(l_surf, l_surf.get_rect(center=self.btn_touch_left.center))

                pygame.draw.rect(screen, (255, 255, 255), self.btn_touch_right, 2, border_radius=15)
                r_surf = FONT_MEDIUM.render("▶", True, COLOR_WHITE)
                screen.blit(r_surf, r_surf.get_rect(center=self.btn_touch_right.center))

                pygame.draw.rect(screen, (85, 240, 125), self.btn_touch_jump, 2, border_radius=15)
                j_surf = FONT_MEDIUM.render("JUMP", True, (85, 240, 125))
                screen.blit(j_surf, j_surf.get_rect(center=self.btn_touch_jump.center))

                hud_text = FONT_MEDIUM.render(f"Level: {self.current_level} / 500   |   Coins: {self.save_data_dict['total_coins']} 🪙", True, COLOR_WHITE)
                screen.blit(hud_text, (20 + shake_x, 20 + shake_y))

            elif self.state == STATE_WIN:
                screen.fill((18, 28, 44))
                win_text = FONT_TITLE.render(f"Level {self.current_level} Completed!", True, (85, 240, 125))
                screen.blit(win_text, (SCREEN_WIDTH//2 - win_text.get_width()//2, 160))

                self.btn_next_level.draw(screen)
                self.btn_win_menu.draw(screen)

                ev = events[0] if events else pygame.event.Event(pygame.NOEVENT)
                if self.btn_next_level.is_clicked(ev):
                    if self.current_level < 500:
                        self.load_level(self.current_level + 1)
                        self.state = STATE_PLAYING
                elif self.btn_win_menu.is_clicked(ev): self.state = STATE_MENU

            elif self.state == STATE_LOSE:
                screen.fill((10, 20, 35))
                lose_text = FONT_TITLE.render("You Fell into the Ocean - Try Again", True, (245, 80, 80))
                screen.blit(lose_text, (SCREEN_WIDTH//2 - lose_text.get_width()//2, 160))

                self.btn_restart_lose.draw(screen)
                self.btn_lose_menu.draw(screen)

                ev = events[0] if events else pygame.event.Event(pygame.NOEVENT)
                if self.btn_restart_lose.is_clicked(ev):
                    self.load_level(self.current_level)
                    self.state = STATE_PLAYING
                elif self.btn_lose_menu.is_clicked(ev): self.state = STATE_MENU

            elif self.state == STATE_PAUSE:
                screen.fill(COLOR_SKY_BOT)
                pause_text = FONT_TITLE.render("Game Paused", True, COLOR_WHITE)
                screen.blit(pause_text, (SCREEN_WIDTH//2 - pause_text.get_width()//2, 120))

                self.btn_resume.draw(screen)
                self.btn_pause_menu.draw(screen)
                self.btn_pause_quit.draw(screen)

                ev = events[0] if events else pygame.event.Event(pygame.NOEVENT)
                if self.btn_resume.is_clicked(ev): self.state = STATE_PLAYING
                elif self.btn_pause_menu.is_clicked(ev): self.state = STATE_MENU
                elif self.btn_pause_quit.is_clicked(ev): running = False

            pygame.display.flip()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = MasterGameController()
    game.run()
