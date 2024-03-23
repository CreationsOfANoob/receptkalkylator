from dataclasses import dataclass
from typing import Union
from math import isclose
from .main import Grundenhet, Enhet, Delenhet
from .enheter import enheter as bef_enheter


class Tal:
    kvantitet: float
    enhet: Grundenhet | Enhet

    def __init__(self, kvantitet, enhet, normalisera = True):
        self.kvantitet = kvantitet
        self.enhet = enhet
        if type(self.enhet) is str:
            self.tolka_str_enhet(self.enhet)
        if self.enhet is None:
            self.enhet = Enhet.enhetslos()
        if normalisera:
            self.kvantitet *= self.enhet.faktor()
        if not self.enhet in bef_enheter:
            for enh in bef_enheter:
                if self.enhet.har_samma_dimension(enh):
                    self.enhet = enh
                    break

    @classmethod
    def tolka(cls, str_):
        str_ = str_.replace(",", ".")
        delar = str_.split()
        try:
            kvant = float(delar[0])
        except ValueError:
            return None
        enh = " ".join(delar[1:])
        return Tal(kvant, enh)

    def tolka_str_enhet(self, str_enhet):
        enh = hitta_enhet_str(str_enhet)
        if enh is None:
            raise(ValueError(f"Kunde inte tolka {str_enhet} som en enhet"))
        self.enhet = enh

    def copy(self):
        return Tal(self.kvantitet, self.enhet)

    def har_samma_dimension(self, other):
        if type(other) is Tal:
            return self.enhet.har_samma_dimension(other.enhet)
        return self.enhet.har_samma_dimension(other)

    def faktor(self):
        return self.enhet.faktor()

    def __add__(self, other):
        if type(other) is Tal:
            if self.enhet.har_samma_dimension(other.enhet):
                return Tal(self.kvantitet + other.kvantitet, self.enhet)
            raise ValueError(f"Kan inte addera tal med olika dimension ({self.enhet} inte samma som {other.enhet})")
        return NotImplemented

    def __mul__(self, other):
        if type(other) is int or type(other) is float:
            kvantitet_ = self.kvantitet * other
            return Tal(kvantitet_, self.enhet, False)
        elif type(other) is Tal:
            ny_enhet = self.enhet * other.enhet
            return Tal((self.kvantitet * other.kvantitet), ny_enhet, False)
        elif type(other) is Enhet or type(other) is Grundenhet:
            return self * Tal(1, other, False)
        elif type(other) is Delenhet:
            return self * Tal(1, Enhet([other]), False)
        return NotImplemented

    __rmul__ = __mul__

    def __sub__(self, other):
        return self + (other * -1)

    def __pow__(self, other):
        if type(other) is int or type(other) is float:
            ny_enhet = pow(self.enhet, other)
            return Tal(pow(self.kvantitet, other), ny_enhet, False)
        return NotImplemented

    def __truediv__(self, other):
        return self * pow(other, -1)

    def __rtruediv__(self, other):
        return other * pow(self, -1)

    def __round__(self, precision):
        return Tal(round(self.kvantitet, precision), self.enhet, False)

    def __eq__(self, other):
        if type(other) is Tal:
            return isclose(self.kvantitet, other.kvantitet) and self.enhet.har_samma_dimension(other.enhet)
        if type(other) is int or type(other) is float:
            return self.kvantitet == other and self.enhet.ar_enhetslos()
        if type(other) is Enhet or type(other) is Grundenhet:
            return self.kvantitet == 1 and self.enhet == other
        return NotImplemented

    def __repr__(self):
        if self.enhet.kort() == "":
            return f"{self.kvantitet:g}"
        return f"{(self.kvantitet / self.enhet.faktor()):g} {self.enhet.kort()}"


def hitta_enhet_str(str_):
    # försök först att hitta en definierad enhet
    enh = hitta_enkel_enhet(str_)
    if not enh is None:
        return enh

    # försök sedan att hitta sammansatt enhet
    if "/" in str_ or "*" in str_:
        enh = None
        str_enh = ""
        last_operator = "*"
        i = 0
        for char in str_:
            i += 1
            if char in "/*" or i == len(str_):
                if i == len(str_):
                    str_enh += char
                tolkad_enhet = hitta_enkel_enhet(str_enh.strip())
                if tolkad_enhet is None:
                    raise(ValueError(f"Kunde inte tolka enheten {str_enh}"))
                if last_operator == "*":
                    enh *= tolkad_enhet
                else:
                    enh /= tolkad_enhet
                last_operator = char
                str_enh = ""
            else:
                str_enh += char
        return enh

def hitta_enkel_enhet(str_):
    enh_kort = str_
    exponent = 1
    if "^" in str_:
        delar = str_.split("^")
        enh_kort = delar[0]
        exponent = int(delar[1].split(" ")[0].split("*")[0].split("/")[0])
    for enh in bef_enheter:
        if enh.kort() == enh_kort:
            if type(enh) is Grundenhet:
                return Enhet([Delenhet(enh, exponent)])
            elif type(enh) is Enhet:
                return enh
