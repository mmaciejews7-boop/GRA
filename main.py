from __future__ import annotations
from typing import List
from copy import deepcopy
import pygame
import random
from abc import ABC, abstractmethod

SZEROKOSC = 800
WYSOKOSC = 600

class Object(ABC):
    @abstractmethod
    def move(self,direction):
        pass



class Enemy(Object):
    def __init__(self):
        __size = 40
        __speed = 3

    def move(self,direction:str):
        pass

class Player(Object):
    def __init__(self):
        self.__size = 30
        self.__speed = 8
        self.__x = SZEROKOSC // 8 - self.__size// 2
        self.__y = WYSOKOSC - 70


    def move(self,direction:str):
        if direction == "right":
            self.__x = self.__x + self.__speed
        elif direction == "left":
            self.__x = self.__x - self.__speed
        elif direction == "up":
            self.__y = self.__y - self.__speed
        elif direction == "down":
            self.__y = self.__y + self.__speed

    @property
    def x(self) -> float:
        ret = deepcopy(self.__x)
        return ret
    @property
    def y(self) -> float:
        return deepcopy(self.__y)
    @property
    def size(self):
        return deepcopy(self.__size)



# 1. Inicjalizacja
pygame.init()

# 2. Parametry okna
'''
SZEROKOSC = 800
WYSOKOSC = 600
'''
ekran = pygame.display.set_mode((SZEROKOSC, WYSOKOSC))
pygame.display.set_caption("Unikaj spadających kwadratów!")

# 3. Ustawienia gracza
gracz1 = Player()
gracz2 = Player()
'''
ROZMIAR_GRACZA = 30
gracz1_x = SZEROKOSC // 8 - ROZMIAR_GRACZA // 2
gracz1_y = WYSOKOSC - 70
predkosc_gracza = 8

gracz2_x = SZEROKOSC // 2 - ROZMIAR_GRACZA // 2
gracz2_y = WYSOKOSC - 70
'''
# 4. Ustawienia przeszkód
ROZMIAR_WROGA = 40
predkosc_wroga = 3
wrogowie_v = []
wrogowie_h = []# Lista przechowująca aktywne przeszkody
CZAS_SPAWNU = 60  # Co ile klatek pojawia się nowy wróg (ok. 0.5 sekundy)
licznik_czasu = 0

# 5. Zegar
zegar = pygame.time.Clock()

# --- GŁÓWNA PĘTLA GRY ---
uruchomiona = True
while uruchomiona:
    # A. Obsługa zdarzeń
    for zdarzenie in pygame.event.get():
        if zdarzenie.type == pygame.QUIT:
            uruchomiona = False

    # B. Ruch gracza (A / D)
    klawisze = pygame.key.get_pressed()
    if klawisze[pygame.K_d] and gracz1.x > 0:
        gracz1.move("right")
    if klawisze[pygame.K_a] and gracz1.x < SZEROKOSC - gracz1.size:
        gracz1.move("left")
    # ruch gracza w / s
    if klawisze[pygame.K_s] and gracz1.y > 0:
        gracz1.move("down")
    if klawisze[pygame.K_w] and gracz1.y < WYSOKOSC - gracz1.size:
        gracz1.move("up")

# drugi gracz
    klawisze = pygame.key.get_pressed()
    if klawisze[pygame.K_l] and gracz2.x > 0:
        gracz2.move("right")
    if klawisze[pygame.K_j] and gracz2.x < SZEROKOSC - gracz2.size:
        gracz2.move("left")
    if klawisze[pygame.K_k] and gracz2.y > 0:
        gracz2.move("down")
    if klawisze[pygame.K_i] and gracz2.y < WYSOKOSC - gracz2.size:
        gracz2.move("up")


    # C. Generowanie przeszkód
    licznik_czasu += 1
    if licznik_czasu >= CZAS_SPAWNU:
        nowy_wrog_x = random.randint(0, SZEROKOSC - ROZMIAR_WROGA)
        nowy_wrog_y = random.randint(0, WYSOKOSC - ROZMIAR_WROGA)
        # Dodajemy listę [x, y] dla każdego nowego wroga
        wrogowie_v.append([nowy_wrog_x, -ROZMIAR_WROGA])
        wrogowie_h.append([-ROZMIAR_WROGA,nowy_wrog_y])
        licznik_czasu = 0

    # D. Logika wrogów i kolizje
    gracz_rect1 = pygame.Rect(gracz1.x, gracz1.y, gracz1.size, gracz1.size)
    gracz_rect2 = pygame.Rect(gracz2.x, gracz2.y, gracz2.size, gracz2.size)

    for wrog in wrogowie_v[:]:  # Używamy kopii listy [:], aby móc bezpiecznie usuwać elementy
        wrog[1] += predkosc_wroga  # Zwiększamy Y (spadanie)


        # Tworzymy rect dla wroga do wykrywania kolizji
        wrog_rect = pygame.Rect(wrog[0], wrog[1], ROZMIAR_WROGA, ROZMIAR_WROGA)

        # Sprawdzanie kolizji
        if gracz_rect1.colliderect(wrog_rect):
            print("KONIEC GRY! Zostałeś trafiony.")
            uruchomiona = False

        if gracz_rect2.colliderect(wrog_rect):
            print("KONIEC GRY! Zostałeś trafiony.")
            uruchomiona = False

        # Usuwanie wrogów, którzy wylecieli za ekran
        if wrog[1] > WYSOKOSC:
            wrogowie_v.remove(wrog)

    for wrog in wrogowie_h[:]:  # Używamy kopii listy [:], aby móc bezpiecznie usuwać elementy
        wrog[0] += predkosc_wroga  # Zwiększamy X (leci w lewo)

        # Tworzymy rect dla wroga do wykrywania kolizji
        wrog_rect = pygame.Rect(wrog[0], wrog[1], ROZMIAR_WROGA, ROZMIAR_WROGA)

        # Sprawdzanie kolizji
        if gracz_rect1.colliderect(wrog_rect):
            print("KONIEC GRY! Zostałeś trafiony.")
            uruchomiona = False

        if gracz_rect2.colliderect(wrog_rect):
            print("KONIEC GRY! Zostałeś trafiony.")
            uruchomiona = False

        # Usuwanie wrogów, którzy wylecieli za ekran
        if wrog[1] > WYSOKOSC:
            wrogowie_h.remove(wrog)

    # E. Rysowanie
    ekran.fill((255, 255, 255))  # Białe tło

    # Rysujemy gracza (czarny)
    pygame.draw.rect(ekran, (0, 0, 0), gracz_rect1)
    pygame.draw.rect(ekran, (0, 255, 0), gracz_rect2)

    # Rysujemy wrogów (czerwoni)
    for wrog in wrogowie_v:
        pygame.draw.rect(ekran, (255, 0, 0), (wrog[0], wrog[1], ROZMIAR_WROGA, ROZMIAR_WROGA))

    for wrog in wrogowie_h:
        pygame.draw.rect(ekran, (200, 0, 0), (wrog[0], wrog[1], ROZMIAR_WROGA, ROZMIAR_WROGA))

    # F. Odświeżenie
    pygame.display.flip()
    zegar.tick(60)

pygame.quit()

