from enum import Enum
from dataclasses import dataclass

# Alla enheter måste ha unika förkortningar.

@dataclass
class Grundenhet:
    id: int # Unik identifierare
    namn: str # t.ex. meter
    _kort: str # förkortning, t.ex. m
    dimension: str # t.ex. längd

    def kort(self):
        return self._kort

    def faktor(self):
        return 1

    def potens(self):
        return 1

    def har_samma_dimension(self, other):
        if type(other) is Grundenhet:
            if self.id is None or other.id is None:
                return self._kort == other._kort
            return self.id == other.id
        if type(other) is Enhet:
            return Enhet([Delenhet(self, 1)]).har_samma_dimension(other)

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
            return self.id == other.id
        #    if (not type(self.id) is None) and (not type(other.id) is None):
        #        return self.id == other.id
        #    return self._kort == other._kort
        return NotImplemented

    def __repr__(self):
        return f"{self.namn} ({self._kort}), {self.dimension}"

@dataclass
class Delenhet:
    enhet: Grundenhet
    _potens: int

    def har_samma_dimension(self, other):
        if type(other) is Delenhet:
            return self == other
        return NotImplemented

    def har_samma_grunddimension(self, other):
        if type(other) is Delenhet:
            return self.enhet == other.enhet
        return NotImplemented

    def potens(self):
        return self._potens

    def __mul__(self, other):
        return self.enhet * other

    __rmul__ = __mul__

    def __truediv__(self, other):
        return self.enhet / other

    def __rtruediv__(self, other):
        return other / self.enhet

    def __imul__(self, other):
        self._potens += other.potens()

    def __pow__(self, other):
        return Delenhet(self.enhet, self._potens * other)

    def __lt__(self, other):
        return self._potens > other.potens()

    def __eq__(self, other):
        if type(other) is Grundenhet:
            return self._potens == 1 and self.enhet == other
        if type(other) is Delenhet:
            return self._potens == other._potens and self.enhet == other.enhet
        return NotImplemented

    def __repr__(self):
        if self._potens == 1:
            return f"{self.enhet._kort}"
        return f"{self.enhet._kort}^{self._potens}"

@dataclass
class Enhet:
    delar: list[Delenhet]
    _namn: str = "" # t.ex. hektar
    _kort: str = "" # t.ex. ha
    dimension: str = "" # t.ex. area
    _faktor: float = 1 # t.ex. 10000.0

    def __post_init__(self):
        if type(self.delar) is Grundenhet:
            self.delar = [Delenhet(self.delar, 1)]
        if type(self.delar) is Enhet:
            faktor = self.delar._faktor * self._faktor
            self.delar = self.delar.delar
            self._faktor = faktor
        if any(type(del_) is not Delenhet for del_ in self.delar):
            raise(ValueError("Delar i Enhet måste vara lista med typen Delenhet"))
        # slå ihop dubbla enhetsdefinitioner
        rensade_delar = []
        for del_ in self.delar:
            if not any(del_.har_samma_grunddimension(del_tillagd) for del_tillagd in rensade_delar):
                rensade_delar.append(del_)
            else:
                for del_samma in rensade_delar:
                    if del_samma.har_samma_grunddimension(del_):
                        del_samma *= del_
        nya_delar = sorted([del_ for del_ in rensade_delar if del_.potens() != 0])
        self.delar = nya_delar

    @classmethod
    def enhetslos(cls):
        return Enhet([], _faktor = 1)

    def ar_enhetslos(self):
        return self.delar == []

    def namn(self):
        return self._namn

    def kort(self):
        if self._kort == "":
            return self.definition()
        return self._kort

    def definition(self):
        definition_ = " * ".join(str(delenh) for delenh in self.delar)
        return definition_

    def faktor(self):
        return self._faktor

    def potens(self):
        if len(self.delar) == 1:
            return self.delar[0].potens()

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

    def copy(self):
        return Enhet(self.delar, self._namn, self._kort, self.dimension, self._faktor)

    def __mul__(self, other):
        if other is None:
            return self.copy()
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
        definition += self.definition()
        return beskrivning + definition
