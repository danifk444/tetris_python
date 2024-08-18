import pygame
import random

pygame.init()

# Játékméret
szerkezet_szelesseg = 10
szerkezet_magassag = 20
meret = 30  #négyzetek mérete pixelben
ablak_szelesseg = szerkezet_szelesseg * meret
ablak_magassag = szerkezet_magassag * meret

# Színek meghatározása (R, G, B)
FEHER = (255, 255, 255)
FEKETE = (0, 0, 0)
PIROS = (255, 0, 0)
ZOLD = (0, 255, 0)
KEK = (0, 0, 255)
CIAN = (0, 255, 255)
SARGA = (255, 255, 0)
MAGENTA = (255, 0, 255)
NARANCS = (255, 165, 0)

# Tetrominók alakjai
# A tetrominó négy négyzetből álló geometriai alakzat, amelyek egymásra merőlegesen kapcsolódnak egymáshoz.
TETROMINOK = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[1, 0, 0], [1, 1, 1]],  # J
    [[0, 0, 1], [1, 1, 1]]  # L
]

SZINEK = [CIAN, SARGA, MAGENTA, ZOLD, PIROS, KEK, NARANCS]

# Ablak létrehozása
ablak = pygame.display.set_mode((ablak_szelesseg, ablak_magassag))
pygame.display.set_caption("Tetris")

# Futási idő
ora = pygame.time.Clock()


# Tetromino osztály
class Tetromino:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.forma = random.choice(TETROMINOK)
        self.szine = SZINEK[TETROMINOK.index(self.forma)]

    def rajzol(self, surface):
        for i, sor in enumerate(self.forma):
            for j, cell in enumerate(sor):
                if cell:
                    pygame.draw.rect(
                        surface,
                        self.szine,
                        pygame.Rect(
                            (self.x + j) * meret,
                            (self.y + i) * meret,
                            meret,
                            meret,
                        )
                    )

    def mozgat(self, dx, dy):
        if not self.utkozik(dx, dy):
            self.x += dx
            self.y += dy

    def utkozik(self, dx, dy):
        for i, sor in enumerate(self.forma):
            for j, cell in enumerate(sor):
                if cell:
                    uj_x = self.x + j + dx
                    uj_y = self.y + i + dy
                    if uj_x < 0 or uj_x >= szerkezet_szelesseg or uj_y >= szerkezet_magassag:
                        return True
                    if uj_y >= 0 and jatektabla[uj_y][uj_x]:
                        return True
        return False

    def forgat(self):
        eredeti_forma = self.forma
        self.forma = [list(sor) for sor in zip(*self.forma[::-1])]
        if self.utkozik(0, 0):
            self.forma = eredeti_forma


def sorok_eltavolitasa():
    global jatektabla
    uj_tablazat = [sor for sor in jatektabla if any(cell == 0 for cell in sor)]
    eltavolitott_sorok = szerkezet_magassag - len(uj_tablazat)
    uj_tablazat = [[0] * szerkezet_szelesseg for _ in range(eltavolitott_sorok)] + uj_tablazat
    jatektabla = uj_tablazat
    return eltavolitott_sorok > 0


def jatek_vege():
    return any(jatektabla[0])


def jatek():
    global jatektabla
    global pontok
    jatektabla = [[0 for _ in range(szerkezet_szelesseg)] for _ in range(szerkezet_magassag)]
    pontok = 0  # Inicializáljuk a pontszámot
    aktualis_tetromino = Tetromino(3, 0) # Új tetrominó generálása a felső sor közepén
    while True:
        for esemeny in pygame.event.get():
            if esemeny.type == pygame.QUIT:
                return False

            if esemeny.type == pygame.KEYDOWN:
                if esemeny.key == pygame.K_LEFT:
                    aktualis_tetromino.mozgat(-1, 0)
                if esemeny.key == pygame.K_RIGHT:
                    aktualis_tetromino.mozgat(1, 0)
                if esemeny.key == pygame.K_DOWN:
                    aktualis_tetromino.mozgat(0, 1)
                if esemeny.key == pygame.K_UP:
                    aktualis_tetromino.forgat()

        # Automatikus süllyedés
        if not aktualis_tetromino.utkozik(0, 1):
            aktualis_tetromino.mozgat(0, 1)
        else:
            for i, sor in enumerate(aktualis_tetromino.forma):
                for j, cell in enumerate(sor):
                    if cell:
                        jatektabla[aktualis_tetromino.y + i][aktualis_tetromino.x + j] = aktualis_tetromino.szine

            if jatek_vege():
                return True

            if sorok_eltavolitasa():
                pontok += 100  # Eltávolított soronként kapott pontszám

            aktualis_tetromino = Tetromino(3, 0)

        # A képernyő frissítése
        ablak.fill(FEKETE)

        # Tetromino rajzolása
        aktualis_tetromino.rajzol(ablak)

        # Játéktábla kirajzolása
        for i, sor in enumerate(jatektabla):
            for j, cell in enumerate(sor):
                if cell:
                    pygame.draw.rect(
                        ablak,
                        cell,
                        pygame.Rect(
                            j * meret,
                            i * meret,
                            meret,
                            meret,
                        )
                    )

        # Pontszám kirajzolása
        font = pygame.font.SysFont(None, 30)
        szoveg = font.render(f"Pontszám: {pontok}", True, FEHER)
        ablak.blit(szoveg, (10, 10))

        # Az ablak kirajzolása
        pygame.display.update()

        # FPS
        ora.tick(7)


def uzenet_kirajzolasa(ablak, uzenet, meret, szin, pozicio):
    font = pygame.font.SysFont(None, meret)
    szoveg = font.render(uzenet, True, szin)
    ablak.blit(szoveg, szoveg.get_rect(center=pozicio))


def start_kepernyo():
    while True:
        ablak.fill(FEKETE)
        uzenet_kirajzolasa(ablak, "Tetris", 50, FEHER, (ablak_szelesseg // 2, ablak_magassag // 3))
        uzenet_kirajzolasa(ablak, "Nyomj SPACE-t a kezdéshez", 30, FEHER, (ablak_szelesseg // 2, ablak_magassag // 2))
        pygame.display.update()

        for esemeny in pygame.event.get():
            if esemeny.type == pygame.QUIT:
                return False
            if esemeny.type == pygame.KEYDOWN:
                if esemeny.key == pygame.K_SPACE:
                    return True


def jatek_vege_kepernyo():
    while True:
        ablak.fill(FEKETE)
        uzenet_kirajzolasa(ablak, "Játék vége", 50, PIROS, (ablak_szelesseg // 2, ablak_magassag // 3))
        uzenet_kirajzolasa(ablak, f"Összegyűjtött pontok: {pontok}", 30, FEHER, (ablak_szelesseg // 2, ablak_magassag // 2))
        uzenet_kirajzolasa(ablak, "Nyomj R-t az újrakezdéshez", 30, FEHER, (ablak_szelesseg // 2, ablak_magassag // 2 + 50))
        uzenet_kirajzolasa(ablak, "Nyomj ESC-et a kilépéshez", 30, FEHER, (ablak_szelesseg // 2, ablak_magassag // 2 + 100))
        pygame.display.update()

        for esemeny in pygame.event.get():
            if esemeny.type == pygame.QUIT:
                return False
            if esemeny.type == pygame.KEYDOWN:
                if esemeny.key == pygame.K_r:
                    return True
                if esemeny.key == pygame.K_ESCAPE:
                    return False


# Fő program
while True:
    if not start_kepernyo():
        break
    if jatek():
        if not jatek_vege_kepernyo():
            break
    else:
        break

pygame.quit()
