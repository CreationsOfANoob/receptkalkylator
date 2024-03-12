from .main import Grundenhet, Enhet

# SI-enheter
m = Grundenhet("meter", "m", "längd")
kg = Grundenhet("kilogram", "kg", "massa")

# Andra enheter
kr = Grundenhet("kronor", "kr", "värde")

# Härledda enheter
l = (0.001 * m * m * m).namnge("liter", "l", "volym")
ml = (0.001 * l).namnge("milliliter", "ml", "volym")
dl = (0.1 * l).namnge("deciliter", "dl", "volym")
tsk = (5 * ml).namnge("tesked", "tsk", "volym")
msk = (15 * ml).namnge("matsked", "msk", "volym")
p = (kg / l)


si_enheter = [m, kg]
andra_enheter = [kr]
harledda_enheter = [l, ml, dl, tsk, msk, p]
enheter = si_enheter + andra_enheter + harledda_enheter
