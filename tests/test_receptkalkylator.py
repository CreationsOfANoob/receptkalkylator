import unittest
from .context import sample

def grund(namn, kort, dimension):
    return sample.enheter.Grundenhet(namn, kort, dimension)

def delenh(kort, potens): # delenhet
    return sample.enheter.Delenhet(grund("", kort, ""), potens)

def samman(namn, kort, dimension, faktor, delar): # sammansatt enhet
    return sample.enheter.Enhet(namn, kort, dimension, faktor, delar)


class TestaEnheter(unittest.TestCase):

    def testa_skriva_grundenhet(self):
        a = grund("meter", "m", "längd")
        b = "meter (m), längd"
        self.assertEqual(repr(a), b)

    def testa_skriva_enhet(self):
        a = samman("hektar", "ha", "area", 10000, [delenh("m", 2)])
        b = "hektar (ha), area: 10000 m^2"
        self.assertEqual(repr(a), b)

    def testa_skriva_enhet_flera_grundenheter(self):
        a = samman("meter per sekund", "m/s", "hastighet", 1, [delenh("m", 1), delenh("s", -1)])
        b = "meter per sekund (m/s), hastighet: m * s^-1"
        self.assertEqual(repr(a), b)

if __name__ == "__main__":
    unittest.main()
