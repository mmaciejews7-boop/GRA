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
    def __init__(self, typ: str):
        self.size = 40
        self.speed = 3
        self.typ = typ  # "v" - leci w pionie, "h" - leci w poziomie

        # Losowanie pozycji startowej w zależności od typu wroga
        if self.typ == "v":
            x = random.randint(0, SZEROKOSC - self.size)
            y = -self.size
        else:  # "h"
            x = -self.size
            y = random.randint(0, WYSOKOSC - self.size)

        self.rect = pygame.Rect(x, y, self.size, self.size)

    def move(self, direction: str = ""):
        # Wróg sam wie, w którą stronę ma się poruszać na podstawie swojego typu
        if self.typ == "v":
            self.rect.y += self.speed
        elif self.typ == "h":
            self.rect.x += self.speed



class Player(Object):
    def __init__(self):
        self.__size = 30
        self.__speed = 8
        self.__x = SZEROKOSC // 8 - self.__size// 2
        self.__y = WYSOKOSC - 70


    def move(self, direction: str):
        if direction == "right":
            self.__x += self.__speed
        elif direction == "left":
            self.__x -= self.__speed
        elif direction == "up":
            self.__y -= self.__speed  # W Pygame góra to odejmowanie Y
        elif direction == "down":
            self.__y += self.__speed  # W Pygame dół to dodawanie Y

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
CZAS_SPAWNU = 60  # Co ile klatek pojawia się nowy wróg (ok. 0.5 sekundy)
licznik_czasu = 0
# 1. Inicjalizacja jednej wspólnej listy na wszystkich wrogów
wrogowie: list[Enemy] = []

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
    if klawisze[pygame.K_a] and gracz1.x > 0:
        gracz1.move("left")
    if klawisze[pygame.K_d] and gracz1.x < SZEROKOSC - gracz1.size:
        gracz1.move("right")
    # ruch gracza w / s
    if klawisze[pygame.K_w] and gracz1.y > 0:
        gracz1.move("up")
    if klawisze[pygame.K_s] and gracz1.y < WYSOKOSC - gracz1.size:
        gracz1.move("down")

# drugi gracz
    klawisze = pygame.key.get_pressed()
    if klawisze[pygame.K_j] and gracz2.x > 0:
        gracz2.move("left")
    if klawisze[pygame.K_l] and gracz2.x < SZEROKOSC - gracz2.size:
        gracz2.move("right")
    if klawisze[pygame.K_i] and gracz2.y > 0:
        gracz2.move("up")
    if klawisze[pygame.K_k] and gracz2.y < WYSOKOSC - gracz2.size:
        gracz2.move("down")

    # --- KOD GENERUJĄCY I ZARZĄDZAJĄCY PRZESZKODAMI ---

    # A. Generowanie (Spawn)
    licznik_czasu += 1
    if licznik_czasu >= CZAS_SPAWNU:
        wrogowie.append(Enemy(typ="v"))
        wrogowie.append(Enemy(typ="h"))
        licznik_czasu = 0

    # D. Logika wrogów i kolizje
    gracz_rect1 = pygame.Rect(gracz1.x, gracz1.y, gracz1.size, gracz1.size)
    gracz_rect2 = pygame.Rect(gracz2.x, gracz2.y, gracz2.size, gracz2.size)

    # B. Logika, Ruch i Kolizje
    for wrog in wrogowie[:]:
        wrog.move()  # Wywołanie metody ruchu z klasy Enemy

        # Sprawdzenie kolizji z graczami
        if gracz_rect1.colliderect(wrog.rect) or gracz_rect2.colliderect(wrog.rect):
            print("KONIEC GRY!")
            uruchomiona = False

        # Usuwanie wrogów poza ekranem
        if wrog.rect.y > WYSOKOSC or wrog.rect.x > SZEROKOSC:
            wrogowie.remove(wrog)




    # E. Rysowanie
    ekran.fill((255, 255, 255))  # Białe tło

    # Rysujemy gracza (czarny)
    pygame.draw.rect(ekran, (0, 0, 0), gracz_rect1)
    pygame.draw.rect(ekran, (0, 255, 0), gracz_rect2)

    # C. Rysowanie wrogów
    for wrog in wrogowie:
        kolor = (255, 0, 0) if wrog.typ == "v" else (200, 0, 0)
        pygame.draw.rect(ekran, kolor, wrog.rect)

    # F. Odświeżenie
    pygame.display.flip()
    zegar.tick(60)

pygame.quit()

