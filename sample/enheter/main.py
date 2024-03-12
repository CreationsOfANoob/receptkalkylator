from enum import Enum
from dataclasses import dataclass

@dataclass
class Grundenhet:
    namn: str # t.ex. meter
    kort: str # förkortning, t.ex. m
    dimension: str # t.ex. längd

    def __repr__(self):
        return f"{self.namn} ({self.kort}), {self.dimension}"

@dataclass
class Delenhet:
    enhet: Grundenhet
    potens: int

    def __repr__(self):
        if self.potens == 1:
            return f"{self.enhet.kort}"
        return f"{self.enhet.kort}^{self.potens}"

@dataclass
class Enhet:
    namn: str # t.ex. hektar
    kort: str # t.ex. ha
    dimension: str # t.ex. area
    faktor: float # t.ex. 10000.0
    delar: list[Delenhet]

    def __repr__(self):
        definition = ""
        if self.faktor != 1:
            definition = str(self.faktor) + " "
        definition += " * ".join(str(delenh) for delenh in self.delar)
        return f"{self.namn} ({self.kort}), {self.dimension}: {definition}"
