"""
# Labyrintspelet

## Beskrivning
Det här är ett textbaserat äventyrsspel där du måste navigera genom en labyrint, lösa utmaningar och hitta utgången innan dina drag tar slut. Spelet är interaktivt och innehåller olika typer av utmaningar som gåtor, fällor och matematiska pussel.

---

## Spelregler
1. **Mål:** Hitta utgången genom att navigera mellan rum i labyrinten.
2. **Drag:** Du har **15 drag** på dig att klara spelet.
3. **Utmaningar:** Många rum och korridorer är blockerade av utmaningar som måste klaras för att gå vidare.
4. **Om du misslyckas:** Du förlorar ett drag och skickas tillbaka till start.

---

## Rum och utmaningar

- **Start**: Utgångspunkten i labyrinten.
- **Korridor 1**: Blockeras av en gåta.
- **Korridor 2**: Blockeras av ett matematiskt pussel.
- **Korridor 3**: Blockeras av ett matematiskt pussel.
- **Gåta Rum**: En staty som ställer en gåta.
- **Fälla Rum**: En farlig plats där du väljer ett nummer för att överleva.
- **Rum sissta**: rummet innan utgången.
- **Utgång**: Här avslutas spelet om du har lyckats hitta rätt väg.

---

## Spelmekanik

1. **Navigera**: Spelaren väljer en riktning att gå genom att skriva kommandon som `rakt fram`, `höger`, `vänster` eller 
`tillbaka`
2. **Utmaningar**:
   - **Gåta**: Lös en gåta genom att gissa rätt svar.
   - **Fällor**: Välj en siffra mellan 1 och 3 för att undvika fällan.
   - **Kodpussel**: Lös en enkel matematikuppgift.
3. **Drag**: Varje rörelse och misslyckad utmaning minskar antalet drag.
