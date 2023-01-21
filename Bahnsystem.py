class Bahnsystem:

    def __init__(self, name: str, anzahl_bahnen: int, anzahl_pro_mannschaft: int, art: int, bahnen_verfügbar: int):
        self.name = name
        self.anzahl_bahnen = anzahl_bahnen
        self.anzahl_pro_mannschaft = anzahl_pro_mannschaft
        self.art = art
        self.bahnen_verfügbar = bahnen_verfügbar
        self.bahnen = list()
