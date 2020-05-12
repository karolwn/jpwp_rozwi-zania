#OK!
import socket
import threading
from gracz import Gracz
from gra import Gra
import json


class Server(object):
    GRACZE = 2 # Ilość klientów, która musi podłączyć się do serwera, aby gra rozpoczeła się

    def __init__(self):
        self.kolejka = []
        self.numer_gry = 0

    def gracz_thread(self, polaczenie, gracz):
       
        while True:
            try:
                try:
                    dane = polaczenie.recv(1024)
                    dane = json.loads(dane.decode())
                except Exception as e:
                    break

                keys = [int(key) for key in dane.keys()]
                wyslij_informacje = {key:[] for key in keys}
                ostatni_gracz = None

                for key in keys:
                    if key == -1:
                        if gracz.gra:
                            wyslij = {gracz.get_nazwa():gracz.get_wynik() for gracz in gracz.gra.gracze}
                            wyslij_informacje[-1] = wyslij
                        else:
                            wyslij_informacje[-1] = []

                    if gracz.gra:
                        if key == 0:
                            poprawna_odpowiedz = gracz.gra.proba_zgadniecia(gracz, dane['0'][0])
                            wyslij_informacje[0] = poprawna_odpowiedz
                        elif key == 1:
                            pomin_runde = gracz.gra.pomin(gracz)
                            wyslij_informacje[1] = pomin_runde
                        elif key == 2:
                            chat_tablica = gracz.gra.runda.chat.get_chat()
                            wyslij_informacje[2] = chat_tablica
                        elif key == 3:
                            tablica = gracz.gra.tablica.get_tablica()
                            if ostatni_gracz != tablica:
                                ostatni_gracz = tablica
                                wyslij_informacje[3] = tablica

                        elif key == 4:
                            wyniki = gracz.gra.get_wyniki_gracza()
                            wyslij_informacje[4] = wyniki
                       # Tu napisz kod obsługujący klucz 5
                        elif key == 5:
                            wyslij_informacje[5] = gracz.gra.liczba_rund

                        elif key == 6:
                            haslo = gracz.gra.runda.haslo
                            wyslij_informacje[6] = haslo
                        elif key == 7:
                            liczba_pominiec = gracz.gra.runda.liczba_pominiec
                            wyslij_informacje[7] = liczba_pominiec
                        elif key == 8:
                            if gracz.gra.runda.rysujacy == gracz:
                                x, y, kolor = dane['8'][:3]
                                gracz.gra.update_tablica(x, y, kolor)
                        elif key == 9:
                            t = gracz.gra.runda.czas
                            wyslij_informacje[9] = t
                        elif key == 10:
                            gracz.gra.tablica.czyszczenie()
                        elif key == 11:
                            wyslij_informacje[11] = gracz.gra.runda.rysujacy == gracz

                wyslij_informacje = json.dumps(wyslij_informacje)
                polaczenie.sendall(wyslij_informacje.encode() + ".".encode())
            except Exception as e:
                print(e)
                break

        if gracz.gra:
            gracz.gra.rozlaczony_gracz(gracz)

        if gracz in self.kolejka:
            self.kolejka.remove(gracz)

        print(F" {gracz.nazwa} rozłączył się z serwerem")
        polaczenie.close()

    def obsluga_kolejki(self, gracz):

        self.kolejka.append(gracz)

        if len(self.kolejka) >= self.GRACZE:
            gra = Gra(self.numer_gry, self.kolejka[:])

            for g in gra.gracze:
                g.zacznij_gre(gra)

            self.numer_gry += 1
            self.kolejka = []
            print(f"Gra {self.numer_gry - 1} rozpoczeła się")

    def obsluga_polaczenia(self, polaczenie, adres):

        try:
            dane = polaczenie.recv(1024)
            nazwa = str(dane.decode())
            if not nazwa:
                raise Exception("Brak nazwy")

            polaczenie.sendall("1".encode())

            gracz = Gracz(adres, nazwa)
            self.obsluga_kolejki(gracz)
            thread = threading.Thread(target=self.gracz_thread, args=(polaczenie, gracz))
            thread.start()
        except Exception as e:
            print(e)
            polaczenie.close()

    def polaczenie_thread(self):
        server = "127.0.0.1"
        port = 8000

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            s.bind((server, port))
        except socket.error as e:
            str(e)

        s.listen(2)
        print("Czekanie na nawiązanie połączenia")

        while True:
            polaczenie, adres = s.accept()
            print("Nawiązano nowe połączenie.")

            self.obsluga_polaczenia(polaczenie, adres)


if __name__ == "__main__":
    s = Server()
    thread = threading.Thread(target=s.polaczenie_thread)
    thread.start()
