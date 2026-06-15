from __future__ import annotations
from typing import List
from copy import deepcopy
import pygame
import random
from abc import ABC, abstractmethod

SZEROKOSC = 800
WYSOKOSC = 600






# 1. Baza dla wszystkich stanów gracza
class PlayerState(ABC):
    @abstractmethod
    def handle_collision(self, player) -> bool:
        "''Zwraca True, jeśli gra powinna się zakończyć"""
        pass

    @abstractmethod
    def get_color(self, default_color:tuple) -> tuple:
        pass

    # 2. KONKRETNY STAN: Normalny gracz


class NormalState(PlayerState):
    def handle_collision(self, player) -> bool:
        print("KONIEC GRY!")
        return False  # Ustawia 'uruchomiona = False' w pętli gry

    def get_color(self,default_color) -> tuple:
        return default_color  # Standardowy czarny kolor

    # 3. KONKRETNY STAN: Nieśmiertelny gracz (z czasem trwania)


class InvincibleState(PlayerState):
    def __init__(self, duration_frames=180):  # Np. 3 sekundy przy 60 FPS
        self.frames_left = duration_frames

    def handle_collision(self, player) -> bool:
        #print("BUM! Wróg odbija się od tarczy!")
        return True  # Ignorujemy obrażenia, gra toczy się dalej

    def get_color(self,default_color) -> tuple:
        # Możemy zrobić efekt migania tarczy!
        return (0, 191, 255)  # Świecący niebieski (Deep Sky Blue)



class Object(ABC):
    @abstractmethod
    def move(self,direction):
        pass


class Shield:
    def __init__(self):
        self.size = 20
        # Losujemy pozycję na ekranie (z bezpiecznym marginesem)
        x = random.randint(50, SZEROKOSC - 50)
        y = random.randint(50, WYSOKOSC - 150)  # Wyżej, tam gdzie latają wrogowie
        self.rect = pygame.Rect(x, y, self.size, self.size)
        self.color = (0, 191, 255)  # Niebieski kolor kółka

    def draw(self, surface: pygame.Surface):
        pygame.draw.circle(surface, self.color, self.rect.center, self.size // 2)



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
    def __init__(self, start_x: int, kolor: tuple):
        self.__size = 30
        self.__speed = 8
        self.state: PlayerState = NormalState()
        self.__kolor = kolor
        self.rect = pygame.Rect(start_x, WYSOKOSC - 70, self.__size, self.__size)

    def update_state(self):
        """Metoda wywoływana co klatkę w pętli gry"""
        if isinstance(self.state, InvincibleState):
            self.state.frames_left -= 1
            if self.state.frames_left <= 0:
                print("Tarcza wygasła!")
                self.state = NormalState()  # Powrót do normalności

    def move(self, direction: str):
        if direction == "right":
            self.rect.x += self.__speed
        elif direction == "left":
            self.rect.x -= self.__speed
        elif direction == "up":
            self.rect.y -= self.__speed  # W Pygame góra to odejmowanie Y
        elif direction == "down":
            self.rect.y += self.__speed  # W Pygame dół to dodawanie Y

    @property
    def x(self) -> int:
        return self.rect.x
    @property
    def y(self) -> int:
        return self.rect.y
    @property
    def size(self):
        return deepcopy(self.__size)

    @property
    def kolor(self):
        return deepcopy(self.__kolor)


# 1. Inicjalizacja
pygame.init()

# 2. Parametry okna

ekran = pygame.display.set_mode((SZEROKOSC, WYSOKOSC))
pygame.display.set_caption("Unikaj spadających kwadratów!")

# 3. Ustawienia gracza

# Przypisujemy graczom różne pozycje startowe i kolory bazowe
gracz1 = Player(SZEROKOSC // 4, (0, 0, 0))       # Gracz 1 - Czarny
gracz2 = Player(SZEROKOSC // 2, (0, 255, 0))     # Gracz 2 - Zielony

# 4. Ustawienia przeszkód
CZAS_SPAWNU = 60  # Co ile klatek pojawia się nowy wróg (ok. 0.5 sekundy)
licznik_czasu = 0
# 1. Inicjalizacja jednej wspólnej listy na wszystkich wrogów
wrogowie: list[Enemy] = []

#Kontrola pojawiania się tarcz
tarcze: list[Shield] = []
CZAS_SPAWNU_TARCZY = 300  # Nowa tarcza co 5 sekund (300 klatek / 60 FPS)
licznik_tarczy = 0

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
    # ruch gracza w / skjalllll
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

    # 3. NOWE: Generowanie tarcz w czasie
    licznik_tarczy += 1
    if licznik_tarczy >= CZAS_SPAWNU_TARCZY:
        tarcze.append(Shield())
        licznik_tarczy = 0

    # D. Logika wrogów i kolizje


    gracz1.update_state()
    gracz2.update_state()

    # zbieranie tarcz
    for tarcza in tarcze[:]:
        if gracz1.rect.colliderect(tarcza.rect):
            gracz1.state = InvincibleState(duration_frames=180)  # Dajemy tarczę na 3 sekundy
            tarcze.remove(tarcza)
            print("Gracz 1 zebrał tarczę!")
        elif gracz2.rect.colliderect(tarcza.rect):
            gracz2.state = InvincibleState(duration_frames=180)
            tarcze.remove(tarcza)
            print("Gracz 2 zebrał tarczę!")

    # B. Logika, Ruch i Kolizje z wrogami
    for wrog in wrogowie[:]:
        wrog.move()  # Wywołanie metody ruchu z klasy Enemy

        # Sprawdzenie kolizji
        if gracz1.rect.colliderect(wrog.rect):
            # Stan sam decyduje, czy gra się kończy!
            uruchomiona = gracz1.state.handle_collision(gracz1)
            if not uruchomiona: break

        if gracz2.rect.colliderect(wrog.rect):
            uruchomiona = gracz2.state.handle_collision(gracz2)
            if not uruchomiona: break

        # Usuwanie wrogów poza ekranem
        if wrog.rect.y > WYSOKOSC or wrog.rect.x > SZEROKOSC:
            wrogowie.remove(wrog)




    # E. Rysowanie
    ekran.fill((255, 255, 255))  # Białe tło

    # Rysujemy gracza (czarny)
    pygame.draw.rect(ekran, gracz1.state.get_color(gracz1.kolor), gracz1.rect)
    pygame.draw.rect(ekran, gracz2.state.get_color(gracz2.kolor), gracz2.rect)

    # C. Rysowanie wrogów
    for wrog in wrogowie:
        kolor = (255, 0, 0) if wrog.typ == "v" else (200, 0, 0)
        pygame.draw.rect(ekran, kolor, wrog.rect)

    for tarcza in tarcze:
        tarcza.draw(ekran)

    # F. Odświeżenie
    pygame.display.flip()
    zegar.tick(60)

pygame.quit()
