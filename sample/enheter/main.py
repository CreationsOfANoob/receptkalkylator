from enum import Enum
from dataclasses import dataclass

# Alla enheter måste ha unika förkortningar.

@dataclass
class Grundenhet:
    namn: str # t.ex. meter
    _kort: str # förkortning, t.ex. m
    dimension: str # t.ex. längd

    def kort(self):
        return self._kort

    def faktor(self):
        return 1

    def har_samma_dimension(self, other):
        return self == other

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
        if type(other) is Grundenhet:
            return self._kort == other._kort
        return NotImplemented

    def __repr__(self):
        return f"{self.namn} ({self._kort}), {self.dimension}"

@dataclass
class Delenhet:
    enhet: Grundenhet
    potens: int

    def har_samma_dimension(self, other):
        if type(other) is Delenhet:
            return self == other
        return NotImplemented

    def har_samma_grunddimension(self, other):
        if type(other) is Delenhet:
            return self.enhet == other.enhet
        return NotImplemented

    def __imul__(self, other):
        self.potens += other.potens

    def __pow__(self, other):
        return Delenhet(self.enhet, self.potens * other)

    def __lt__(self, other):
        return self.potens > other.potens#(self.enhet.kort() < other.enhet.kort() and self.potens == other.potens) or self.potens < other.potens

    def __eq__(self, other):
        if type(other) is Grundenhet:
            return self.potens == 1 and self.enhet == other
        if type(other) is Delenhet:
            return self.potens == other.potens and self.enhet == other.enhet
        return NotImplemented

    def __repr__(self):
        if self.potens == 1:
            return f"{self.enhet._kort}"
        return f"{self.enhet._kort}^{self.potens}"

@dataclass
class Enhet:
    delar: list[Delenhet]
    _namn: str = "" # t.ex. hektar
    _kort: str = "" # t.ex. ha
    dimension: str = "" # t.ex. area
    _faktor: float = 1 # t.ex. 10000.0

    def __post_init__(self):
        # slå ihop dubbla enhetsdefinitioner
        rensade_delar = []
        for del_ in self.delar:
            if not any(del_.har_samma_grunddimension(del_tillagd) for del_tillagd in rensade_delar):
                rensade_delar.append(del_)
            else:
                for del_samma in rensade_delar:
                    if del_samma.har_samma_grunddimension(del_):
                        del_samma *= del_
        nya_delar = sorted([del_ for del_ in rensade_delar if del_.potens != 0])
        self.delar = nya_delar

    @classmethod
    def enhetslos(cls):
        return Enhet([], _faktor = 1)

    def namn(self):
        return self._namn

    def kort(self):
        return self._kort

    def faktor(self):
        return self._faktor

    def namnge(self, namn, kort, dimension):
        return Enhet(self.delar, namn, kort, dimension, self._faktor)

    def har_samma_dimension(self, other):
        if type(other) is Enhet:
            return sorted(self.delar) == sorted(other.delar)
        elif type(other) is Grundenhet:
            if len(self.delar) == 1:
                return self.delar[0] == other
            return False
        return NotImplemented

    def __mul__(self, other):
        if type(other) is Grundenhet:
            return Enhet(self.delar + [Delenhet(other, 1)], _faktor = self._faktor)
        elif type(other) is Enhet:
            return Enhet(self.delar + other.delar, _faktor = self._faktor * other._faktor)
        elif type(other) is int or type(other) is float:
            return Enhet(self.delar, self._namn, self._kort, self.dimension, self._faktor * other)

    __rmul__ = __mul__

    def __truediv__(self, other):
        return self * (other ** -1)

    def __rtruediv__(self, other):
        return (self ** -1) * other

    def __pow__(self, other):
        mult_delar = []
        for del_ in self.delar:
            mult_delar.append(del_ ** other)
        return Enhet(mult_delar, _faktor = pow(self._faktor, other))

    def __eq__(self, other):
        if type(other) is Enhet:
            return self._faktor == other._faktor and sorted(self.delar) == sorted(other.delar)
        if type(other) is Grundenhet:
            if len(self.delar) == 1:
                return self._faktor == 1 and self.delar[0] == other
            return False
        return NotImplemented

    def __repr__(self):
        beskrivning = ""
        if self._namn != "":
            beskrivning += self._namn
        if self._kort != "":
            beskrivning += f" ({self._kort})"
        if self.dimension != "":
            beskrivning += ", " + self.dimension
        if beskrivning != "":
            beskrivning += ": "
        definition = ""
        if self._faktor != 1:
            definition = f"{self._faktor:g} "
        if self.delar == []:
            definition += "enhetslös"
        definition += " * ".join(str(delenh) for delenh in self.delar)
        return beskrivning + definition
