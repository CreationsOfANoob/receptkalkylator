from .main import Grundenhet, Enhet

# SI-enheter
m = Grundenhet("meter", "m", "längd")
kg = Grundenhet("kilogram", "kg", "massa")

# Andra enheter
kr = Grundenhet("kronor", "kr", "värde")

# Härledda enheter
l = (0.001 * m * m * m).namnge("liter", "l", "volym")
