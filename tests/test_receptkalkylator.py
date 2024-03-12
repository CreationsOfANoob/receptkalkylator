import unittest
from .context import sample

def grund(namn, kort, dimension):
    return sample.enheter.Grundenhet(namn, kort, dimension)

def delenh(kort, potens): # delenhet
    return sample.enheter.Delenhet(grund("", kort, ""), potens)

def samman(namn, kort, dimension, faktor, delar): # sammansatt enhet
    return sample.enheter.Enhet(delar, namn, kort, dimension, faktor)


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

    def testa_skapa_sammansatt_enhet_flera_av_samma(self):
        a = samman("kvadratmeter", "kvm", "area", 1, [delenh("m", 1), delenh("m", 1)])
        b = "kvadratmeter (kvm), area: m^2"
        self.assertEqual(repr(a), b)

    def testa_delenheter_har_samma_enhet_samma_potens(self):
        a = delenh("m", 1)
        b = delenh("m", 1)
        self.assertTrue(a.har_samma_enhet(b))

    def testa_delenheter_har_samma_enhet_olika_potens(self):
        a = delenh("m", 1)
        b = delenh("m", 2)
        self.assertTrue(a.har_samma_enhet(b))

    def testa_delenheter_har_olika_enhet(self):
        a = delenh("m", 1)
        b = delenh("km", 1)
        self.assertFalse(a.har_samma_enhet(b))

    def testa_compare_grundenheter_samma_namn(self):
        a = grund("meter", "m", "längd")
        b = grund("meter", "m", "längd")
        self.assertEqual(a, b)

    def testa_compare_grundenheter_olika_namn(self):
        a = grund("meter", "m", "längd")
        b = grund("metermeter", "m", "längd")
        self.assertEqual(a, b)

    def testa_skapa_enhetslos_enhet(self):
        a = samman("stycken", "st", "antal", 1, [])
        b = "stycken (st), antal: enhetslös"
        self.assertEqual(repr(a), b)

    def testa_dividera_enhetslos_enhet(self):
        m = grund("", "m", "")
        self.assertEqual(repr(m / m), "enhetslös")

    def testa_multiplicera_grundenheter_olika(self):
        a = grund("", "N", "") * grund("", "m", "")
        self.assertEqual(repr(a), "N * m")

    def testa_multiplicera_grundenheter_samma(self):
        a = grund("", "m", "") * grund("", "m", "")
        self.assertEqual(repr(a), "m^2")

    def testa_multiplicera_grundenhet_integer(self):
        a = grund("", "m", "") * 5
        self.assertEqual(repr(a), "5 m")

    def testa_multiplicera_integer_grundenhet(self):
        a = 5 * grund("", "m", "")
        self.assertEqual(repr(a), "5 m")

    def testa_multiplicera_integer_integer_grundenhet(self):
        a = 5 * 2 * grund("", "m", "")
        self.assertEqual(repr(a), "10 m")

    def testa_multiplicera_integer_grundenhet_grundenhet(self):
        m = grund("", "m", "")
        a = 5 * m * m
        self.assertEqual(repr(a), "5 m^2")

    def testa_multiplicera_grundenhet_grundenhet_integer(self):
        m = grund("", "m", "")
        a = m * m * 5
        self.assertEqual(repr(a), "5 m^2")

    def testa_multiplicera_float_grundenhet(self):
        a = 0.001 * grund("", "m", "")
        self.assertEqual(repr(a), "0.001 m")

    def testa_multiplicera_grundenhet_enhet(self):
        a = grund("", "kg", "") * samman("", "", "", 1, [delenh("W", 1)])
        self.assertEqual(repr(a), "kg * W")

    def testa_multiplicera_grundenhet_enhet_med_faktor(self):
        a = grund("", "kg", "") * samman("", "", "", 10, [delenh("W", 1)])
        self.assertEqual(repr(a), "10 kg * W")

    def testa_multiplicera_integer_enhet(self):
        a = 3 * samman("", "", "", 1, [delenh("W", 1)])
        self.assertEqual(repr(a), "3 W")

    def testa_multiplicera_enhet_integer(self):
        a = samman("", "", "", 1, [delenh("W", 1)]) * 4
        self.assertEqual(repr(a), "4 W")

    def testa_multiplicera_enhet_float(self):
        a = 0.1 * samman("", "", "", 1, [delenh("W", 1)])
        self.assertEqual(repr(a), "0.1 W")

    def testa_exponent_grundenhet(self):
        a = grund("", "m", "") ** 2
        self.assertEqual(repr(a), "m^2")

    def testa_division_grundenhet_int(self):
        a = grund("", "m", "") / 2
        self.assertEqual(repr(a), "0.5 m")

    def testa_division_int_grundenhet(self):
        a = 1 / grund("", "m", "")
        self.assertEqual(repr(a), "m^-1")

    def testa_division_enhet_int(self):
        m = samman("", "", "", 1, [delenh("m", 1)])
        a = m / 2
        self.assertEqual(repr(a), "0.5 m")

    def testa_division_int_enhet(self):
        m = samman("", "", "", 1, [delenh("m", 1)])
        s = samman("", "", "", 1, [delenh("s", 1)])
        a = m / s**2
        self.assertEqual(repr(a), "m * s^-2")

    def testa_division_grundenhet_enhet(self):
        m = samman("", "", "", 1, [delenh("m", 1)])
        s = grund("", "s", "")
        a = m / s**2
        self.assertEqual(repr(a), "m * s^-2")

    def testa_byt_namn_enhet(self):
        a = samman("", "", "", 1, [delenh("m", 1)]).namnge("meter", "m", "längd")
        self.assertEqual(repr(a), "meter (m), längd: m")

    def testa_byt_namn_enhet_med_faktor(self):
        a = samman("", "", "", 1000, [delenh("m", 1)]).namnge("kilometer", "km", "längd")
        self.assertEqual(repr(a), "kilometer (km), längd: 1000 m")

    def testa_byt_namn_enhet_med_faktor_float(self):
        a = samman("", "", "", 0.001, [delenh("m", 1)]).namnge("millimeter", "mm", "längd")
        self.assertEqual(repr(a), "millimeter (mm), längd: 0.001 m")

    def testa_byt_namn_enhet_med_faktor_float_multiplicerad(self):
        a = (0.001 * samman("", "", "", 1, [delenh("m", 1)])).namnge("millimeter", "mm", "längd")
        self.assertEqual(repr(a), "millimeter (mm), längd: 0.001 m")

class TestaStorheter(unittest.TestCase):
    pass


if __name__ == "__main__":
    unittest.main()
