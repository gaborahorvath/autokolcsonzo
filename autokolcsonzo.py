from abc import ABC
from datetime import datetime, timedelta


# --- 1. OSZTÁLYOK DEFINIÁLÁSA ---

class Auto(ABC):
    """Absztrakt ősosztály az autók számára."""

    def __init__(self, rendszam: str, tipus: str, berleti_dij: int):
        self._rendszam = rendszam
        self._tipus = tipus
        self._berleti_dij = berleti_dij

    @property
    def rendszam(self):
        return self._rendszam

    @property
    def tipus(self):
        return self._tipus

    @property
    def berleti_dij(self):
        return self._berleti_dij


class Szemelyauto(Auto):
    """Személyautó osztály, specifikus attribútummal."""

    def __init__(self, rendszam: str, tipus: str, berleti_dij: int, utasok_szama: int):
        super().__init__(rendszam, tipus, berleti_dij)
        self._utasok_szama = utasok_szama


class Teherauto(Auto):
    """Teherautó osztály, specifikus attribútummal."""

    def __init__(self, rendszam: str, tipus: str, berleti_dij: int, teherbiras_kg: int):
        super().__init__(rendszam, tipus, berleti_dij)
        self._teherbiras_kg = teherbiras_kg


class Berles:
    """Egy adott autó egy adott napra történő bérlését tárolja."""

    def __init__(self, auto: Auto, datum: datetime):
        self._auto = auto
        self._datum = datum

    @property
    def auto(self):
        return self._auto

    @property
    def datum(self):
        return self._datum


class Autokolcsonzo:
    """A kölcsönzőt és a hozzá tartozó műveleteket kezelő osztály."""

    def __init__(self, nev: str):
        self._nev = nev
        self._autok = []
        self._berlesek = []

    def auto_hozzaadasa(self, auto: Auto):
        self._autok.append(auto)

    def berles(self, rendszam: str, datum_str: str) -> int:
        """Autó bérlése egy adott dátumra, validációval."""
        try:
            datum = datetime.strptime(datum_str, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Hibás dátum formátum! Használja az ÉÉÉÉ-HH-NN formátumot.")

        if datum.date() < datetime.now().date():
            raise ValueError("Múltbeli dátumra nem lehet autót bérelni!")

        keresett_auto = next((a for a in self._autok if a.rendszam == rendszam), None)
        if not keresett_auto:
            raise ValueError("Nem található ilyen rendszámú autó a kölcsönzőben.")

        # Ellenőrizzük, hogy az autó az adott napon ki van-e már adva
        for b in self._berlesek:
            if b.auto.rendszam == rendszam and b.datum.date() == datum.date():
                raise ValueError("Az autó ezen a napon már ki van bérelve.")

        uj_berles = Berles(keresett_auto, datum)
        self._berlesek.append(uj_berles)
        return keresett_auto.berleti_dij

    def lemondas(self, rendszam: str, datum_str: str):
        """Bérlés lemondása, ellenőrzi a létezést."""
        try:
            datum = datetime.strptime(datum_str, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Hibás dátum formátum! Használja az ÉÉÉÉ-HH-NN formátumot.")

        for b in self._berlesek:
            if b.auto.rendszam == rendszam and b.datum.date() == datum.date():
                self._berlesek.remove(b)
                return True

        raise ValueError("Nem található ilyen bérlés a rendszerben, így nem lehet lemondani.")

    def listazas(self):
        """Aktuális bérlések listázása."""
        if not self._berlesek:
            print("Jelenleg nincs aktív bérlés.")
            return

        print(f"\n--- {self._nev} Aktuális Bérlései ---")
        for b in self._berlesek:
            print(f"Dátum: {b.datum.strftime('%Y-%m-%d')} | Autó: {b.auto.rendszam} ({b.auto.tipus})")
        print("--------------------------------------")


# --- 2. FELHASZNÁLÓI INTERFÉSZ ÉS ELŐKÉSZÍTÉS ---

def main():
    # Rendszer előkészítése
    kolcsonzo = Autokolcsonzo("SuperCars Kölcsönző")

    # 3 autó hozzáadása
    auto1 = Szemelyauto("ABC-123", "Ford Focus", 15000, 5)
    auto2 = Szemelyauto("XYZ-987", "Skoda Octavia", 18000, 5)
    auto3 = Teherauto("TEH-001", "Ford Transit", 25000, 1500)

    kolcsonzo.auto_hozzaadasa(auto1)
    kolcsonzo.auto_hozzaadasa(auto2)
    kolcsonzo.auto_hozzaadasa(auto3)

    # Dátumok generálása a 4 előre betöltött bérléshez (hogy mindig a jövőben legyenek)
    ma = datetime.now()
    datum1 = (ma + timedelta(days=2)).strftime("%Y-%m-%d")
    datum2 = (ma + timedelta(days=5)).strftime("%Y-%m-%d")

    # 4 előre definiált bérlés felvitele
    kolcsonzo.berles("ABC-123", datum1)
    kolcsonzo.berles("ABC-123", datum2)
    kolcsonzo.berles("XYZ-987", datum1)
    kolcsonzo.berles("TEH-001", datum2)

    # CLI Menü
    while True:
        print("\n=== AUTÓKÖLCSÖNZŐ RENDSZER ===")
        print("1. Autó bérlése")
        print("2. Bérlés lemondása")
        print("3. Bérlések listázása")
        print("4. Kilépés")

        valasztas = input("Kérem válasszon egy opciót (1-4): ")

        if valasztas == "1":
            print("\nElérhető autók rendszámai: ABC-123, XYZ-987, TEH-001")
            rendszam = input("Kérem adja meg a bérelni kívánt autó rendszámát: ").upper()
            datum = input("Kérem adja meg a bérlés dátumát (ÉÉÉÉ-HH-NN): ")
            try:
                ar = kolcsonzo.berles(rendszam, datum)
                print(f"Sikeres bérlés! A fizetendő összeg: {ar} Ft.")
            except ValueError as e:
                print(f"Hiba történt: {e}")

        elif valasztas == "2":
            rendszam = input("Kérem adja meg a lemondani kívánt autó rendszámát: ").upper()
            datum = input("Kérem adja meg a bérlés dátumát (ÉÉÉÉ-HH-NN): ")
            try:
                kolcsonzo.lemondas(rendszam, datum)
                print("A bérlés sikeresen lemondva.")
            except ValueError as e:
                print(f"Hiba történt: {e}")

        elif valasztas == "3":
            kolcsonzo.listazas()

        elif valasztas == "4":
            print("Kilépés a rendszerből. Viszontlátásra!")
            break
        else:
            print("Érvénytelen választás. Kérem 1 és 4 közötti számot adjon meg.")


if __name__ == "__main__":
    main()