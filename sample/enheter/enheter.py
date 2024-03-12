from .main import Grundenhet, Enhet

# SI-enheter
m = Grundenhet("meter", "m", "längd")
kg = Grundenhet("kilogram", "kg", "massa")

# Andra enheter
kr = Grundenhet("kronor", "kr", "värde")

# Härledda enheter
l = m * m * m

if __name__=="__main__":
    print(l)
