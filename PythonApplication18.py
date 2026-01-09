# -*- coding: utf-8 -*-
import pygame
import random
import math
import sys
import os
import numpy as np
import array

# Initialize PyGame
pygame.init()
pygame.mixer.init()

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
FPS = 60

class SoundManager1:
    def __init__(self):
        self.sounds = {}
        self.sfx_volume = 0.7  # Громкость эффектов
        
        # Создаём папку sounds если её нет
        if not os.path.exists("sounds"):
            os.makedirs("sounds")
        
        self.load_or_create_sounds()
    
    def load_or_create_sounds(self):
        """Загружает или создаёт звуки"""
        # Пробуем загрузить из файлов
        self.load_sound_files()
        
        # Если не нашли файлы, создаём простые звуки
        if 'laser' not in self.sounds:
            self.create_laser_sound()
        
        if 'explosion' not in self.sounds:
            self.create_explosion_sound()
    
    def load_sound_files(self):
        """Пробует загрузить звуки из файлов"""
        sound_files = {
            'laser': ['sounds/laser.wav', 'sounds/laser.ogg', 'sounds/shoot.wav'],
            'explosion': ['sounds/explosion.wav', 'sounds/explode.wav'],
        }
        
        for sound_name, paths in sound_files.items():
            for path in paths:
                if os.path.exists(path):
                    try:
                        self.sounds[sound_name] = pygame.mixer.Sound(path)
                        print(f"Загружен звук: {path}")
                        break
                    except:
                        pass
    
    def create_laser_sound(self):
        """Создаёт звук лазерного выстрела программно"""
        sample_rate = 22050
        duration = 0.1  # 0.1 секунды
        samples = int(sample_rate * duration)
        
        sound_data = []
        for i in range(samples):
            t = float(i) / sample_rate
            # Высокочастотный писк с затуханием
            frequency = 880 + math.sin(t * 100) * 50  # 880 Гц с модуляцией
            value = math.sin(t * frequency * 2 * math.pi) * 0.5
            
            # Затухание
            envelope = 1.0 - (t / duration)
            value *= envelope
            
            # Стерео
            sound_data.append([value, value])
        
        # Преобразуем в звук PyGame
        sound_array = pygame.sndarray.make_sound(
            (pygame.sndarray.array(sound_data) * 32767).astype(np.int16)
        )
        self.sounds['laser'] = sound_array
    
    def create_explosion_sound(self):
        """Создаёт звук взрыва"""
        sample_rate = 22050
        duration = 0.5
        samples = int(sample_rate * duration)
        
        sound_data = []
        for i in range(samples):
            t = float(i) / sample_rate
            # Низкочастотный взрыв с шумом
            frequency = 80 + 200 * math.exp(-t * 10)  # Падающая частота
            value = math.sin(t * frequency * 2 * math.pi) * 0.7
            
            # Добавляем шум для эффекта взрыва
            value += random.uniform(-0.1, 0.1)
            
            # Экспоненциальное затухание
            envelope = math.exp(-t * 8)
            value *= envelope
            
            sound_data.append([value, value])
        
        sound_array = pygame.sndarray.make_sound(
            (pygame.sndarray.array(sound_data) * 32767).astype(np.int16)
        )
        self.sounds['explosion'] = sound_array
    
    def play(self, sound_name, volume=None):
        """Проигрывает звуковой эффект"""
        if sound_name in self.sounds:
            sound = self.sounds[sound_name].copy()  # Копируем чтобы можно было играть одновременно
            if volume is not None:
                sound.set_volume(volume * self.sfx_volume)
            else:
                sound.set_volume(self.sfx_volume)
            sound.play()
            return sound
        return None
    
    def set_volume(self, sfx_vol=None):
        """Устанавливает громкость"""
        if sfx_vol is not None:
            self.sfx_volume = max(0.0, min(1.0, sfx_vol))
class SoundManager:
    def __init__(self):
        self.sounds = {}
        self.sfx_volume = 0.7
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        
        if not os.path.exists("sounds"):
            os.makedirs("sounds")
        
        self.load_or_create_sounds()
    
    def create_laser_sound(self):
        """Создаёт звук лазерного выстрела"""
        sample_rate = 22050
        duration = 0.15
        samples = int(sample_rate * duration)
        
        # Создаём массив для стерео звука (левый и правый канал чередуются)
        sound_data = array.array('h')
        
        for i in range(samples):
            t = float(i) / sample_rate
            # Основная частота с небольшими вариациями
            frequency = 880 + math.sin(t * 100) * 50
            value = math.sin(t * frequency * 2 * math.pi) * 0.5
            
            # Затухание
            envelope = 1.0 - (t / duration)
            value *= envelope
            
            sample = int(value * 32767)
            # Стерео - одинаковый звук в оба канала
            sound_data.append(sample)  # Левый канал
            sound_data.append(sample)  # Правый канал
        
        # Создаём звук
        sound = pygame.mixer.Sound(buffer=bytes(sound_data))
        sound.set_volume(0.6)
        return sound
    
    def create_explosion_sound(self):
        """Создаёт звук взрыва"""
        sample_rate = 22050
        duration = 0.5
        samples = int(sample_rate * duration)
        
        sound_data = array.array('h')
        
        for i in range(samples):
            t = float(i) / sample_rate
            frequency = 80 + 200 * math.exp(-t * 10)
            value = math.sin(t * frequency * 2 * math.pi) * 0.7
            
            # Добавляем немного шума
            value += random.uniform(-0.1, 0.1)
            
            # Экспоненциальное затухание
            envelope = math.exp(-t * 8)
            value *= envelope
            
            sample = int(value * 32767)
            sound_data.append(sample)
            sound_data.append(sample)  # Стерео
        
        sound = pygame.mixer.Sound(buffer=bytes(sound_data))
        sound.set_volume(0.8)
        return sound
    
    def load_or_create_sounds(self):
        """Загружает или создаёт звуки"""
        # Пробуем загрузить файлы
        sound_files = {
            'laser': ['sounds\laser.wav', 'sounds/laser.ogg', 'sounds\shoot.wav'],
            'explosion': ['sounds\explosion.wav', 'sounds\explode.wav', 'sounds/explosion.ogg'],
        }
        
        urrent_directory = os.path.dirname(os.path.abspath(__file__))

        for sound_name, paths in sound_files.items():
            loaded = False
            for path in paths:
                if os.path.exists(urrent_directory+"/"+path):
                    try:
                        self.sounds[sound_name] = pygame.mixer.Sound(path)
                        loaded = True
                        print(f"✓ Загружен звук: {path}")
                        break
                    except Exception as e:
                        print(f"✗ Ошибка загрузки {path}: {e}")
            
            if not loaded:
                # Создаём программно
                print(f"Создаю звук {sound_name} программно...")
                if sound_name == 'laser':
                    self.sounds[sound_name] = self.create_laser_sound()
                elif sound_name == 'explosion':
                    self.sounds[sound_name] = self.create_explosion_sound()
        
        # Создаём несколько вариантов звука выстрела для разнообразия
        #self.create_variations()
    
    def create_variations(self):
        """Создаёт вариации звуков для разнообразия"""
        self.laser_variations = []
        
        # Создаём 3 варианта звука выстрела с разной высотой
        for i in range(3):
            sample_rate = 22050
            duration = 0.1 + random.random() * 0.05
            samples = int(sample_rate * duration)
            
            sound_data = array.array('h')
            
            for j in range(samples):
                t = float(j) / sample_rate
                # Разная частота для каждого варианта
                frequency = 800 + i * 100 + random.random() * 50
                value = math.sin(t * frequency * 2 * math.pi) * 0.4
                envelope = 1.0 - (t / duration)
                value *= envelope
                
                sample = int(value * 32767)
                sound_data.append(sample)
                sound_data.append(sample)
            
            sound = pygame.mixer.Sound(buffer=bytes(sound_data))
            sound.set_volume(0.5)
            self.laser_variations.append(sound)
    
    def play(self, sound_name, volume=None):
        """Проигрывает звуковой эффект"""
        if sound_name == 'laser' and hasattr(self, 'laser_variations'):
            # Для выстрела используем случайную вариацию
            sound = random.choice(self.laser_variations)
        elif sound_name in self.sounds:
            sound = self.sounds[sound_name]
        else:
            return None
        
        # Устанавливаем громкость
        if volume is not None:
            current_volume = volume * self.sfx_volume
        else:
            current_volume = self.sfx_volume
        
        # В PyGame Sound не имеет copy(), поэтому создаём новый Sound с теми же данными
        # или просто играем оригинальный звук
        sound.set_volume(current_volume)
        sound.play()
        
        return sound
    
    def play_shoot(self):
        """Проигрывает звук выстрела (удобный метод)"""
        return self.play('laser')
    
    def play_explosion(self, volume=1.0):
        """Проигрывает звук взрыва"""
        return self.play('explosion')
    
    def set_volume(self, sfx_vol=None):
        """Устанавливает громкость звуковых эффектов"""
        if sfx_vol is not None:
            self.sfx_volume = max(0.0, min(1.0, sfx_vol))
# Modern color palette
class Colors:
    DARK_BLUE = (15, 25, 45)
    CYAN = (0, 255, 255)
    MAGENTA = (255, 0, 255)
    YELLOW = (255, 255, 0)
    WHITE = (240, 240, 255)
    RED = (255, 50, 50)
    GREEN = (50, 255, 100)
    PURPLE = (180, 70, 255)
    ORANGE = (255, 150, 50)
    BLUE = (50, 150, 255)

# Particles for visual effects
class Particle:
    def __init__(self, x, y, color, velocity, size=3, decay=0.9):
        self.x = x
        self.y = y
        self.color = color
        self.vx, self.vy = velocity
        self.size = size
        self.decay = decay
        self.life = 1.0
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vx *= self.decay
        self.vy *= self.decay
        self.life -= 0.02
        self.size = max(0.5, self.size * 0.97)
        return self.life > 0
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size))

# Particle system manager
class ParticleSystem:
    def __init__(self):
        self.particles = []
    
    def emit(self, x, y, count=10, color=Colors.CYAN, spread=3):
        for _ in range(count):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(0.5, spread)
            velocity = (math.cos(angle) * speed, math.sin(angle) * speed)
            self.particles.append(Particle(x, y, color, velocity))
    
    def update(self):
        self.particles = [p for p in self.particles if p.update()]
    
    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen)

# Player spaceship
class Player:
    def __init__(self, x, y, sound_manager=None):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 60
        self.speed = 6
        self.health = 100
        self.max_health = 100
        self.level = 1
        self.exp = 0
        self.exp_to_next = 50
        self.shoot_cooldown = 0
        self.shoot_delay = 0.12 #уменьшает задержку стрельбы
        self.bullet_speed = 25
        self.bullets = []
        self.invincible = 0
        self.particle_system = ParticleSystem()
        self.trail_cooldown = 0
        self.use_mouse_control = True  # Флаг управления мышкой
        self.mouse_speed = 0.2  # Плавность движения к курсору
        
        self.sound_manager = sound_manager
        self.shoot_cooldown = 0
        self.shoot_delay = 15  # Кадры между выстрелами
    
    def move(self, keys, mouse_pos=None):
         if self.use_mouse_control and mouse_pos:
            # Движение к курсору мыши
            target_x, target_y = mouse_pos
            
            # Плавное движение к цели
            dx = target_x - (self.x + self.width // 2)
            dy = target_y - (self.y + self.height // 2)
            
            self.x += dx * self.mouse_speed
            self.y += dy * self.mouse_speed
            
            # Ограничение в границах экрана
            self.x = max(20, min(SCREEN_WIDTH - 20 - self.width, self.x))
            self.y = max(20, min(SCREEN_HEIGHT - 20 - self.height, self.y))
         else:
            # Smooth movement
            # Здеся настраиваються бинды кнопок
            if keys[pygame.K_a] and self.x > 20:
               self.x -= self.speed
            if keys[pygame.K_d] and self.x < SCREEN_WIDTH - 20 - self.width:
               self.x += self.speed
            if keys[pygame.K_w] and self.y > 20:
               self.y -= self.speed
            if keys[pygame.K_s] and self.y < SCREEN_HEIGHT - 20 - self.height:
               self.y += self.speed
        
         # # Engine trail particles
         self.trail_cooldown -= 1
         if self.trail_cooldown <= 0:
            self.particle_system.emit(
                self.x + self.width // 2,
                self.y + self.height,
                count=2,
                color=Colors.CYAN,
                spread=0.5
            )
            self.trail_cooldown = 3
    
    def shoot(self):
        if self.shoot_cooldown <= 0:
            # Main shot
            self.bullets.append({
                'x': self.x + self.width // 2 - 2,
                'y': self.y,
                'width': 4,
                'height': 15,
                'speed': self.bullet_speed,
                'color': Colors.CYAN,
                'damage': 10 + self.level * 2
            })
            
            # Side shots at higher levels
            if self.level >= 3:
                self.bullets.append({
                    'x': self.x + 10,
                    'y': self.y + 20,
                    'width': 4,
                    'height': 15,
                    'speed': self.bullet_speed,
                    'color': Colors.CYAN,
                    'damage': 8 + self.level * 2
                })
                self.bullets.append({
                    'x': self.x + self.width - 10,
                    'y': self.y + 20,
                    'width': 4,
                    'height': 15,
                    'speed': self.bullet_speed,
                    'color': Colors.CYAN,
                    'damage': 8 + self.level * 2
                })
            
            self.shoot_cooldown = self.shoot_delay
            self.particle_system.emit(
                self.x + self.width // 2,
                self.y,
                count=5,
                color=Colors.YELLOW,
                spread=1
            )
             # Эффект выстрела
            self.particle_system.emit(
                self.x + self.width // 2,
                self.y,
                count=5,
                color=Colors.YELLOW,
                spread=1
            )
            
            # ⭐ ЗВУК ВЫСТРЕЛА ⭐
            if self.sound_manager:
                # Немного изменяем высоту для разнообразия
                pitch_variation = 0.9 + random.random() * 0.2
                self.sound_manager.play('laser', volume=pitch_variation)
    
    
    def update_bullets(self):
        for bullet in self.bullets[:]:
            bullet['y'] -= bullet['speed']
            if bullet['y'] < -20:
                self.bullets.remove(bullet)
    
    def take_damage(self, amount):
        if self.invincible <= 0:
            self.health = max(0, self.health - amount)
            self.invincible = 30  # 0.5 seconds of invincibility
            self.particle_system.emit(
                self.x + self.width // 2,
                self.y + self.height // 2,
                count=20,
                color=Colors.RED,
                spread=5
            )
            return True
        return False
    
    def add_exp(self, amount):
        self.exp += amount
        while self.exp >= self.exp_to_next:
            self.level_up()
    
    def level_up(self):
        self.level += 1
        self.exp -= self.exp_to_next
        self.exp_to_next = int(self.exp_to_next * 1.5)
        self.max_health += 20
        self.health = self.max_health
       # self.shoot_delay = max(5, self.shoot_delay - 1)  # Faster shooting
        self.bullet_speed += 1
        
        # Level up effect
        for _ in range(50):
            self.particle_system.emit(
                self.x + self.width // 2,
                self.y + self.height // 2,
                count=1,
                color=random.choice([Colors.CYAN, Colors.MAGENTA, Colors.YELLOW]),
                spread=8
            )
    
    def update(self):
        self.shoot_cooldown = max(0, self.shoot_cooldown - 1)
        self.invincible = max(0, self.invincible - 1)
        self.update_bullets()
        self.particle_system.update()
        # В методе update() класса Game:
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        self.move(keys, mouse_pos)

        # Переключение по клавише M
        if keys[pygame.K_m]:
           self.toggle_control_mode()

        mouse_buttons = pygame.mouse.get_pressed()  # (левая, средняя, правая)
        # Стрельба по ЛЕВОЙ кнопке мыши
        if mouse_buttons[0]:  # Индекс 0 = левая кнопка
            self.shoot()
    
    def draw(self, screen):
        # Draw player ship (triangle)
        points = [
            (self.x + self.width // 2, self.y),  # Nose
            (self.x, self.y + self.height),      # Bottom left
            (self.x + self.width, self.y + self.height)  # Bottom right
        ]
        
        # Color with invincibility effect
        if self.invincible > 0 and self.invincible % 6 < 3:
            color = Colors.WHITE
        else:
            color = Colors.CYAN
        
        pygame.draw.polygon(screen, color, points)
        pygame.draw.polygon(screen, Colors.WHITE, points, 2)
        
        # Engines
        pygame.draw.rect(screen, Colors.ORANGE, 
                        (self.x + 10, self.y + self.height - 10, 8, 15))
        pygame.draw.rect(screen, Colors.ORANGE, 
                        (self.x + self.width - 18, self.y + self.height - 10, 8, 15))
        
        # Bullets
        for bullet in self.bullets:
            pygame.draw.rect(screen, bullet['color'], 
                           (bullet['x'], bullet['y'], bullet['width'], bullet['height']))
        
        # Particles
        self.particle_system.draw(screen)

# Enemy ships
class Enemy:
    def __init__(self, x, y, enemy_type="normal"):
        self.x = x
        self.y = y
        self.type = enemy_type
        self.speed = random.uniform(1.0, 3.0)
        self.health = 30
        self.max_health = 30
        self.value = 10  # Experience value
        
        if enemy_type == "fast":
            self.speed = 4.0
            self.health = 20
            self.color = Colors.MAGENTA
            self.value = 15
        elif enemy_type == "tank":
            self.speed = 0.8
            self.health = 100
            self.color = Colors.ORANGE
            self.value = 30
        else:
            self.color = Colors.GREEN
    
    def update(self):
        self.y += self.speed
        return self.y < SCREEN_HEIGHT + 50
    
    def draw(self, screen):
        # Draw enemy based on type
        if self.type == "normal":
            pygame.draw.rect(screen, self.color, (self.x, self.y, 40, 40))
            pygame.draw.rect(screen, Colors.WHITE, (self.x, self.y, 40, 40), 2)
            pygame.draw.circle(screen, Colors.RED, (self.x + 20, self.y + 15), 6)
        
        elif self.type == "fast":
            points = [
                (self.x + 20, self.y),
                (self.x, self.y + 40),
                (self.x + 40, self.y + 40)
            ]
            pygame.draw.polygon(screen, self.color, points)
            pygame.draw.polygon(screen, Colors.WHITE, points, 2)
        
        elif self.type == "tank":
            pygame.draw.rect(screen, self.color, (self.x - 10, self.y, 60, 30))
            pygame.draw.rect(screen, Colors.WHITE, (self.x - 10, self.y, 60, 30), 3)
            pygame.draw.rect(screen, Colors.DARK_BLUE, (self.x + 15, self.y - 10, 10, 15))
        
        # Health bar
        if self.health < self.max_health:
            health_width = 40
            health_ratio = max(0, self.health / self.max_health)
            pygame.draw.rect(screen, Colors.RED, (self.x, self.y - 10, health_width, 5))
            pygame.draw.rect(screen, Colors.GREEN, (self.x, self.y - 10, health_width * health_ratio, 5))

# Boss enemy
class Boss:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2 - 100
        self.y = -200
        self.width = 200
        self.height = 150
        self.health = 500
        self.max_health = 500
        self.speed = 1
        self.direction = 1
        self.phase = 1
        self.attack_cooldown = 0
        self.bullets = []
        self.particle_system = ParticleSystem()
        self.invincible = 0
    
    def update(self):
        # Movement
        self.x += self.speed * self.direction
        if self.x <= 0 or self.x >= SCREEN_WIDTH - self.width:
            self.direction *= 1
            self.y += 30
        
        # Attack
        self.attack_cooldown -= 0
        if self.attack_cooldown <= 0:
            self.shoot()
            self.attack_cooldown = 60  # Attack every second
        
        # Update bullets
        for bullet in self.bullets[:]:
            bullet['y'] += bullet['speed']
            bullet['x'] += bullet['vx']
            if bullet['y'] > SCREEN_HEIGHT + 20:
                self.bullets.remove(bullet)
        
        self.particle_system.update()
        
        return self.health > 0 and self.y < SCREEN_HEIGHT + 100
    
    def shoot(self):
        if self.phase == 1:
            # Fan attack
            for angle in range(-30, 31, 10):
                rad = math.radians(angle)
                self.bullets.append({
                    'x': self.x + self.width // 2,
                    'y': self.y + self.height,
                    'vx': math.sin(rad) * 3,
                    'vy': math.cos(rad) * 5,
                    'color': Colors.RED,
                    'size': 8,
                    'speed': 1
                })
        else:
            # Targeted attack
            for _ in range(3):
                self.bullets.append({
                    'x': self.x + self.width // 2 + random.randint(-20, 20),
                    'y': self.y + self.height,
                    'vx': random.uniform(-1, 1),
                    'vy': 7,
                    'color': Colors.ORANGE,
                    'size': 12,
                    'speed': 1
                })
        
        # Shot effect
        self.particle_system.emit(
            self.x + self.width // 2,
            self.y + self.height,
            count=20,
            color=Colors.RED,
            spread=3
        )
    
    def take_damage(self, amount):
        if self.invincible <= 0:
            self.health = max(0, self.health - amount)
            self.invincible = 10
            
            # Phase change at 50% health
            if self.health < self.max_health * 0.5 and self.phase == 1:
                self.phase = 2
                self.speed = 2
                # Phase change effect
                for _ in range(100):
                    self.particle_system.emit(
                        self.x + self.width // 2,
                        self.y + self.height // 2,
                        color=Colors.MAGENTA,
                        spread=10
                    )
            
            return True
        return False
    
    def draw(self, screen):
        # Main body
        pygame.draw.rect(screen, Colors.PURPLE, 
                        (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, Colors.WHITE, 
                        (self.x, self.y, self.width, self.height), 4)
        
        # Details
        pygame.draw.circle(screen, Colors.RED, 
                          (self.x + self.width // 2, self.y + 40), 20)
        pygame.draw.circle(screen, Colors.DARK_BLUE, 
                          (self.x + self.width // 2, self.y + 40), 10)
        
        # Cannons
        for offset in [-40, 0, 40]:
            pygame.draw.rect(screen, Colors.DARK_BLUE,
                           (self.x + self.width // 2 + offset - 5, 
                            self.y + self.height - 20, 10, 25))
        
        # Bullets
        for bullet in self.bullets:
            pygame.draw.circle(screen, bullet['color'],
                              (int(bullet['x']), int(bullet['y'])), bullet['size'])
        
        # Health bar
        health_width = 300
        pygame.draw.rect(screen, Colors.RED, 
                        (SCREEN_WIDTH // 2 - health_width // 2, 20, health_width, 25))
        health_ratio = max(0, self.health / self.max_health)
        pygame.draw.rect(screen, Colors.GREEN, 
                        (SCREEN_WIDTH // 2 - health_width // 2, 20, health_width * health_ratio, 25))
        pygame.draw.rect(screen, Colors.WHITE, 
                        (SCREEN_WIDTH // 2 - health_width // 2, 20, health_width, 25), 3)
        
        self.particle_system.draw(screen)

# Main game class
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Space Shooter - Advanced Version")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 36, bold=True)
        self.small_font = pygame.font.SysFont('Arial', 24)
        
        self.player = Player(SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT - 100)
        self.enemies = []
        self.boss = None
        self.particle_system = ParticleSystem()
        
        self.score = 0
        self.wave = 1
        self.enemies_spawned = 0
        self.enemies_to_spawn = 10
        self.spawn_cooldown = 0
        self.game_state = "playing"  # playing, game_over, victory
        self.background_stars = []
        self.create_stars()
        
        self.auto_shoot_timer = -1
         # Добавьте эту строку в __init__:
        self.sound_manager = SoundManager()
        
        # И передайте sound_manager в игрока:
        self.player = Player(SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT - 100, self.sound_manager)
    
    def create_stars(self):
        self.background_stars = []
        for _ in range(200):
            self.background_stars.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'size': random.randint(1, 3),
                'speed': random.uniform(0.1, 0.5),
                'brightness': random.randint(150, 255)
            })
    
    def spawn_enemy(self):
        if self.enemies_spawned < self.enemies_to_spawn:
            enemy_type = random.choices(
                ["normal", "fast", "tank"],
                weights=[0.6, 0.3, 0.1]
            )[0]
            
            enemy = Enemy(
                random.randint(50, SCREEN_WIDTH - 90),
                random.randint(-100, -40),
                enemy_type
            )
            self.enemies.append(enemy)
            self.enemies_spawned += 1
            self.spawn_cooldown = 30
    
    def check_collisions(self):
        # Player bullets vs enemies
        player_bullets_copy = self.player.bullets.copy()
        for bullet in player_bullets_copy:
            bullet_rect = pygame.Rect(bullet['x'], bullet['y'], bullet['width'], bullet['height'])
            
            # With regular enemies
            for enemy in self.enemies[:]:
                enemy_rect = pygame.Rect(enemy.x, enemy.y, 40, 40)
                if bullet_rect.colliderect(enemy_rect):
                    enemy.health -= bullet['damage']
                    self.particle_system.emit(
                        enemy.x + 20, enemy.y + 20,
                        count=10,
                        color=enemy.color,
                        spread=3
                    )

                    # 🔥 ЗВУК ПОПАДАНИЯ (маленький взрыв)
                    if self.sound_manager:
                        self.sound_manager.play_explosion(volume=0.3)
                    
                    if bullet in self.player.bullets:
                        self.player.bullets.remove(bullet)
                    
                    if enemy.health <= 0:
                        self.player.add_exp(enemy.value)
                        self.score += enemy.value
                        self.particle_system.emit(
                            enemy.x + 20, enemy.y + 20,
                            count=30,
                            color=Colors.YELLOW,
                            spread=5
                        )
                        self.enemies.remove(enemy)
                        # 💥 ЗВУК ВЗРЫВА ВРАГА (большой взрыв)
                        if self.sound_manager:
                            self.sound_manager.play_explosion(volume=0.8)
                    break
            

            # With boss
            if self.boss:
                boss_rect = pygame.Rect(self.boss.x, self.boss.y, self.boss.width, self.boss.height)
                if bullet_rect.colliderect(boss_rect):
                    if self.boss.take_damage(bullet['damage']):
                        self.particle_system.emit(
                            bullet['x'], bullet['y'],
                            count=15,
                            color=Colors.PURPLE,
                            spread=4
                        )
                    
                    if bullet in self.player.bullets:
                        self.player.bullets.remove(bullet)
        
        # Boss bullets vs player
        if self.boss:
            for bullet in self.boss.bullets[:]:
                bullet_rect = pygame.Rect(bullet['x'] - bullet['size'], 
                                        bullet['y'] - bullet['size'],
                                        bullet['size'] * 2, bullet['size'] * 2)
                player_rect = pygame.Rect(self.player.x, self.player.y, 
                                        self.player.width, self.player.height)
                
                if bullet_rect.colliderect(player_rect):
                    self.player.take_damage(20)
                    self.boss.bullets.remove(bullet)
                    self.particle_system.emit(
                        bullet['x'], bullet['y'],
                        count=20,
                        color=Colors.ORANGE,
                        spread=3
                    )
        
        # Enemy collision with player
        player_rect = pygame.Rect(self.player.x, self.player.y, 
                                self.player.width, self.player.height)
        for enemy in self.enemies[:]:
            enemy_rect = pygame.Rect(enemy.x, enemy.y, 40, 40)
            if player_rect.colliderect(enemy_rect):
                self.player.take_damage(10)
                enemy.health = 0
                self.particle_system.emit(
                    enemy.x + 20, enemy.y + 20,
                    count=40,
                    color=Colors.RED,
                    spread=6
                )
                if enemy in self.enemies:
                    self.enemies.remove(enemy)
    
    def draw_ui(self):
        # Player health bar
        health_width = 200
        health_ratio = max(0, self.player.health / self.player.max_health)
        pygame.draw.rect(self.screen, Colors.RED, (20, 20, health_width, 25))
        pygame.draw.rect(self.screen, Colors.GREEN, 
                        (20, 20, health_width * health_ratio, 25))
        pygame.draw.rect(self.screen, Colors.WHITE, (20, 20, health_width, 25), 3)
        
        # Experience bar
        exp_width = 200
        exp_ratio = min(1.0, self.player.exp / self.player.exp_to_next)
        pygame.draw.rect(self.screen, Colors.DARK_BLUE, (20, 55, exp_width, 15))
        pygame.draw.rect(self.screen, Colors.CYAN, 
                        (20, 55, exp_width * exp_ratio, 15))
        pygame.draw.rect(self.screen, Colors.WHITE, (20, 55, exp_width, 15), 1)
        
        # Text information
        health_text = self.font.render(f"{int(self.player.health)}/{self.player.max_health}", 
                                      True, Colors.WHITE)
        level_text = self.font.render(f"Уровень: {self.player.level}", True, Colors.YELLOW)
        score_text = self.font.render(f"Очки: {self.score}", True, Colors.WHITE)
        wave_text = self.font.render(f"Волна: {self.wave}", True, Colors.WHITE)
        
        self.screen.blit(health_text, (230, 18))
        self.screen.blit(level_text, (SCREEN_WIDTH - 120, 20))
        self.screen.blit(score_text, (SCREEN_WIDTH - 200, 60))
        self.screen.blit(wave_text, (SCREEN_WIDTH - 200, 100))
        
        # Stats
        stats_y = 130
        stats = [
            f"Дамаг: {10 + self.player.level * 2}",
            f"Скорость пули: {self.player.bullet_speed}",
            f"Радиус стрельбы: {60/self.player.shoot_delay:.1f}/sec"
        ]
        
        for i, stat in enumerate(stats):
            stat_text = self.small_font.render(stat, True, Colors.WHITE)
            self.screen.blit(stat_text, (SCREEN_WIDTH - 200, stats_y + i * 25))
    
    def draw_background(self):
        # Dark blue gradient background
        for y in range(SCREEN_HEIGHT):
            color_value = max(0, 25 - y // 30)
            color = (color_value, color_value + 10, color_value + 20)
            pygame.draw.line(self.screen, color, (0, y), (SCREEN_WIDTH, y))
        
        # Moving stars
        for star in self.background_stars:
            star['y'] += star['speed']
            if star['y'] > SCREEN_HEIGHT:
                star['y'] = 0
                star['x'] = random.randint(0, SCREEN_WIDTH)
            
            # Star twinkling
            brightness = star['brightness'] + random.randint(-20, 20)
            brightness = max(150, min(255, brightness))
            
            color = (brightness, brightness, brightness)
            pygame.draw.circle(self.screen, color, (int(star['x']), int(star['y'])), star['size'])
    
    def next_wave(self):
        self.wave += 1
        self.enemies_spawned = 0
        self.enemies_to_spawn = 10 + self.wave * 2
        
        # Spawn boss every 5 waves
        if self.wave % 5 == 0:
            self.boss = Boss()
        
        # Wave start effect
        for _ in range(100):
            self.particle_system.emit(
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2,
                color=Colors.CYAN,
                spread=10
            )
    
    def draw_game_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        game_over_text = self.font.render("GAME OVER", True, Colors.RED)
        score_text = self.font.render(f"Your Score: {self.score}", True, Colors.WHITE)
        wave_text = self.font.render(f"Wave Reached: {self.wave}", True, Colors.WHITE)
        restart_text = self.small_font.render("Press R to Restart", True, Colors.WHITE)
        quit_text = self.small_font.render("Press ESC to Quit", True, Colors.WHITE)
        
        texts = [game_over_text, score_text, wave_text, restart_text, quit_text]
        start_y = SCREEN_HEIGHT // 2 - len(texts) * 25
        
        for i, text in enumerate(texts):
            self.screen.blit(text, 
                           (SCREEN_WIDTH // 2 - text.get_width() // 2, 
                            start_y + i * 50))
    
    def draw_victory(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 50, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        victory_text = self.font.render("VICTORY!", True, Colors.YELLOW)
        boss_text = self.font.render("BOSS DEFEATED!", True, Colors.CYAN)
        score_text = self.font.render(f"Your Score: {self.score}", True, Colors.WHITE)
        restart_text = self.small_font.render("Press R to Restart", True, Colors.WHITE)
        quit_text = self.small_font.render("Press ESC to Quit", True, Colors.WHITE)
        
        texts = [victory_text, boss_text, score_text, restart_text, quit_text]
        start_y = SCREEN_HEIGHT // 2 - len(texts) * 25
        
        for i, text in enumerate(texts):
            self.screen.blit(text, 
                           (SCREEN_WIDTH // 2 - text.get_width() // 2, 
                            start_y + i * 50))
    
    def run(self):
        running = True
        
        while running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.player.shoot()
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_r and self.game_state != "playing":
                        # Restart game
                        self.__init__()
                    elif event.key == pygame.K_p:
                        # Pause (can be implemented)
                        pass
            
            if self.game_state == "playing":
                # Movement
                keys = pygame.key.get_pressed()
                self.player.move(keys)
                
                # Auto shooting when space is held
                if keys[pygame.K_SPACE]:
                    self.player.shoot()
                
                # Automatic shooting (every 10 frames)
                # self.auto_shoot_timer += 1
                # if self.auto_shoot_timer >= 10:
                #     self.player.shoot()
                #     self.auto_shoot_timer = 0
                
                # Enemy spawning
                self.spawn_cooldown = max(0, self.spawn_cooldown - 1)
                if self.spawn_cooldown == 0 and self.enemies_spawned < self.enemies_to_spawn:
                    self.spawn_enemy()
                
                # Update objects
                self.player.update()
                
                # Update enemies
                enemies_to_remove = []
                for enemy in self.enemies:
                    if not enemy.update():
                        enemies_to_remove.append(enemy)
                for enemy in enemies_to_remove:
                    if enemy in self.enemies:
                        self.enemies.remove(enemy)
                
                # Update boss
                if self.boss:
                    if not self.boss.update():
                        self.boss = None
                        self.next_wave()  # Go to next wave after defeating boss
                
                self.particle_system.update()
                
                # Check collisions
                self.check_collisions()
                
                # Check if wave is complete
                if (len(self.enemies) == 0 and 
                    self.enemies_spawned >= self.enemies_to_spawn and 
                    not self.boss):
                    self.next_wave()
                
                # Check player death
                if self.player.health <= 0:
                    self.game_state = "game_over"
            
            # Drawing
            self.draw_background()
            
            # Draw game objects (in correct order)
            for enemy in self.enemies:
                enemy.draw(self.screen)
            
            if self.boss:
                self.boss.draw(self.screen)
            
            self.player.draw(self.screen)
            self.particle_system.draw(self.screen)
            
            # Draw UI
            self.draw_ui()
            
            # Draw game states
            if self.game_state == "game_over":
                self.draw_game_over()
            elif self.game_state == "victory":
                self.draw_victory()
            
            # Update display
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

# Run the game
if __name__ == "__main__":
    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"Error occurred: {e}")
        import traceback
        traceback.print_exc()
        pygame.quit()