from dataclasses import dataclass
from typing import Union
from .main import Grundenhet, Enhet, Delenhet
from .enheter import enheter as bef_enheter


@dataclass
class Tal:
    kvantitet: float
    enhet: Grundenhet | Enhet

    def __post_init__(self):
        if type(self.enhet) is str:
            self.enhet = hitta_enhet_str(self.enhet)
        if self.enhet is None:
            self.enhet = Enhet.enhetslos()
        self.kvantitet *= self.enhet.faktor() # Ta ut enhetens faktor
        if not self.enhet in bef_enheter:
            for enh in bef_enheter:
                if self.enhet.har_samma_dimension(enh):
                    a = self.kvantitet
                    self.enhet = enh
                    break

    @classmethod
    def tolka(cls, str_):
        delar = str_.split()
        kvant = float(delar[0])
        enh = hitta_enhet_str(delar[1])
        if enh is None:
            raise(ValueError(f"Kunde inte tolka {delar[1]} som en enhet (i {str_})"))
        return Tal(kvant, enh)


    def __add__(self, other):
        if type(other) is Tal:
            if self.enhet.har_samma_dimension(other.enhet):
                return Tal(self.kvantitet + other.kvantitet, self.enhet)
            raise ValueError(f"Kan inte addera tal med olika dimension ({self.enhet} inte samma som {other.enhet})")
        return NotImplemented

    def __mul__(self, other):
        if type(other) is int or type(other) is float:
            kvantitet = self.kvantitet * other
            return Tal(kvantitet, self.enhet)
        elif type(other) is Tal:
            ny_enhet = self.enhet * other.enhet
            return Tal((self.kvantitet * other.kvantitet) / ny_enhet.faktor(), ny_enhet)
        return NotImplemented

    __rmul__ = __mul__

    def __sub__(self, other):
        return self + (other * -1)

    def __pow__(self, other):
        if type(other) is int or type(other) is float:
            ny_enhet = pow(self.enhet, other)
            return Tal(pow(self.kvantitet, other) / ny_enhet.faktor(), ny_enhet)
        return NotImplemented

    def __truediv__(self, other):
        return self * pow(other, -1)

    def __rtruediv__(self, other):
        return other * pow(self, -1)

    def __eq__(self, other):
        if type(other) is Tal:
            return self.kvantitet == other.kvantitet and self.enhet.har_samma_dimension(other.enhet)
        if type(other) is int or type(other) is float:
            return self.kvantitet == other and self.enhet.ar_enhetslos()
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
        for l in str_:
            i += 1
            if l in "/*" or i == len(str_):
                if i == len(str_):
                    str_enh += l
                tolkad_enhet = hitta_enkel_enhet(str_enh)
                if last_operator == "*":
                    enh *= tolkad_enhet
                else:
                    enh /= tolkad_enhet
                last_operator = l
                str_enh = ""
            else:
                str_enh += l
        return enh


def hitta_enkel_enhet(str_):
    enh_kort = str_
    exponent = 1
    if "^" in str_:
        delar = str_.split("^")
        enh_kort = delar[0]
        exponent = int(delar[1])
    for enh in bef_enheter:
        if enh.kort() == enh_kort:
            if type(enh) is Grundenhet:
                return Enhet([Delenhet(enh, exponent)])
            elif type(enh) is Enhet:
                return enh
    return None
