# Lägg in kommentarer i koden
# Utöka antalet rum om du siktar mot C eller A
#Flödeschema

import random
import os


class Labyrint:
    def __init__(self):
        self.nuvarande_rum = "start"
        self.max_drag = 20
        self.kvarvarande_drag = self.max_drag
        self.uppklarade_utmaningar = set()
        self.minst_en_utmaning_klarad = False
        self.rum = self.initiera_rum()

    def rensa_skarm(self):
        """Rensar terminalfönstret för bättre läsbarhet"""
        os.system('cls' if os.name == 'nt' else 'clear') 

    def spelinstruktioner(self):
        with open('readme.txt', 'r', encoding="utf-8") as file:  
            data = file.read()  
            print(data) 

    def visa_karta(self):
        """Visar en enkel ASCII-karta över spelarens position"""
        karta = {
            "start": """
            [*START*]---[GÅTA]
               |           |
            [FÄLLA]---[KORRIDOR 1]---[KORRIDOR 2]
               |                           |             
                                       [UTGÅNG] """,                           
                                        
            "gåta_rum": """             
            [Start]---[*GÅTA*]
               |          |
            [FÄLLA]---[KORRIDOR 1]---[KORRIDOR 2]---[UTGÅNG]
            """,
            "fälla_rum": """
            [Start]---[GÅTA]
               |         |
            [*FÄLLA*]---[KORRIDOR 1]---[KORRIDOR 2]---[UTGÅNG]
            """,
            "korridor_1": """
            [Start]---[GÅTA]
               |         |
            [FÄLLA]---[*KORRIDOR 1*]---[KORRIDOR 2]---[UTGÅNG]
            """,
            "korridor_2": """
            [Start]---[GÅTA]
               |         |
            [FÄLLA]---[KORRIDOR 1]---[*KORRIDOR 2*]---[UTGÅNG]
            """,
            "utgång": """
            [Start]---[GÅTA]
               |         |
            [FÄLLA]---[KORRIDOR 1]---[KORRIDOR 2]---[*UTGÅNG*]
            """
        }
        print("\nDin position:")
        print(karta.get(self.nuvarande_rum, karta["start"]))

    def initiera_rum(self):
        return {
            "start": {
                "namn": "Startrum",
                "beskrivning": """
                ╔════════════════════════════════════════╗
                ║ Du står i ett mörkt rum med tre dörrar ║
                ║ Din tid är begränsad!                  ║
                ╚════════════════════════════════════════╝
                """,
                "val": {
                    "rakt fram": ("fälla_rum", "Du går genom dörren rakt fram"),
                    "vänster": ("gåta_rum", "Du tar dörren till vänster")
                }
            },
            "korridor_1": {
                "namn": "Korridor 1",
                "beskrivning": """
                ╔════════════════════════════════════════════════════╗
                ║ En lång, smal korridor. Framför dig finns flera    ║
                ║ dörrar. En skugga blockerar din väg!               ║
                ╚════════════════════════════════════════════════════╝
                """,
                "val": {
                    "vänster": ("korridor_2", "Du fortsätter framåt"),
                },
                "utmaning": lambda: self.gåta_utmaning()
            },
            "korridor_2": {
                "namn": "Korridor 2",
                "beskrivning": """
                ╔════════════════════════════════════════════════════╗
                ║ En bred korridor med mörka väggar. En dörr         ║
                ║ skymtas framför dig, men en mekanism låser den!    ║
                ╚════════════════════════════════════════════════════╝
                """,
                "val": {
                    "rakt fram": ("utgång", "Du går mot utgången"),
                    "tillbaka": ("korridor_1", "Du går tillbaka")
                },
                "utmaning": lambda: self.kod_utmaning()
            },
            "gåta_rum": {
                "namn": "Gåtans rum",
                "beskrivning": """
                ╔════════════════════════════════════════════════════╗
                ║ Ett rum med en gammal staty som talar:             ║
                ║ 'Lös min gåta för att komma vidare.'               ║
                ╚════════════════════════════════════════════════════╝
                """,
                "val": {
                    "tillbaka": ("start", "Du går tillbaka"),
                    "höger": ("korridor_1", "Du fortsätter frammåt")
                },
                "utmaning": lambda: self.gåta_utmaning()
            },
            "fälla_rum": {
                "namn": "Fällans rum",
                "beskrivning": """
                ╔════════════════════════════════════════════════════╗
                ║ Golvet är fullt av fällor!                         ║
                ║ Du måste hitta en säker väg genom rummet.          ║
                ╚════════════════════════════════════════════════════╝
                """,
                "val": {
                    "tillbaka": ("start", "Du går tillbaka")
                },
                "utmaning": lambda: self.falla_utmaning()
            },
            "utgång": {
                "namn": "Utgång",
                "beskrivning": """
                ╔════════════════════════════════════════════════════╗
                ║ GRATTIS! Du har hittat utgången och vunnit spelet! ║
                ╚════════════════════════════════════════════════════╝
                """,
                "val": {}
            }
        }

    def spela(self):
        self.rensa_skarm()
        self.spelinstruktioner()  # Visa instruktionerna en gång i början
        input("\nTryck ENTER för att börja spelet...")

        while self.nuvarande_rum != "utgång" and self.kvarvarande_drag > 0:
            self.visa_rum()
        if self.nuvarande_rum in self.rum and "utmaning" in self.rum[self.nuvarande_rum]:
            self.kontrollera_utmaning()
        val = input("\nVilken väg väljer du? ").lower()
        self.flytta(val)

        self.visa_slutresultat()

    def visa_rum(self):
        self.rensa_skarm()
        rum = self.rum[self.nuvarande_rum]
        print(f"\n{rum['namn'].upper()}")
        print(rum['beskrivning'])
        self.visa_karta()
        print("\nTillgängliga vägar:")
        for riktning, (_, beskrivning) in rum["val"].items():
            print(f"► {riktning.capitalize()}: {beskrivning}")
        print(f"\nDrag kvar: {self.kvarvarande_drag}")

    def flytta(self, riktning):
        rum = self.rum[self.nuvarande_rum]
        if riktning in rum["val"]:
            nasta_rum, meddelande = rum["val"][riktning]
            print(f"\n{meddelande}")
            input("\nTryck ENTER för att fortsätta...")
            self.nuvarande_rum = nasta_rum
            self.kvarvarande_drag -= 1
            return True
        else:
            print("\n❌ Det går inte att gå åt det hållet!")
            input("\nTryck ENTER för att fortsätta...")
            return False



    def kontrollera_utmaning(self):
        rum = self.rum[self.nuvarande_rum]
        if "utmaning" in rum and self.nuvarande_rum not in self.uppklarade_utmaningar:
            print("\nDu stöter på en utmaning!")
            om_utmaning_klarad = rum["utmaning"]()
            if om_utmaning_klarad:
                print("\nUtmaningen är klarad! En ny väg öppnas.")
                self.uppklarade_utmaningar.add(self.nuvarande_rum)
                self.minst_en_utmaning_klarad = True
            else:
                print("\nDu misslyckades med utmaningen och förlorade ett drag.")
                self.kvarvarande_drag -= 1
                self.nuvarande_rum = "start"

    def gåta_utmaning(self):
        print("\nGåtan är: 'Vad har nycklar men inga lås, utrymmen men inga rum, och du kan bära det med dig?'")
        svar = input("Ditt svar: ").lower()
        return svar == "keyboard" or svar == "tangentbord"
    
    def korridor_1(self):
        print("\nGåtan är: 'Vad blir blötare ju mer du torkar med den?'")
        svar = input("Ditt svar: ").lower()
        return svar == "handduk"

    def falla_utmaning(self):
        print("\nDu måste navigera genom fällorna! Välj en siffra mellan 1 och 3.")
        val = input("Ditt val: ")
        korrekt_val = str(random.randint(1, 3))
        return val == korrekt_val

    def kod_utmaning(self):
        print("\nEtt matematiskt pussel visas framför dig:")
        tal1 = random.randint(1, 10)
        tal2 = random.randint(1, 10)
        operator = random.choice(["+", "-", "*"])

        if operator == "+":
            korrekt_svar = tal1 + tal2
        elif operator == "-":
            korrekt_svar = tal1 - tal2
        else:
            korrekt_svar = tal1 * tal2

        print(f"Vad är {tal1} {operator} {tal2}?")
        for _ in range(2):
            try:
                gissning = int(input("Ditt svar: "))
                if gissning == korrekt_svar:
                    print("\nRätt svar! En väg öppnas.")
                    return True
                else:
                    print("Fel svar! Försök igen.")
            except ValueError:
                print("Du måste skriva en siffra.")
        return False

    def spela(self):
        self.rensa_skarm()
        print("""
        ╔═══════════════════════════════════════╗
        ║      Välkommen till Labyrinten!       ║
        ║  Hitta utgången innan tiden tar slut  ║
        ╚═══════════════════════════════════════╝
        """)
        input("Tryck ENTER för att börja...")

        while self.nuvarande_rum != "utgång" and self.kvarvarande_drag > 0:
            self.visa_rum()
            if self.nuvarande_rum in self.rum and "utmaning" in self.rum[self.nuvarande_rum]:
                self.kontrollera_utmaning()
            val = input("\nVilken väg väljer du? ").lower()
            self.flytta(val)

        self.visa_slutresultat()

    def visa_slutresultat(self):
        self.rensa_skarm()
        if self.nuvarande_rum == "utgång":
            print("""
            ╔═══════════════════════════════╗
            ║    GRATTIS! Du klarade det!   ║
            ╚═══════════════════════════════╝
            """)
        else:
            print("""
            ╔═══════════════════════════════╗
            ║  Tiden tog slut! Game Over!   ║
            ╚═══════════════════════════════╝
            """)

# Starta spelet
if __name__ == "__main__":
    labyrint = Labyrint()
    labyrint.spela()