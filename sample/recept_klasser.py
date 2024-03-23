import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import sample.enheter as enh
import json
from dataclasses import dataclass

brak_unicode_tecken = {".33":"⅓", ".67":"⅔", ".2":"⅕", ".4":"⅖", ".6":"⅗", ".8":"⅘", ".5":"½", ".25":"¼", ".75":"¾"}

def tolka_braktecken(str_):
    inv_braktecken = {v: k for k, v in brak_unicode_tecken.items()}
    return inv_braktecken.get(str_, None)

def byt_braktecken(str_):
    for key, value in brak_unicode_tecken.items():
        str_ = str_.replace(key, " " + value)
    if str_[0] == "0":
        str_ = str_[2:]
    return str_


class Produkt:
    namn: str
    _matvarden: list[enh.Tal]

    def __init__(self, namn, matvarden, temp = False):
        self.namn = namn
        self._matvarden = matvarden
        self._temp = temp # Temporär produkt som inte finns i sparad dict

    @classmethod
    def ur_dict(cls, dict):
        namn = dict.get("namn", "")
        matvarden = []
        for matvarde in dict.get("mätvärden", []):
            matvarden.append(enh.Tal.tolka(matvarde))
        return(Produkt(namn, matvarden))

    @classmethod
    def tolka(cls, str_):
        ing_dict = json.loads(str_)
        return Produkt.ur_dict(ing_dict)

    def matvarden(self):
        return self._matvarden

    def pris(self, tal):
        pris_per_enhet = self.berakna_varde_i(enh.kr, tal.enhet)
        return tal * pris_per_enhet

    def berakna_varde_i(self, beroende, oberoende):
        if self.matvarden():
            enhet_ut = beroende / oberoende
            for matvarde in self.matvarden():

                if matvarde.har_samma_dimension(enhet_ut):
                    return matvarde
                elif (1 / enh.Tal(1, matvarde.enhet)).har_samma_dimension(enhet_ut):
                    return 1 / matvarde
            alternativ_matvarde = self.finn_alternativ(beroende)
            alternativ = (alternativ_matvarde * beroende)
            andra_matvarde = self.berakna_varde_i(alternativ, oberoende)
            resultat = andra_matvarde / alternativ_matvarde
            return resultat
        return 0

    def finn_alternativ(self, beroende):
        for matvarde in self.matvarden():
            for del_ in matvarde.enhet.delar():
                if del_.har_samma_dimension(beroende):
                    return (1 / (matvarde))
                elif del_.har_samma_dimension(1 / beroende):
                    return matvarde
        raise(ValueError(f"Kunde inte hitta mätvärde med variabel {beroende} i {self.matvarden()}"))

    def kilopris(self):
        return self.berakna_varde_i(enh.kr, enh.kg)

    def till_dict(self):
        dict = {"namn":self.namn, "mätvärden":[str(matv) for matv in self.matvarden()]}
        return dict

    def __repr__(self):
        return self.namn


@dataclass
class Produktkatalog:
    produkter: list[Produkt]

    @classmethod
    def tolka(cls, str_):
        str_dict = json.loads(str_)
        produkter = [Produkt.ur_dict(dict) for dict in str_dict.get("produkter", [])]
        return Produktkatalog(produkter)

    def hitta_med_namn(self, namn):
        for produkt in self.produkter:
            if produkt.namn == namn:
                return produkt

    def add(self, produkt):
        self.produkter.append(produkt)

    def till_dict(self):
        dict = {"produkter":[produkt.till_dict() for produkt in self.produkter if not produkt._temp]}
        return dict

    def __add__(self, other):
        if type(other) is Produktkatalog:
            return Produktkatalog(self.produkter + other.produkter)
        return NotImplemented

@dataclass
class Ingrediens:
    produkt: Produkt
    mangd: enh.Tal

    @classmethod
    def tolka(cls, str_, produktkatalog):
        str_delar = str_.split()
        testa_brak = tolka_braktecken(str_delar[1])
        if not testa_brak is None:
            tal_del = str_delar[0] + testa_brak + str_delar[2]
            produkt_del = " ".join(str_delar[3:])
        else:
            tal_del = " ".join(str_delar[:2])
            produkt_del = " ".join(str_delar[2:])
        mangd = enh.Tal.tolka(tal_del)
        if mangd is None:
            return str_
        produkt = produktkatalog.hitta_med_namn(produkt_del)
        if produkt is None:
            produkt = Produkt(produkt_del, [enh.Tal.tolka("0 kr/kg"), enh.Tal.tolka("0 kr/st"), enh.Tal.tolka("0 kr/dl")], True)
            produktkatalog.add(produkt)
        return Ingrediens(produkt, mangd)

    def kostnad(self):
        return self.produkt.pris(self.mangd)

    def __repr__(self):
        return byt_braktecken(f"{self.mangd} {self.produkt}")

@dataclass
class Recept:
    ingredienser: list[Ingrediens]
    produktkatalog: Produktkatalog
    portioner: int = 4
    instruktioner_steg: str = ""
    beskrivning: str = ""
    rubrik: str = ""
    ugnstemperatur: enh.Tal = None

    @classmethod
    def tolka(cls, str_, produktkatalog):
        str_dict = json.loads(str_)
        ingredienser = [Ingrediens.tolka(ing, produktkatalog) for ing in str_dict.get("ingredienser", [])]
        portioner = int(str_dict.get("portioner", 4))
        instruktioner_steg = str_dict.get("instruktioner", "")
        beskrivning = str_dict.get("beskrivning", "")
        rubrik = str_dict.get("rubrik", "")
        ugnstemperatur = str_dict.get("ugnstemperatur", None)
        return Recept(ingredienser, produktkatalog, portioner, instruktioner_steg, beskrivning, rubrik, ugnstemperatur)

    def portionskostnad(self):
        return self.totalkostnad() / self.portioner

    def totalkostnad(self, prata = False):
        totalkostnad = enh.Tal(0, enh.kr)
        for ingrediens in self.ingredienser:
            if type(ingrediens) is str:
                continue
            ingredienskostnad = ingrediens.kostnad()
            totalkostnad += ingredienskostnad
            if prata:
                print(f"{ingrediens}: {ingredienskostnad}")
        return totalkostnad

    def till_dict(self):
        return {
            "rubrik":self.rubrik,
            "beskrivning":self.beskrivning,
            "portioner":self.portioner,
            "ingredienser":[str(ing) for ing in self.ingredienser],
            "instruktioner":self.instruktioner_steg,
            "ugnstemperatur":self.ugnstemperatur
            }

    def __repr__(self):
        extra_info = ", ".join(i for i in [str(self.ugnstemperatur), f"{self.portioner} portioner"] if not i in ("", "None"))
        return f"{self.rubrik}\n\n{extra_info}\n\n{self.beskrivning}\n\nIngredienser:\n{"\n".join([f"  {ing}" for ing in self.ingredienser])}\n\n{self.instruktioner_steg}"


if __name__=="__main__":
    pass
