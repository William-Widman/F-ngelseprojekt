import random

class Labyrint:
    def __init__(self):
        self.nuvarande_rum = "start"
        self.max_drag = 20  # Antal drag innan spelet tar slut
        self.kvarvarande_drag = self.max_drag
        self.uppklarade_utmaningar = set()

        # Definiera rummen utan att referera till metoder ännu
        self.rum = {
            "start": {
                "beskrivning": "Du står i ett mörkt rum med tre dörrar. Din tid är begränsad!",
                "val": {
                    "rakt fram": "korridor_1",
                    "höger": "gåta_rum",
                    "vänster": "fälla_rum"
                }
            },
            "korridor_1": {
                "beskrivning": "En lång, smal korridor. Framför dig finns flera dörrar.",
                "val": {
                    "höger": "kod_rum",
                    "rakt fram": "korridor_2",
                    "tillbaka": "start"
                }
            },
            "korridor_2": {
                "beskrivning": "En bred korridor med mörka väggar. En dörr skymtas framför dig.",
                "val": {
                    "rakt fram": "utgång",
                    "tillbaka": "korridor_1"
                }
            },
            "gåta_rum": {
                "beskrivning": "Ett rum med en gammal staty som talar: 'Lös min gåta för att komma vidare.'",
                "val": {"tillbaka": "start"}
            },
            "fälla_rum": {
                "beskrivning": "Golvet är fullt av fällor! Du måste ta dig igenom utan att fastna.",
                "val": {"tillbaka": "start"}
            },
            "kod_rum": {
                "beskrivning": "Ett rum med ett låst kassaskåp. Du måste lösa koden.",
                "val": {"tillbaka": "korridor_1"}
            },
            "utgång": {
                "beskrivning": "GRATTIS! Du har hittat utgången och vunnit spelet!",
                "val": {}
            }
        }

        # Tilldela utmaningsfunktionerna efteråt
        self.rum["gåta_rum"]["utmaning"] = self.gata_utmaning
        self.rum["fälla_rum"]["utmaning"] = self.falla_utmaning
        self.rum["kod_rum"]["utmaning"] = self.kod_utmaning

        self.uppklarade_utmaningar = set()

    def visa_rum(self):
        rum = self.rum[self.nuvarande_rum]
        print(f"\n{rum['beskrivning']}")
        print("\nDu kan gå:")
        for riktning in rum["val"]:
            print(f"- {riktning}")

    def flytta(self, riktning):
        if riktning in self.rum[self.nuvarande_rum]["val"]:
            self.nuvarande_rum = self.rum[self.nuvarande_rum]["val"][riktning]
            self.kvarvarande_drag -= 1
        else:
            print("\nDet går inte att gå åt det hållet!")

    def kontrollera_utmaning(self):
        rum = self.rum[self.nuvarande_rum]
        if "utmaning" in rum and self.nuvarande_rum not in self.uppklarade_utmaningar:
            print("\nDu stöter på en utmaning!")
            om_utmaning_klarad = rum["utmaning"]()
            if om_utmaning_klarad:
                print("\nUtmaningen är klarad! En ny väg öppnas.")
                self.uppklarade_utmaningar.add(self.nuvarande_rum)
                if self.nuvarande_rum == "gåta_rum":
                    self.rum["gåta_rum"]["val"]["rakt fram"] = "korridor_1"
                elif self.nuvarande_rum == "fälla_rum":
                    self.rum["fälla_rum"]["val"]["rakt fram"] = "korridor_1"
                elif self.nuvarande_rum == "kod_rum":
                    self.rum["kod_rum"]["val"]["rakt fram"] = "korridor_2"
            else:
                print("\nDu misslyckades med utmaningen och förlorade ett drag.")
                self.kvarvarande_drag -= 1
                self.nuvarande_rum = "start"

    def gata_utmaning(self):
        print("\nGåtan är: 'Vad har nycklar men inga lås, utrymmen men inga rum, och du kan bära det med dig?'")
        svar = input("Ditt svar: ").lower()
        return svar == "keyboard" or svar == "tangentbord"

    def falla_utmaning(self):
        print("\nDu måste navigera genom fällorna! Välj en siffra mellan 1 och 3.")
        val = input("Ditt val: ")
        korrekt_val = str(random.randint(1, 3))
        return val == korrekt_val

def kod_utmaning(self):
    print("\nEn gammal stenpelare står i rummet. På den finns ett pussel ingraverat:")

    # Skapa ett slumpmässigt matematiskt pussel
    tal1 = random.randint(1, 10)
    tal2 = random.randint(1, 10)
    operator = random.choice(["+", "-", "*"])

    # Beräkna det korrekta svaret
    if operator == "+":
        korrekt_svar = tal1 + tal2
    elif operator == "-":
        korrekt_svar = tal1 - tal2
    else:  # Multiplikation
        korrekt_svar = tal1 * tal2

    print(f"Vad är {tal1} {operator} {tal2}?")

    # Ge spelaren 2 försök att svara
    for _ in range(2):
        try:
            gissning = int(input("Ditt svar: "))
            if gissning == korrekt_svar:
                print("\nStenpelaren skakar och en hemlig dörr öppnas!")
                return True
            else:
                print("Fel svar! Försök igen.")
        except ValueError:
            print("Du måste skriva en siffra.")

        print(f"\nDu misslyckades med pusslet. Det korrekta svaret var {korrekt_svar}.")
        return False



    def spela(self):
        print("Välkommen till labyrinten! Hitta ut innan dina drag tar slut.")
        while self.nuvarande_rum != "utgång" and self.kvarvarande_drag > 0:
            print(f"\nDrag kvar: {self.kvarvarande_drag}")
            self.visa_rum()
            self.kontrollera_utmaning()
            val = input("\nVilken riktning vill du gå? ").lower()
            self.flytta(val)
        
        if self.nuvarande_rum == "utgång":
            print("\nDu klarade labyrinten! Grattis!")
        else:
            print("\nTiden tog slut! Du fastnade i labyrinten...")


# Starta spelet
labyrint = Labyrint()
labyrint.spela()
