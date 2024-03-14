from .main import Grundenhet, Enhet

# SI-enheter
m = Grundenhet("meter", "m", "sträcka")
kg = Grundenhet("kilogram", "kg", "massa")
s = Grundenhet("sekunder", "s", "tid")

# Andra enheter
kr = Grundenhet("kronor", "kr", "värde")
enhetslos = Enhet.enhetslos()

# Härledda enheter
km = (1000 * m).namnge("kilometer", "km", "sträcka")
l = (0.001 * m * m * m).namnge("liter", "l", "volym")
ml = (0.001 * l).namnge("milliliter", "ml", "volym")
dl = (0.1 * l).namnge("deciliter", "dl", "volym")
tsk = (5 * ml).namnge("tesked", "tsk", "volym")
msk = (15 * ml).namnge("matsked", "msk", "volym")
p = (kg / (m * m * m)).namnge("", "kg/m^3", "densitet")


si_enheter = [m, kg]
andra_enheter = [kr]
harledda_enheter = [l, ml, dl, tsk, msk, p]
enheter = si_enheter + andra_enheter + harledda_enheter + [enhetslos]
