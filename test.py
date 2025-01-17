import random
import os

class Labyrint:
    def __init__(self):
        self.nuvarande_rum = "start"
        self.max_drag = 25
        self.kvarvarande_drag = self.max_drag
        self.uppklarade_utmaningar = set()
        self.minst_en_utmaning_klarad = False
        self.rum = self.initiera_rum()
        self.spelinstruktioner()

    def rensa_skarm(self):
        """Rensar terminalfönstret för bättre läsbarhet"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def spelinstruktioner(self):
        """Läser in och visar spelets instruktioner från readme.txt om filen finns"""
        filnamn = "readme.txt"
        if os.path.exists(filnamn):
            with open(filnamn, 'r', encoding="utf-8") as file:
                print(file.read())
        else:
            print("❌ Instruktionsfil saknas! Se till att 'readme.txt' finns i spelets katalog.")

    def initiera_rum(self):
        return {
            "start": {
                "namn": "Startrum",
                "beskrivning": """
                Du vaknar upp i ett dunkelt rum. Väggarna är täckta av gamla ristningar.
                Tre dörrar omger dig, men vilken leder vidare... och vilken till din undergång?
                """,
                "val": {
                    "vänster": ("gåta_rum", "Du går in i ett rum fyllt av viskande röster."),
                    "rakt fram": ("fälla_rum", "Du går in i ett smalt rum med ett förrädiskt golv.")
                }
            },
            "gåta_rum": {
                "namn": "Gåtans rum",
                "beskrivning": """
                En gammal staty rör sig plötsligt och talar:
                'För att passera måste du svara på min gåta.'
                """,
                "val": {
                    "höger": ("korridor_1", "Du fortsätter genom en smal passage."),
                    "tillbaka": ("start", "Du går tillbaka till start.")
                },
                "utmaning": lambda: self.gåta_utmaning()
            },
            "fälla_rum": {
                "namn": "Fällans rum",
                "beskrivning": """
                Golvet knakar under dina fötter. En felaktig rörelse kan bli din sista.
                """,
                "val": {
                    "tillbaka": ("start", "Du går tillbaka till start.")
                },
                "utmaning": lambda: self.falla_utmaning()
            },
            "korridor_1": {
                "namn": "Spegelrummet",
                "beskrivning": """
                Du kliver in i ett rum fyllt av speglar. Din spegelbild rör sig inte alltid som du...
                """,
                "val": {
                    "rakt fram": ("korridor_2", "Du fortsätter djupare in i labyrinten."),
                },
                "utmaning": lambda: self.spegel_utmaning()
            },
            "korridor_2": {
                "namn": "Labyrintens hjärta",
                "beskrivning": """
                Du står inför en vägg av symboler. Endast den med starkt minne kan hitta rätt.
                """,
                "val": {
                    "rakt fram": ("korridor_3", "Du rör dig försiktigt vidare."),
                    "tillbaka": ("korridor_1", "Du går tillbaka.")
                },
                "utmaning": lambda: self.minnes_utmaning()
            },
            "korridor_3": {
                "namn": "Dörrarnas prövning",
                "beskrivning": """
                Tre dörrar står framför dig. Två leder till undergång, en leder ut...
                Men vilken?
                """,
                "val": {
                    "rakt fram": ("utgång", "Du öppnar en av dörrarna och går vidare."),
                    "tillbaka": ("korridor_2", "Du tvekar och går tillbaka.")
                },
                "utmaning": lambda: self.dorrar_utmaning()
            },
            "utgång": {
                "namn": "Utgång",
                "beskrivning": """
                Du känner vinden mot ditt ansikte. Du har hittat utgången och överlevt labyrinten!
                """,
                "val": {}
            }
        }

    def spela(self):
        self.rensa_skarm()
        input("\nTryck ENTER för att börja spelet...")

        while self.nuvarande_rum != "utgång" and self.kvarvarande_drag > 0:
            self.visa_rum()
            if "utmaning" in self.rum[self.nuvarande_rum]:
                self.kontrollera_utmaning()
            val = input("\nVilken väg väljer du? ").lower()
            self.flytta(val)

        self.visa_slutresultat()

    def visa_rum(self):
        self.rensa_skarm()
        rum = self.rum[self.nuvarande_rum]
        print(f"\n{rum['namn'].upper()}")
        print(rum['beskrivning'])
        print(f"\nDrag kvar: {self.kvarvarande_drag}")

    def flytta(self, riktning):
        rum = self.rum[self.nuvarande_rum]
        if riktning in rum["val"]:
            nasta_rum, meddelande = rum["val"][riktning]
            print(f"\n{meddelande}")
            input("\nTryck ENTER för att fortsätta...")
            self.nuvarande_rum = nasta_rum
            self.kvarvarande_drag -= 1
        else:
            print("\n❌ Det går inte att gå åt det hållet!")
            input("\nTryck ENTER för att fortsätta...")

    def kontrollera_utmaning(self):
        rum = self.rum[self.nuvarande_rum]
        if "utmaning" in rum and self.nuvarande_rum not in self.uppklarade_utmaningar:
            if rum["utmaning"]():
                self.uppklarade_utmaningar.add(self.nuvarande_rum)
            else:
                self.kvarvarande_drag -= 1
                self.nuvarande_rum = "start"

    def spegel_utmaning(self):
        print("\nVilken av speglarna visar din riktiga spegelbild?")
        svar = input("Skriv 'vänster', 'mitten' eller 'höger': ").lower()
        return svar == "mitten"

    def minnes_utmaning(self):
        symboler = ["✦", "◼", "◆", "★", "⬟"]
        rätt_symbol = random.choice(symboler)
        print(f"\nMemorera denna symbol: {rätt_symbol}")
        input("Tryck ENTER och försök minnas...")
        self.rensa_skarm()
        gissning = input("Vilken symbol visades? ")
        return gissning == rätt_symbol

    def dorrar_utmaning(self):
        rätt_dörr = str(random.randint(1, 3))
        val = input("\nVälj en dörr (1, 2 eller 3): ")
        return val == rätt_dörr

    def visa_slutresultat(self):
        self.rensa_skarm()
        print("\nGRATTIS! Du har överlevt labyrinten!" if self.nuvarande_rum == "utgång" else "\nGAME OVER!")

if __name__ == "__main__":
    Labyrint().spela()
