import unittest
from .context import sample

m = sample.enheter.m
km = sample.enheter.km
s = sample.enheter.s
dl = sample.enheter.dl
enhetslos = sample.enheter.Enhet([], "enhetslös", "", "", 1)

def grund(namn, kort, dimension):
    return sample.enheter.Grundenhet(namn, kort, dimension)

def delenh(kort, potens): # delenhet
    return sample.enheter.Delenhet(grund("", kort, ""), potens)

def samman(namn, kort, dimension, faktor, delar): # sammansatt enhet
    return sample.enheter.Enhet(delar, namn, kort, dimension, faktor)

def tal(kvantitet, enhet):
    return sample.enheter.Tal(kvantitet, enhet)

def tolka_tal(text):
    return sample.enheter.Tal.tolka(text)

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

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

    def testa_delenheter_har_samma_dimension_samma_potens(self):
        a = delenh("m", 1)
        b = delenh("m", 1)
        self.assertTrue(a.har_samma_dimension(b))

    def testa_delenheter_har_samma_grundenhet_olika_potens(self):
        a = delenh("m", 1)
        b = delenh("m", 2)
        self.assertFalse(a.har_samma_dimension(b))

    def testa_delenheter_har_olika_enhet(self):
        a = delenh("m", 1)
        b = delenh("km", 1)
        self.assertFalse(a.har_samma_dimension(b))

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
        self.assertEqual(repr(m / m), "enhetslös")

    def testa_multiplicera_grundenheter_olika(self):
        a = grund("", "N", "") * m
        self.assertEqual(repr(a), "N * m")

    def testa_multiplicera_grundenheter_samma(self):
        a = m * m
        self.assertEqual(repr(a), "m^2")

    def testa_multiplicera_grundenhet_integer(self):
        a = m * 5
        self.assertEqual(repr(a), "5 m")

    def testa_multiplicera_integer_grundenhet(self):
        a = 5 * m
        self.assertEqual(repr(a), "5 m")

    def testa_multiplicera_integer_integer_grundenhet(self):
        a = 5 * 2 * m
        self.assertEqual(repr(a), "10 m")

    def testa_multiplicera_integer_grundenhet_grundenhet(self):
        a = 5 * m * m
        self.assertEqual(repr(a), "5 m^2")

    def testa_multiplicera_grundenhet_grundenhet_integer(self):
        a = m * m * 5
        self.assertEqual(repr(a), "5 m^2")

    def testa_multiplicera_float_grundenhet(self):
        a = 0.001 * m
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

    def testa_multiplikation_enhet_faktor_enhet_faktor_samma(self):
        a = samman("", "", "", 3, [delenh("s", 1)])
        b = samman("", "", "", 4, [delenh("s", 1)])
        c = a * b
        self.assertEqual(repr(c), "12 s^2")

    def testa_multiplikationion_enhet_faktor_enhet_faktor_olika(self):
        a = samman("", "", "", 10, [delenh("s", 1)])
        b = samman("", "", "", 2, [delenh("m", 1)])
        c = a * b
        self.assertEqual(repr(c), "20 s * m")

    def testa_exponent_grundenhet(self):
        a = m ** 2
        self.assertEqual(repr(a), "m^2")

    def testa_division_grundenhet_int(self):
        a = m / 2
        self.assertEqual(repr(a), "0.5 m")

    def testa_division_int_grundenhet(self):
        a = 1 / m
        self.assertEqual(repr(a), "m^-1")

    def testa_division_enhet_int(self):
        m = samman("", "", "", 1, [delenh("m", 1)])
        a = m / 2
        self.assertEqual(repr(a), "0.5 m")

    def testa_division_int_enhet(self):
        m = samman("", "", "", 1, [delenh("m", 1)])
        a = 1 / m
        self.assertEqual(repr(a), "m^-1")

    def testa_multiplicera_division_int_enhet(self):
        m = samman("", "", "", 1, [delenh("m", 1)])
        s = samman("", "", "", 1, [delenh("s", 1)])
        a = s * (1 / m)
        self.assertEqual(repr(a), "s * m^-1")

    def testa_multiplicera_division_int_enhet_speglad(self):
        m = samman("", "", "", 1, [delenh("m", 1)])
        s = samman("", "", "", 1, [delenh("s", 1)])
        a = (1 / m) * s
        self.assertEqual(repr(a), "s * m^-1")

    def testa_division_int_enhet(self):
        m = samman("", "", "", 1, [delenh("m", 1)])
        s = samman("", "", "", 1, [delenh("s", 1)])
        a = m / s**2
        self.assertEqual(repr(a), "m * s^-2")

    def testa_division_grundenhet_enhet(self):
        m_ = samman("", "", "", 1, [delenh("m", 1)])
        a = m_ / s**2
        self.assertEqual(repr(a), "m * s^-2")

    def testa_division_grundenhet_grundenhet_multiplicerad(self):
        a = m / (s*s)
        self.assertEqual(repr(a), "m * s^-2")

    def testa_division_grundenhet_enhet_med_faktor(self):
        h = samman("", "", "", 3600, [delenh("s", 1)])
        km = 1000 * m
        a = h / km
        self.assertEqual(repr(a), "3.6 s * m^-1")

    def testa_division_enhet_faktor_enhet_faktor_samma(self):
        a = samman("", "", "", 3, [delenh("s", 1)])
        b = samman("", "", "", 4, [delenh("s", 1)])
        c = a / b
        self.assertEqual(repr(c), "0.75 enhetslös")

    def testa_division_enhet_faktor_enhet_faktor_olika(self):
        a = samman("", "", "", 10, [delenh("s", 1)])
        b = samman("", "", "", 2, [delenh("m", 1)])
        c = a / b
        self.assertEqual(repr(c), "5 s * m^-1")

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

    def testa_enhet_samma_enhet_olika_ordning(self):
        a = samman("", "", "", 1, [delenh("m", 1), delenh("s", -1)])
        b = samman("", "", "", 1, [delenh("s", -1), delenh("m", 1)])
        self.assertTrue(a == b)

    def testa_enhet_olika_enhet_olika_ordning(self):
        a = samman("", "", "", 1, [delenh("m", 1), delenh("s", -1)])
        b = samman("", "", "", 1, [delenh("s", -2), delenh("m", 1)])
        self.assertFalse(a == b)

    def testa_enhet_samma_grundenhet_samma(self):
        a = m
        b = samman("", "", "", 1, [delenh("m", 1)])
        self.assertEqual(a, b)

    def testa_skapa_enhetslos_enhet_funktion(self):
        a = sample.enheter.Enhet.enhetslos()
        self.assertEqual(a, samman("", "", "", 1, []))


class TestaTal(unittest.TestCase):

    def testa_repr_tal(self):
        a = tal(1, m)
        self.assertEqual(repr(a), "1 m")

    def testa_repr_tal_fel(self):
        a = tal(10, m)
        self.assertNotEqual(repr(a), "1 m")

    def testa_repr_tal_harledd_enhet(self):
        a = tal(10, dl)
        self.assertEqual(repr(a), "1 l")

    def testa_compare_tal_samma(self):
        a = tal(1, m)
        b = tal(1, m)
        self.assertTrue(a == b)

    def testa_compare_tal_olika_kvantitet(self):
        a = tal(1, m)
        b = tal(2, m)
        self.assertFalse(a == b)

    def testa_compare_tal_olika_enhet(self):
        a = tal(1, m)
        b = tal(1, s)
        self.assertFalse(a == b)

    def testa_addera_olika_enheter_fel(self):
        a = tal(10, m)
        b = tal(5, s)
        self.assertRaises(ValueError, add, a, b)

    def testa_addera_tal_samma_enhet(self):
        a = tal(1, m)
        b = tal(2, m)
        self.assertEqual(a + b, tal(3, m))

    def testa_subtrahera_olika_enheter_fel(self):
        a = tal(10, m)
        b = tal(5, s)
        self.assertRaises(ValueError, subtract, a, b)

    def testa_subtrahera_tal_samma_enhet(self):
        a = tal(1, m)
        b = tal(2, m)
        self.assertEqual(a - b, tal(-1, m))

    def testa_multiplicera_tal_samma_enhet(self):
        a = tal(2, m)
        b = tal(2, m)
        self.assertEqual(a * b, tal(4, m * m))

    def testa_multiplicera_tal_olika_enhet(self):
        a = tal(2, m)
        b = tal(2, s)
        self.assertEqual(a * b, tal(4, m * s))

    def testa_dividera_tal_samma_enhet(self):
        a = tal(2, m)
        b = tal(2, m)
        self.assertEqual(a / b, tal(1, enhetslos))

    def testa_dividera_tal_olika_enhet(self):
        a = tal(2, m)
        b = tal(2, s)
        self.assertEqual(a / b, tal(1, m * s**-1))

    def testa_tolka_string_till_tal(self):
        a = tal(10, m)
        b = tolka_tal("10 m")
        self.assertEqual(a, b)

    def testa_tolka_string_till_tal_komplex(self):
        a = tal(10, 0.001 * m * m * m)
        b = tolka_tal("100 dl")
        self.assertEqual(a, b)

    def testa_tolka_string_till_tal_komplex_fel(self):
        a = tal(10, 0.001 * m * m * m)
        b = tolka_tal("10 l")
        self.assertEqual(a, b)

    def testa_skapa_tal_harledd_enhet(self):
        a = tal(2000, m)
        b = tal(2, km)
        self.assertEqual(a / b, tal(1, enhetslos))


if __name__ == "__main__":
    unittest.main()
