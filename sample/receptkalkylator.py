from .enheter import enheter as enh


class Ingrediens:

    def __init__(self):
        pass

    @classmethod
    def tolka(cls, str_):
        return(Ingrediens())

    def kilopris(self):
        return 1

if __name__=="__main__":
    for enhet in enh.enheter:
        print(enhet)
    print()
    print(enh.Tal(10, enh.m))
    print(enh.Tal.tolka("10 dl"))
