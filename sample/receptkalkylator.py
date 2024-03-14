import enheter as enh

if __name__=="__main__":
    for enhet in enh.enheter:
        print(enhet)
    print()
    print(enh.Tal(10, enh.m))
    print(enh.Tal.tolka("10 dl"))
