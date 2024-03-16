import unittest
from .context import sample

ingrediens = sample.Ingrediens

tal = sample.enheter.Tal

class TestaIngredienser(unittest.TestCase):

    def testa_skapa_ingrediens_tolka(self):
        a = ingrediens.tolka('{"namn":"havregryn", "kilopris":"15 kr/kg"}')
        self.assertEqual(a.kilopris(), tal(15, "kr/kg"))

    def testa_ingrediens_till_dict(self):
        a = ingrediens("vetemjöl", kilopris = tal(10, "kr/kg")).till_dict()
        b = {"namn":"vetemjöl", "kilopris":tal(10, "kr/kg")}
        self.assertEqual(a, b)

if __name__=="__main__":
    unittest.main()
