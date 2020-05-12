import pygame
from przyciski import Przycisk, PrzyciskTekstowy
from tablica import Tablica
from pasek_gorny import PasekGorny
from ranking import Ranking
from gracz import Gracz
from pasek_dolny import PasekDolny
from chat import Chat


class Gra:
    TLO = (255, 255, 255)
    KOLORY = { (255, 255, 255): 0,     (0, 0, 0): 1, } # Słownik przechowujący biały i czarny

    def __init__(self, win, connection=None):
        pygame.font.init()
        self.connection = connection
        self.win = win #okno do wyswietlania
        #inicjalizacja parametrow
        self.ranking = Ranking(50, 125)
        self.tablica = Tablica(305, 125)
        self.pasek_gorny = PasekGorny(50, 10, 990, 100)
        self.pasek_gorny.zmiana_rundy(1)
        self.gracze = []
        self.pomin_button = PrzyciskTekstowy(810, 555, 225, 50, (255, 255, 0), "Pomin")
        self.pasek_dolny = PasekDolny(305, 880, self)
        self.chat = Chat(810, 125)
        self.kolor_rysowania = (0, 0, 0)
        self.rysujacy = False

    def dodaj_gracza(self, gracz):
        self.gracze.append(gracz)
        self.ranking.dodaj_gracza(gracz)

    def rysuj(self):

        self.win.fill(self.TLO)
        self.ranking.rysuj(self.win)
        self.pasek_gorny.rysuj(self.win)
        self.tablica.rysuj(self.win)
        self.pomin_button.rysuj(self.win)

        if self.rysujacy:
            self.pasek_dolny.rysuj(self.win)
        self.chat.rysuj(self.win)
        pygame.display.update()

    def obsluga_przyciskow(self):
       
        mouse = pygame.mouse.get_pos()
        # pominięcie rundy
        if self.pomin_button.klikniecie(*mouse) and not self.rysujacy:
            pominiete_rundy = self.connection.send({1: []})

        kliknieta_tablica = self.tablica.klikniecie(*mouse)
        #rysowanie
        if kliknieta_tablica:
            self.tablica.update(*kliknieta_tablica, self.kolor_rysowania)
            self.connection.send({8: [*kliknieta_tablica, self.KOLORY[tuple(self.kolor_rysowania)]]})

    def run(self):
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(60)

            try:
               
                odpowiedz = self.connection.send({3: []})
                if odpowiedz:
                    self.tablica.podzielona_tablica = odpowiedz
                    self.tablica.dzielenie_tablicy()

               
                odpowiedz = self.connection.send({9: []})
                self.pasek_gorny.czas = odpowiedz

               
                ################################################
                #KOD DO ZADANIA 3
                ###############################################

                odpowiedz = self.connection.send({2: []})
                self.chat.update_chat(odpowiedz)
              

              
                self.pasek_gorny.haslo = self.connection.send({6: []})
                self.pasek_gorny.runda = self.connection.send({5: []})
                self.rysujacy = self.connection.send({11: []})
                self.pasek_gorny.rysujacy = self.rysujacy
                self.pasek_gorny.max_rund = len(self.gracze)

                odpowiedz = self.connection.send({4: []})
                for gracz in self.gracze:
                    if odpowiedz != []:
                        gracz.ustaw_wynik(odpowiedz[gracz.get_nazwa()])

               
            except:
                run = False
                break

            self.rysuj()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

                if pygame.mouse.get_pressed()[0]:
                    self.obsluga_przyciskow()
                    self.pasek_dolny.obsluga_przyciskow()

                if event.type == pygame.KEYDOWN:
                    if not self.rysujacy:
                        if event.key == pygame.K_RETURN:
                            self.connection.send({0: [self.chat.pisanie]})
                            self.chat.pisanie = ""
                        else:
                         
                            key_name = pygame.key.name(event.key)

                          
                            key_name = key_name.lower()
                            self.chat.type(key_name)

        pygame.quit()