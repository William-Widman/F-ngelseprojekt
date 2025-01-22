# Lägg in kommentarer i koden
# Utöka antalet rum om du siktar mot C eller A
# Flödeschema


import time
import random
import os


# Läser in och visar en "readme"-textfil för introduktion
with open('readme.txt', 'r', encoding="utf-8") as file:  
            data = file.read()  
            print(data)

input("Tryck på enter för att fortsätta") # Väntar på att spelaren ska läsa texten


# Klass för att hantera labyrintspelet
class Labyrint:
    def __init__(self):
        self.nuvarande_rum = "start"
        self.max_drag = 15
        self.kvarvarande_drag = self.max_drag
        self.uppklarade_utmaningar = set()
        self.minst_en_utmaning_klarad = False
        self.rum = self.initiera_rum()

    def rensa_skarm(self):
        #Rensar terminalfönstret för bättre läsbarhet
        os.system('cls' if os.name == 'nt' else 'clear') 

    def visa_karta(self):
        """Visar en enkel ASCII-karta över spelarens position"""
        karta = { # Kartor baserade på spelarens nuvarande rum
            "start": """
            [*START*]---[GÅTA]
               |           |
            [FÄLLA]---[KORRIDOR 1]---[KORRIDOR 2]---[rum]
                                          |           |
                                     [korridor 3]---[UTGÅNG] """,                           
                                        
            "gåta_rum": """             
            [START]---[*GÅTA*]
               |           |
            [FÄLLA]---[KORRIDOR 1]---[KORRIDOR 2]---[rum]
                                          |           |
                                     [korridor 3]---[UTGÅNG]
            """,
            "fälla_rum": """
            [START]---[GÅTA]
               |           |
            [*FÄLLA*]---[KORRIDOR 1]---[KORRIDOR 2]---[rum]
                                            |           |
                                       [korridor 3]---[UTGÅNG]
            """,
            "korridor_1": """
            [START]---[GÅTA]
               |           |
            [FÄLLA]---[*KORRIDOR 1*]---[KORRIDOR 2]---[rum]
                                           |             |
                                       [korridor 3]---[UTGÅNG]
            """,
            "korridor_2": """
            [START]---[GÅTA]
               |           |
            [FÄLLA]---[KORRIDOR 1]---[*KORRIDOR 2*]---[rum]
                                          |           |
                                    [korridor 3]---[UTGÅNG]
            """,
            "korridor_3": """
            [START]---[GÅTA]
               |           |
            [FÄLLA]---[KORRIDOR 1]---[KORRIDOR 2]---[rum]
                                          |           |
                                   [*korridor 3*]---[UTGÅNG]
            """,
            "rum": """
            [START]---[GÅTA]
               |           |
            [FÄLLA]---[KORRIDOR 1]---[KORRIDOR 2]---[*rum*]
                                          |           |
                                     [korridor 3]---[UTGÅNG]
            """,
            "utgång": """
            [START]---[GÅTA]
               |           |
            [FÄLLA]---[KORRIDOR 1]---[KORRIDOR 2]---[rum]
                                          |           |
                                     [korridor 3]---[*UTGÅNG*]
            """
        }
        print("\nDin position:")
        print(karta.get(self.nuvarande_rum, karta["start"]))

    def initiera_rum(self):
        return {
             # Varje rum har ett namn, en beskrivning, möjliga val och ibland en utmaning
            "start": {
                "namn": "Startrum",
                "beskrivning": """
                ╔════════════════════════════════════════╗
                ║ Du står i ett mörkt rum med tre dörrar ║
                ║ Din tid är begränsad!                  ║
                ╚════════════════════════════════════════╝
                """,
                "val": {
                    "rakt fram": ("fälla_rum", "Du går genom dörren rakt fram."),
                    "vänster": ("gåta_rum", "Du tar dörren till vänster.")
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
                    "vänster": ("korridor_2", "Du fortsätter framåt."),
                },
                "utmaning": lambda: self.korridor_1()
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
                    "rakt fram": ("rum", "Du fortsätter mot utgången."),
                    "tillbaka": ("korridor_1", "Du går tillbaka."),
                    "höger": ("korridor_3", "Du går höger.")
                },
                "utmaning": lambda: self.kod_utmaning()
            },

            "korridor_3": {
                "namn": "korridor_3",
                "beskrivning": """
                ╔════════════════════════════════════════════════════╗
                ║  Den sissta utmaningen innan du tar dig ut!        ║
                ║ Lös min sissta gåta.                               ║
                ╚════════════════════════════════════════════════════╝
                """,
                "val": {
                    "tillbaka": ("korridor_2", "Du går tillbaka."),
                    "vänster": ("utgång", "Du går mot utgången.")
                },
                "utmaning": lambda: self.tidsprovning()
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
                    "tillbaka": ("start", "Du går tillbaka."),
                    "höger": ("korridor_1", "Du fortsätter frammåt.")
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
                    "tillbaka": ("start", "Du går tillbaka."),
                    "vänster": ("korridor_1", "Du fortsätter frammåt.")
                },
                "utmaning": lambda: self.falla_utmaning()
            },
            "rum": {
                "namn": "rum",
                "beskrivning":"""
                ╔════════════════════════════════════════════════════╗
                ║ Du ser ljuset runt hörnet, inte långt kvar nu!     ║
                ╚════════════════════════════════════════════════════╝
                """,
                "val": {
                    "tillbaka": ("korridor_2", "Du går tillbaka."),
                    "höger": ("utgång", "Du går mot utgången.")
                },
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
        input("\nTryck ENTER för att börja spelet...")

        while self.nuvarande_rum != "utgång" and self.kvarvarande_drag > 0:
            self.visa_rum() # Visar aktuellt rum
        if self.nuvarande_rum in self.rum and "utmaning" in self.rum[self.nuvarande_rum]:
            self.kontrollera_utmaning() # Hanterar utmaningar om de finns
        val = input("\nVilken väg väljer du? ").lower()
        self.flytta(val)    # Flyttar spelaren till nästa rum baserat på valet

        self.visa_slutresultat()

    def visa_rum(self):
        self.rensa_skarm()
        rum = self.rum[self.nuvarande_rum]
        print(f"\n{rum['namn'].upper()}")
        print(rum['beskrivning'])
        self.visa_karta()   # Visar kartan
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
                
    # Exempel på utmaningar
    def gåta_utmaning(self):
        print("\nGåtan är: 'Vad har nycklar men inga lås, och du kan bära det med dig?'")
        svar = input("Ditt svar: ").lower()
        return svar == "keyboard" or svar == "tangentbord"
    
    def korridor_1(self):
        print("\nGåtan är: 'Vad blir blötare ju mer du torkar med den?'")
        svar = input("Ditt svar: ").lower()
        return svar == "handduk"

    def falla_utmaning(self):
        print("\nDu måste navigera genom fällorna! Välj en siffra mellan 1 och 2.")
        val = input("Ditt val: ")
        korrekt_val = str(random.randint(1, 2))
        return val == korrekt_val
    

    def tidsprovning(self):
        print("\nTiden är knapp! Du måste svara innan sanden rinner ut.")
        fråga = "Vad är två tredjedelar av 90?"
        korrekt_svar = 60
        total_tid = 15  # Total tid på 15 sekunder
        tid_reduktion = 5  # Tid som minskas för varje felaktigt svar
        start_tid = time.time()

        print(f"\nFråga: {fråga}")

        while total_tid > 0:
            kvarvarande_tid = total_tid - (time.time() - start_tid)
            if kvarvarande_tid <= 0:
                print("\nTiden är slut! Sanden har runnit ut.")
                return False  # Funktionen avslutas här

            print(f"Du har {kvarvarande_tid:.1f} sekunder kvar.")
            try:
                gissning = int(input("Ditt svar: "))
                if gissning == korrekt_svar:
                    print("\nRätt svar! Du hann i tid.")
                    return True  # Funktionen avslutas vid rätt svar
                else:
                    print("Fel svar! Tiden minskar.")
                    total_tid -= tid_reduktion  # Minskar den återstående tiden
                    start_tid = time.time()  # Återställer tidens referenspunkt
            except ValueError:
                print("Skriv en giltig siffra.")
    
        print("\nTiden är slut! Tiden har runnit ut.")
        return False

    

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