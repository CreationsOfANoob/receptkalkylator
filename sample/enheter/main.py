from enum import Enum
from dataclasses import dataclass

@dataclass
class Grundenhet:
    namn: str # t.ex. meter
    kort: str # förkortning, t.ex. m
    dimension: str # t.ex. längd

    def __mul__(self, other):
        return Enhet([Delenhet(self, 1)]) * other

    __rmul__ = __mul__

    def __truediv__(self, other):
        return self * (1 / other)

    def __rtruediv__(self, other):
        return self**-1 * other

    def __pow__(self, other):
        if type(other) is int:
            return Enhet([Delenhet(self, other)])

    def __eq__(self, other):
        return self.kort == other.kort and self.dimension == other.dimension

    def __repr__(self):
        return f"{self.namn} ({self.kort}), {self.dimension}"

@dataclass
class Delenhet:
    enhet: Grundenhet
    potens: int

    def har_samma_enhet(self, other):
        return self.enhet == other.enhet

    def __imul__(self, other):
        self.potens += other.potens

    def __pow__(self, other):
        return Delenhet(self.enhet, self.potens * other)

    def __repr__(self):
        if self.potens == 1:
            return f"{self.enhet.kort}"
        return f"{self.enhet.kort}^{self.potens}"

@dataclass
class Enhet:
    delar: list[Delenhet]
    _namn: str = "" # t.ex. hektar
    kort: str = "" # t.ex. ha
    dimension: str = "" # t.ex. area
    faktor: float = 1 # t.ex. 10000.0

    def __post_init__(self):
        # slå ihop dubbla enhetsdefinitioner
        rensade_delar = []
        for del_ in self.delar:
            if not any(del_.har_samma_enhet(del_tillagd) for del_tillagd in rensade_delar):
                rensade_delar.append(del_)
            else:
                for del_samma in rensade_delar:
                    if del_samma.har_samma_enhet(del_):
                        del_samma *= del_
        nya_delar = [del_ for del_ in rensade_delar if del_.potens != 0]
        self.delar = nya_delar

    def namn(self):
        return self._namn

    def namnge(self, namn, kort, dimension):
        return Enhet(self.delar, namn, kort, dimension, self.faktor)

    def __mul__(self, other):
        if type(other) is Grundenhet:
            return Enhet(self.delar + [Delenhet(other, 1)], faktor = self.faktor)
        elif type(other) is Enhet:
            return Enhet(self.delar + other.delar, faktor = self.faktor * other.faktor)
        elif type(other) is int or type(other) is float:
            return Enhet(self.delar, self._namn, self.kort, self.dimension, self.faktor * other)

    __rmul__ = __mul__

    def __truediv__(self, other):
        return self * (other ** -1)

    __rtruediv__ = __truediv__

    def __pow__(self, other):
        mult_delar = []
        for del_ in self.delar:
            mult_delar.append(del_ ** other)
        return Enhet(mult_delar)

    def __repr__(self):
        beskrivning = ""
        if self._namn != "":
            beskrivning += self._namn
        if self.kort != "":
            beskrivning += f" ({self.kort})"
        if self.dimension != "":
            beskrivning += ", " + self.dimension
        if beskrivning != "":
            beskrivning += ": "
        definition = ""
        if self.faktor != 1:
            definition = str(self.faktor) + " "
        if self.delar == []:
            definition += "enhetslös"
        definition += " * ".join(str(delenh) for delenh in self.delar)
        return beskrivning + definition
