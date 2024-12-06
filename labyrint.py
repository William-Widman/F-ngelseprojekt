

print("Du vaknar till medvetande med en molande huvudvärk.\nDina ögon försöker fokusera i ett svagt upplyst rum.\nGolvetkänns hårt och kallt under dig, och när du sakta\nreser dig märker du att du inte minns hur du hamnade här.")
print("Väggarna runt omkring dig är gråvita och nästan omärkligt böjda.\nIngen fönster. Ingen tydlig dörr. Bara tre mörka öppningar\nsom leder åt olika håll. Din kropp känns stum,\noch minnet är borta - det enda du vet är att du måste hitta\nett sätt ut härifrån.\n\n")




class Labyrint:
    def __init__(self):
        self.nuvarande_rum = "start"
        self.rum = {
            "start": {
                "beskrivning": "Du befinner dig i en ljus startrum med vita väggar.\nTre dörrar finns framför dig.",
                "val": {
                    "höger": "korridor_1",
                    "vänster": "sidorum",
                    "rakt fram": "huvudkorridor"
                }
            },
            "sidorum": {
                "beskrivning": "Ett litet sidorum med dämpat ljus. Här finns bara en väg tillbaka.",
                "val": {
                    "tillbaka": "start"
                }
            },
            "huvudkorridor": {
                "beskrivning": "En lång korridor med mystiska skuggor på väggarna. Du ser flera valmöjligheter.",
                "val": {
                    "höger": "mörkt_rum",
                    "vänster": "ljust_rum", 
                    "rakt fram": "korridor_2"
                }
            },
            "korridor_1": {
                "beskrivning": "En smal korridor med träpanel. Du ser en dörr framför dig.",
                "val": {
                    "vänster": "start",
                    "rakt fram": "litet_rum"
                }
            },
            "korridor_2": {
                "beskrivning": "En bred korridor med högt i tak. Flera passager syns.",
                "val": {
                    "höger": "hemlig_gång",
                    "vänster": "huvudkorridor",
                    "rakt fram": "utgång"
                }
            },
            "mörkt_rum": {
                "beskrivning": "Ett mörkt rum där du knappt ser någonting. Försiktigt måste du välja nästa steg.",
                "val": {
                    "vänster": "huvudkorridor"
                }
            },
            "ljust_rum": {
                "beskrivning": "Ett upplyst rum med ett fönster. Här finns bara en väg tillbaka.",
                "val": {
                    "tillbaka": "huvudkorridor"
                }
            },
            "litet_rum": {
                "beskrivning": "Ett litet kvadratiskt rum med en karta på väggen. Du ser flera utgångar.",
                "val": {
                    "höger": "hemlig_gång",
                    "vänster": "korridor_1"
                }
            },
            "hemlig_gång": {
                "beskrivning": "En smal, mystisk gång som verkar leda någonstans spännande.",
                "val": {
                    "vänster": "litet_rum",
                    "rakt fram": "utgång"
                }
            },
            "utgång": {
                "beskrivning": "GRATTIS! Du har hittat utgången och klarar labyrinten!",
                "val": {}
            }
        }

    def visa_rum(self):
        rum = self.rum[self.nuvarande_rum]
        print(rum["beskrivning"])
        print("\nDu kan gå:")
        for riktning in rum["val"]:
            print(f"- {riktning}")

    def flytta(self, riktning):
        if riktning in self.rum[self.nuvarande_rum]["val"]:
            self.nuvarande_rum = self.rum[self.nuvarande_rum]["val"][riktning]
            return True
        else:
            print("Det går inte att gå åt det hållet!")
            return False

def spela_labyrint():
    labyrint = Labyrint()
    print("Välkommen till labyrinten! Försök hitta utgången.")
    
    while labyrint.nuvarande_rum != "utgång":
        labyrint.visa_rum()
        val = input("\nVilken riktning vill du gå? ").lower()
        labyrint.flytta(val)
    
    print("\nDu klarade labyrinten! Grattis!")

spela_labyrint()