# Tre variabler
variabel_1 = "Hej här är jag den första variabeln!"
variabel_2 = 42  # Ett heltal
variabel_3 = True  # Ett booleskt värde

print("Programmet startar...")

print("\n------------------------------------------------------------------\n")

print(f"variabel_1 är nu: \n{variabel_1}\n\nvariabel_2 är nu: \n{variabel_2}\n\nvariabel_3 är nu: \n{variabel_3}\n")

# Öppna filen i skrivläge (eller skapa filen om den inte finns)
# with open säkerställer att filen automatiskt stängs när den inte längre behövs, 
# vilket minimerar risken för buggar eller låsta resurser.
with open("sparade_variabler.txt", "w") as fil:
    # Skriv variabelnamn och värden i filen, varje variabel på en egen rad
    fil.write("variabel_1: " + variabel_1 + "\n")
    fil.write("variabel_2: " + str(variabel_2) + "\n")  # Konvertera heltalet till en sträng
    fil.write("variabel_3: " + str(variabel_3) + "\n")  # Konvertera bool till en sträng

print("De tre variablerna har sparats i filen 'sparade_variabler.txt'.")

print("\n------------------------------------------------------------------\n")

print("Nu ändrar jag på variablerna.\n")

variabel_1 = "Hej här är jag den första variabeln som fått ett nytt värde!"
variabel_2 = 99  # Nytt heltal
variabel_3 = False  # Nytt booleskt värde

print(f"variabel_1 är nu: \n{variabel_1}\n\nvariabel_2 är nu: \n{variabel_2}\n\nvariabel_3 är nu: \n{variabel_3}\n")

print("\n------------------------------------------------------------------\n")

print("Nu ska jag ersätta variablernas värde med de som är sparade i textfilen...\n")

# Läs in sparade variabler från filen
# readlines() läser hela filens innehåll och lagrar varje rad som en sträng i en lista.
# För större filer kan readline() användas för att läsa en rad i taget.
with open("sparade_variabler.txt", "r") as fil:
    innehåll = fil.readlines()

# Extrahera och dela upp varje rad baserat på kolon
# .strip() tar bort onödiga blanksteg och radbrytningar från texten.
# .split(": ") delar strängen vid första förekomsten av ": ", vilket ger 
# en lista där första elementet är variabelnamnet och andra är värdet.
for rad in innehåll:
    if "variabel_1" in rad:
        # Hämtar värdet för variabel_1 som en sträng
        variabel_1 = rad.strip().split(": ")[1]  
    elif "variabel_2" in rad:
        # Hämtar värdet för variabel_2 som ett heltal
        variabel_2 = int(rad.strip().split(": ")[1])
    elif "variabel_3" in rad:   
        # Hämtar värdet för variabel_3 och konverterar det tillbaka till en bool
        variabel_3 = rad.strip().split(": ")[1] == "True"

print(f"variabel_1 är nu: \n{variabel_1} \n\nvariabel_2 är nu: \n{variabel_2}\n\nvariabel_3 är nu: \n{variabel_3}\n")

print("\n------------------------------------------------------------------\n")

print("Avslutar programmet...")