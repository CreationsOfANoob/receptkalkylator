import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import sample.enheter as enh
import json
from dataclasses import dataclass



class Produkt:
    namn: str
    _matvarden: list[enh.Tal]

    def __init__(self, namn, matvarden):
        self.namn = namn
        self._matvarden = matvarden

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
#        print(f"{self.namn}: {pris_per_enhet}, mängd: {tal}, => pris: {tal * pris_per_enhet} (enhet: {tal.enhet} med faktor: {tal.enhet.faktor()})")
        return tal * pris_per_enhet

    def berakna_varde_i(self, beroende, oberoende, depth = 0):
        enhet_ut = beroende / oberoende
        for matvarde in self.matvarden():
            if matvarde.har_samma_dimension(enhet_ut):
                return matvarde / matvarde.faktor()
            elif (1 / matvarde).har_samma_dimension(enhet_ut):
                return (1 / matvarde) * (enhet_ut.faktor())
            else:
                for del_ in matvarde.enhet.delar():
                    if del_ == beroende:
                        alternativ = 1 / (matvarde / beroende)
                        resultat = matvarde * self.berakna_varde_i(alternativ, oberoende, depth + 1)
                        return resultat
                    elif del_ == 1 / beroende:
                        alternativ = matvarde / beroende
                        resultat = matvarde * self.berakna_varde_i(alternativ, oberoende, depth + 1)
                        return resultat

    def kilopris(self):
        return self.berakna_varde_i(enh.kr, enh.kg)

    def till_dict(self):
        dict = {"namn":self.namn, "mätvärden":self.matvarden()}
        return dict


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


@dataclass
class Ingrediens:
    produkt: Produkt
    mangd: enh.Tal

    @classmethod
    def tolka(cls, str_, produktkatalog):
        str_delar = str_.split()
        tal_del = " ".join(str_delar[:2])
        produkt_del = " ".join(str_delar[2:])
        mangd = enh.Tal.tolka(tal_del)
        produkt = produktkatalog.hitta_med_namn(produkt_del)
        return Ingrediens(produkt, mangd)

    def kostnad(self):
        return self.produkt.pris(self.mangd)

@dataclass
class Recept:
    ingredienser: list[Ingrediens]
    produktkatalog: Produktkatalog
    portioner: int = 4
    instruktioner_steg: str = ""
    beskrivning: str = ""

    @classmethod
    def tolka(cls, str_, produktkatalog):
        str_dict = json.loads(str_)
        ingredienser = [Ingrediens.tolka(ing, produktkatalog) for ing in str_dict.get("ingredienser", [])]
        portioner = str_dict.get("portioner", 4)
        instruktioner_steg = str_dict.get("instruktioner", "")
        beskrivning = str_dict.get("beskrivning", "")
        return Recept(ingredienser, produktkatalog, portioner, instruktioner_steg, beskrivning)

    def portionskostnad(self):
        return self.totalkostnad() / self.portioner

    def totalkostnad(self):
        totalkostnad = enh.Tal(0, enh.kr)
        for ingrediens in self.ingredienser:
            ingredienskostnad = ingrediens.kostnad()
            totalkostnad += ingredienskostnad
        return totalkostnad


if __name__=="__main__":
    for enhet in enh.enheter:
        print(enhet)
    print()
    print(enh.Tal.tolka("36 km/h") + enh.Tal.tolka("25 m/s"))
