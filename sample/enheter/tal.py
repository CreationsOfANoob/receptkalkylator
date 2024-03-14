from dataclasses import dataclass
from typing import Union
from .main import Grundenhet, Enhet
from .enheter import enheter as bef_enheter


@dataclass
class Tal:
    kvantitet: float
    enhet: Grundenhet | Enhet

    def __post_init__(self):
        if self.enhet is None:
            self.enhet = Enhet.enhetslos()
        for enh in bef_enheter:
            if self.enhet.har_samma_dimension(enh):
                self.kvantitet *= self.enhet.faktor() / enh.faktor()
                self.enhet = enh
                break

    @classmethod
    def tolka(cls, str_):
        delar = str_.split()
        kvant = float(delar[0])
        enh = hitta_enhet_str(delar[1])
        return Tal(kvant, enh[0])

    def __add__(self, other):
        if type(other) is Tal:
            if self.enhet.har_samma_dimension(other.enhet):
                return Tal(self.kvantitet + other.kvantitet, self.enhet)
            raise ValueError(f"Kan inte addera tal med olika dimension ({self.enhet} inte samma som {other.enhet})")
        return NotImplemented

    def __mul__(self, other):
        if type(other) is int or type(other) is float:
            kvantitet = self.kvantitet * other * self.enhet.faktor()
            return Tal(kvantitet, self.enhet)
        elif type(other) is Tal:
            return Tal(self.kvantitet * other.kvantitet, self.enhet * other.enhet)
        return NotImplemented

    __rmul__ = __mul__

    def __sub__(self, other):
        return self + (other * -1)

    def __pow__(self, other):
        if type(other) is int or type(other) is float:
            return Tal(pow(self.kvantitet, other), pow(self.enhet, other))
        return NotImplemented

    def __truediv__(self, other):
        return self * pow(other, -1)

    __rtruediv__ = __truediv__

    def __eq__(self, other):
        if type(other) is Tal:
            return self.kvantitet == other.kvantitet and self.enhet == other.enhet
        return NotImplemented

    def __repr__(self):
        if self.enhet.kort() == "":
            return f"{self.kvantitet:g}"
        return f"{self.kvantitet:g} {self.enhet.kort()}"


def hitta_enhet_str(str_):
    for enh in bef_enheter:
        if enh.kort() == str_:
            return (enh, enh.faktor())
    return None
