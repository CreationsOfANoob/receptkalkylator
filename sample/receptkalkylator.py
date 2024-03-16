import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import sample.enheter as enh
import json


class Ingrediens:

    def __init__(self, namn, kilopris = None, styckpris = None):
        self.namn = namn
        self._kilopris = kilopris
        self._styckpris = styckpris

    @classmethod
    def tolka(cls, str_):
        ing_dict = json.loads(str_)
        namn = ing_dict.get("namn", "")
        kilopris = ing_dict.get("kilopris", None)
        styckpris = ing_dict.get("styckpris", None)
        return(Ingrediens(namn, kilopris, styckpris))

    def kilopris(self):
        if not self._kilopris is None:
            return self._kilopris
        return None

    def till_dict(self):
        dict = {"namn":self.namn}
        if not self._kilopris is None:
            dict["kilopris"] = self._kilopris
        if not self._styckpris is None:
            dict["styckpris"] = self._styckpris
        return dict


if __name__=="__main__":
    for enhet in enh.enheter:
        print(enhet)
    print()
    print(enh.Tal(10, enh.m))
    print(enh.Tal.tolka("10 dl"))
