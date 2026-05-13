import pygame
import random

# 1. Inicjalizacja
pygame.init()
random
# 2. Parametry okna
SZEROKOSC = 800
WYSOKOSC = 600
ekran = pygame.display.set_mode((SZEROKOSC, WYSOKOSC))
pygame.display.set_caption("Unikaj spadających kwadratów!")

# 3. Ustawienia gracza
ROZMIAR_GRACZA = 30
gracz1_x = SZEROKOSC // 8 - ROZMIAR_GRACZA // 2
gracz1_y = WYSOKOSC - 70
predkosc_gracza = 8

gracz2_x = SZEROKOSC // 2 - ROZMIAR_GRACZA // 2
gracz2_y = WYSOKOSC - 70

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
    if klawisze[pygame.K_a] and gracz1_x > 0:
        gracz1_x -= predkosc_gracza
    if klawisze[pygame.K_d] and gracz1_x < SZEROKOSC - ROZMIAR_GRACZA:
        gracz1_x += predkosc_gracza
    # ruch gracza w / s
    if klawisze[pygame.K_w] and gracz1_y > 0:
        gracz1_y -= predkosc_gracza
    if klawisze[pygame.K_s] and gracz1_y < WYSOKOSC - ROZMIAR_GRACZA:
        gracz1_y += predkosc_gracza

# drugi gracz
    if klawisze[pygame.K_j] and gracz2_x > 0:
        gracz2_x -= predkosc_gracza
    if klawisze[pygame.K_l] and gracz2_x < SZEROKOSC - ROZMIAR_GRACZA:
        gracz2_x += predkosc_gracza

    if klawisze[pygame.K_i] and gracz2_y > 0:
        gracz2_y -= predkosc_gracza
    if klawisze[pygame.K_k] and gracz2_y < WYSOKOSC - ROZMIAR_GRACZA:
        gracz2_y += predkosc_gracza


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
    gracz_rect1 = pygame.Rect(gracz1_x, gracz1_y, ROZMIAR_GRACZA, ROZMIAR_GRACZA)
    gracz_rect2 = pygame.Rect(gracz2_x, gracz2_y, ROZMIAR_GRACZA, ROZMIAR_GRACZA)

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

