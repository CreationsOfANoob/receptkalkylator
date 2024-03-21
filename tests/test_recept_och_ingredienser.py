import unittest
from .context import sample

ingrediens = sample.Produkt
ingredienslista = sample.Produktkatalog
tal = sample.enheter.Tal
recept = sample.Recept

class TestaIngredienser(unittest.TestCase):

    def testa_tolka_ingrediens_kilopris(self):
        a = ingrediens.tolka('{"namn":"havregryn", "mätvärden":["15 kr/kg"]}')
        self.assertEqual(a.kilopris(), tal(15, "kr/kg"))

    def testa_tolka_ingrediens_kilopris_invers(self):
        a = ingrediens.tolka('{"namn":"havregryn", "mätvärden":["0.1 kg/kr"]}')
        self.assertEqual(a.kilopris(), tal(10, "kr/kg"))

    def testa_tolka_ingrediens_med_styckpris_och_styckvikt_kilopris(self):
        a = ingrediens.tolka('{"namn":"havregryn", "mätvärden":["10 kr/st", "0.2 kg/st"]}')
        self.assertEqual(a.kilopris(), tal(50, "kr/kg"))

    def testa_tolka_ingrediens_med_styckpris_och_volymstyck_kilopris(self):
        a = ingrediens.tolka('{"namn": "citronsaft","mätvärden":["5 kr/st", "0,4 dl/st"]}')
        b = a.pris(tal(1, sample.enheter.msk))
        self.assertEqual(b, tal(1.875, "kr"))

    def testa_ingrediens_till_dict(self):
        a = ingrediens("vetemjöl", [tal(10, "kr/kg")]).till_dict()
        b = {"namn":"vetemjöl", "mätvärden":[tal(10, "kr/kg")]}
        self.assertEqual(a, b)


class TestaRecept(unittest.TestCase):

    recept_1_text = """{"ingredienser":["10 dl havregryn", "1 dl hasselnötter", "1,5 dl råsocker", "2 dl vatten", "5 msk rapsolja", "1 dl pumpakärnor", "1 dl linfrö"], "portioner":15}"""
    ingredienskatalog_1_text = '''{"produkter":
    [
        {"namn":"råsocker", "mätvärden":["50 kr/kg", "85 g/dl"]},
        {"namn":"hasselnötter", "mätvärden":["200 kr/kg", "70 g/dl"]},
        {"namn":"vatten", "mätvärden":["1 kg/l", "0 kr/l"]},
        {"namn":"rapsolja", "mätvärden":["30 kr/l", "90 g/dl"]},
        {"namn":"pumpakärnor", "mätvärden":["130 kr/kg", "40 g/dl"]},
        {"namn":"havregryn", "mätvärden":["15 kr/kg", "35 g/dl"]},
        {"namn":"linfrö", "mätvärden":["60 kr/kg", "60 g/dl"]}
    ]}'''

    def testa_enkel_totalkostnad(self):
        a = ingredienslista.tolka('{"produkter":[{"namn":"mjöl", "mätvärden":["10 kr/kg", "10 dl/kg"]}]}')
        b = recept.tolka('{"ingredienser":["1 dl mjöl"]}', a)
        c = b.totalkostnad()
        self.assertEqual(c, tal.tolka("1 kr"))

    def testa_enkel_totalkostnad_tva_produkter(self):
        a = ingredienslista.tolka('{"produkter":[{"namn":"mjöl", "mätvärden":["10 kr/kg", "10 dl/kg"]}, {"namn":"salt", "mätvärden":["12 kr/kg", "130 g/dl"]}]}')
        b = recept.tolka('{"ingredienser":["1 dl mjöl", "2 tsk salt"]}', a)
        c = b.totalkostnad()
        self.assertEqual(c, tal.tolka("1,156 kr"))

    def testa_totalkostnad_recept(self):
        a = ingredienslista.tolka(TestaRecept.ingredienskatalog_1_text)
        b = recept.tolka(TestaRecept.recept_1_text, a)
        c = b.totalkostnad()
        self.assertEqual(c, tal.tolka("36,675 kr"))

    def testa_portionskostnad_recept(self):
        a = ingredienslista.tolka(TestaRecept.ingredienskatalog_1_text)
        b = recept.tolka(TestaRecept.recept_1_text, a)
        c = b.portionskostnad()
        self.assertEqual(c, tal.tolka("2,445 kr"))

if __name__=="__main__":
    unittest.main()
