# coding=utf-8
import os
import json
import cmd
import tempfile
import subprocess
import sample
from dataclasses import dataclass


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    YELLOW = '\033[93m'


def text_color(text, color):
    return color + text + bcolors.ENDC

def indexsiffra(index):
    return f"{text_color(f'[{index}]', bcolors.HEADER)}"

nummer_str = text_color("[NUMMER]", bcolors.HEADER)

def clear():
    print("\033[2J\033[0;0H", end = "")

def recept_file_exists(receptfilnamn):
    return os.path.isfile(os.path.join("data", "recept", f"{receptfilnamn}.json"))

def create_recept_file(receptfilnamn):
    filsokvag = os.path.join("data", "recept", f"{receptfilnamn}.json")
    with open(filsokvag, "w+") as file:
        pass
    return DataFromFile(filsokvag, None)

def hitta_alla_filer(sokvag):
    return [os.path.join(sokvag, f) for f in os.listdir(sokvag) if os.path.isfile(os.path.join(sokvag, f))]

def pretty_print_files():
    filsokvagar = hitta_alla_filer(os.path.join("data", "recept")) + hitta_alla_filer(os.path.join("data", "råvaror"))
    for filsokvag in filsokvagar:
        with open(filsokvag, "r") as file:
            contents = file.read()
            json_contents = json.loads(contents) if not contents == "" else {}
        with open(filsokvag, "w") as file:
            file.write(json.dumps(json_contents, indent = 4, ensure_ascii = False))

def ladda_fil_ur_data(mapp, funk = None, args = None):
    filsokvagar = hitta_alla_filer(os.path.join("data", mapp))
    filedata = []
    for filsokvag in filsokvagar:
        with open(filsokvag, "r") as file:
            data = file.read()
            try:
                data = funk(data, *args)
            except TypeError:
                try:
                    data = funk(data, args)
                except TypeError:
                    try:
                        data = funk(data)
                    except TypeError:
                        pass
            try:
                print(data, args)
            except:
                pass
            filedata.append(DataFromFile(filsokvag, data))
    return filedata

def ladda_recept(produktkatalog):
    recept_filer = ladda_fil_ur_data("recept", sample.Recept.tolka, produktkatalog)
    return recept_filer

def ladda_produktkatalog():
    fil_lista = ladda_fil_ur_data("råvaror", sample.Produktkatalog.tolka)
    produktkatalog = fil_lista[0]
    return produktkatalog

def ny_ingrediens():
    pass

def lista_kommandon(kontext):
    print(f"{kontext["namn"]}\n\nTillgängliga kommandon:")
    kommandon = kontext["komm"] + [kmd.AVSLUTA]
    for k in kommandon:
        menynamn = kontext.get('namn', 'Namnlös meny')
        print(f"  {k.namn.format(nummer = nummer_str)}:  {k.beskrivning.format(namn = menynamn)}")
    print()

def lista_recept(recept):
    for i, r in enumerate(recept):
        print(f"{indexsiffra(i)} {r.data.rubrik}")
    print()

def lista_ingredienser(ingr):
    for i, r in enumerate(ingr):
        invalid_str = ""
        if r._temp:
            invalid_str = text_color("Odefinierad men finns i recept", bcolors.RED)
        print(f"{indexsiffra(i)} {r.namn} {invalid_str}")
    print()

def print_line(maxbredd = 500, tecken = "-"):
    bredd = min(maxbredd, os.get_terminal_size().columns)
    print((tecken*bredd)[:bredd])

def print_recept(recept):
    print(text_color(str(recept), bcolors.BOLD))
    print()
    print(str(round(recept.data.portionskostnad(), 1)) + " per portion")

def print_ingrediens(ingrediens):
    print(text_color(ingrediens.namn, bcolors.BOLD))
    print(f"Mätvärden:\n{'\n'.join([str(i) for i in ingrediens.matvarden()])}")

def produkt_ar_temporar(ingrediens):
    try:
        return ingrediens.produkt._temp
    except AttributeError:
        return False

def redigera_med_cli(text):
    t = tempfile.NamedTemporaryFile(delete = False)
    with open(t.name, "w") as file:
        file.write(f"{text}")#.encode("utf-8"))
    subprocess.call([global_editor, t.name, "-L"])
    with open(t.name, "r") as file:
        text_ut = file.read()
    return text_ut


class DataFromFile:
    def __init__(self, filsokvag, content):
        self.filsokvag = filsokvag
        self.data = content

    def save(self):
        with open(self.filsokvag, "w") as file:
            try:
                file.write(self.content_to_str())
            except TypeError:
                pass

    def content_to_str(self):
        if type(self.data) is sample.Recept or type(self.data) is sample.Produktkatalog:
            return json.dumps(self.data.till_dict())

    def __repr__(self):
        return str(self.data)


class Ruta:
    "Basklass för ett fält i en Redigerare"
    def __init__(self, namn, object, attribute):
        self.namn = namn
        self.object = object
        self.attribute = attribute

    def set(self, value):
        setattr(self.object, self.attribute, value)

    def get(self):
        return getattr(self.object, self.attribute)

    def redigera(self):
        pass

    def print(self):
        pass

class StrRuta(Ruta):
    def redigera(self):
        text = redigera_med_cli(self.get())
        self.set(text)

    def print(self):
        text = self.get()
        if type(text) is str:
            if len(text) > 20:
                text = text[:20] + "[...]"
        print(f"{self.namn}:  '{text}'")

class IntRuta(Ruta):
    def redigera(self):
        clear()
        print(f"Nuvarande värde: {self.get()}\nNytt värde:\n: ", end = "")
        inp = input()
        self.set(inp)

    def print(self):
        print(f"{self.namn}: {self.get()}")

class ListRuta(Ruta):
    def __init__(self, namn, object, attribute, funk, arg = None, is_invalid_func = None, invalid_str = None):
        Ruta.__init__(self, namn, object, attribute)
        self.funk = funk
        self.arg = arg
        self.is_invalid_func = is_invalid_func
        self.invalid_str = invalid_str

    def redigera(self):
        text_in = f"{',\n'.join([str(it) for it in self.get()])}"
        text_ut = redigera_med_cli(text_in)
        lista_parsed = text_ut.split(",\n")
        lista = []
        for str_ in lista_parsed:
            if self.arg is None:
                lista.append(self.funk(str_))
            else:
                lista.append(self.funk(str_, self.arg))
        self.set(lista)

    def print(self):
        print(f"{self.namn}:")
        for it in self.get():
            text = str(it)
            if not self.is_invalid_func is None:
                if self.is_invalid_func(it):
                    text += self.invalid_str
            print(f"  {text}")


class Redigerare:
    def __init__(self, datafromfileobject, rutor):
        self._data = datafromfileobject
        self._rutor = rutor

    @classmethod
    def tom(cls):
        return Redigerare(None, [])

    def redigera_ruta(self, index):
        self._rutor[index].redigera()
        self._data.save()
        pretty_print_files()

    def print(self):
        print_line(100, "* ")
        for i, ruta in enumerate(self._rutor):
            print(f"\n{indexsiffra(i)} ", end = "")
            ruta.print()
        print()
        print_line(100, "* ")


@dataclass
class Kommando:
    namn: str
    beskrivning: str

class kmd:
    UPP = Kommando("UPP", "Gå till överordnad sida")
    RECEPT = Kommando("REC", "Visa alla recept")
    INGREDIENSER = Kommando("INGR", "Visa alla ingredienser")
    VISA = Kommando("VISA {nummer}", "Visa objekt med NUMMER")
    ANDRA = Kommando("MOD", "Ändra {namn}")
    ANDRAINDEX = Kommando("MOD {nummer}", "Ändra objekt med NUMMER")
    PRIS = Kommando("PRIS", "Visa ytterligare prisinformation")
    SKAPA = Kommando("SKAPA 'NAMN'", "Skapa nytt objekt med NAMN")
    AVSLUTA = Kommando("Q / AVSLUTA", "Avsluta")

class Kontext:
    HUVUDMENY = {"namn":"HUVUDMENY",
        "komm": [kmd.RECEPT, kmd.INGREDIENSER]}
    RECEPTLISTA = {"upp":HUVUDMENY, "namn":"RECEPT",
        "komm": [kmd.UPP, kmd.VISA, kmd.ANDRAINDEX, kmd.SKAPA]}
    RECEPTVY = {"upp":RECEPTLISTA, "namn":"RECEPT",
        "komm": [kmd.UPP, kmd.ANDRA, kmd.PRIS]}
    RECEPTREDIGERARE = {"upp":RECEPTVY, "namn":"REDIGERA RECEPT",
        "komm": [kmd.UPP, kmd.ANDRAINDEX]}
    INGREDIENSLISTA = {"upp":HUVUDMENY, "namn": "INGREDIENSER",
        "komm": [kmd.UPP, kmd.ANDRAINDEX, kmd.SKAPA]}
    INGREDIENSVY = {"upp":INGREDIENSLISTA, "namn":"INGREDIENS",
        "komm": [kmd.UPP, kmd.ANDRA]}
    INGREDIENSREDIGERARE = {"upp":INGREDIENSVY, "namn":"REDIGERA INGREDIENS",
        "komm": [kmd.UPP, kmd.ANDRAINDEX]}
    # Lägg till cirkulära referenser
    RECEPTLISTA["ned"] = RECEPTVY
    INGREDIENSLISTA["ned"] = INGREDIENSVY


class ReceptShell(cmd.Cmd):
    intro = ""#Välkommen till Receptkalkylatorn.\n"#Skriv help eller ? för en lista över kommandon.\n"
    prompt = ": "

    def preloop(self):
        pretty_print_files()
        self.produktkatalog = ladda_produktkatalog()
        self.recept = ladda_recept(self.produktkatalog.data)
        self.kontext = Kontext.HUVUDMENY
        self.visa_id = 0
        self.redigerare = Redigerare.tom()
        self.precmd()

    def precmd(self, line = ""):
        clear()
        print("Välkommen till Receptkalkylatorn.\n")
        lista_kommandon(self.kontext)
        print_line(100, "=")
        match self.kontext:
            case Kontext.RECEPTLISTA:
                lista_recept(self.recept)
            case Kontext.RECEPTVY:
                print_recept(self.recept[self.visa_id])
            case Kontext.RECEPTREDIGERARE:
                aktuellt_recept = self.recept[self.visa_id]
                print(aktuellt_recept.filsokvag)
                self.redigerare.print()
            case Kontext.INGREDIENSLISTA:
                lista_ingredienser(self.produktkatalog.data.produkter)
            case Kontext.INGREDIENSVY:
                print_ingrediens(self.produktkatalog.data.produkter[self.visa_id])
            case Kontext.INGREDIENSREDIGERARE:
                self.redigerare.print()
        print_line(100, "=")
        return line.lower()

    def byt_kontext(self, kontext, tyst = False):
        self.kontext = kontext
        if not tyst:
            self.precmd()

    def andra_falt(self, arg):
        try:
            index = int(arg)
        except ValueError:
            print(f"Fel: {arg} är inte en siffra.")
            return
        match self.kontext:
            case Kontext.RECEPTREDIGERARE | Kontext.INGREDIENSREDIGERARE:
                self.redigerare.redigera_ruta(index)
                self.precmd()
            case Kontext.RECEPTLISTA:
                self.visa_id = index
                self.byt_kontext(Kontext.RECEPTVY, True)
                self.do_mod(arg)
            case Kontext.INGREDIENSLISTA:
                self.visa_id = index
                self.byt_kontext(Kontext.INGREDIENSVY, True)
                self.do_mod(arg)

    def andra_objekt(self, arg):
        match self.kontext:
            case Kontext.RECEPTVY:
                r = self.recept[self.visa_id]
                self.redigerare = Redigerare(
                        r, [
                        StrRuta("RUBRIK", r.data, "rubrik"),
                        StrRuta("BESKRIVNING", r.data, "beskrivning"),
                        ListRuta("INGREDIENSLISTA", r.data, "ingredienser", sample.Ingrediens.tolka, r.data.produktkatalog, produkt_ar_temporar, text_color(" (odefinierad)", bcolors.RED)),
                        StrRuta("INSTRUKTIONER", r.data, "instruktioner_steg"),
                        IntRuta("PORTIONER", r.data, "portioner"),
                        StrRuta("UGNSTEMPERATUR", r.data, "ugnstemperatur")
                        ])
                self.byt_kontext(Kontext.RECEPTREDIGERARE)
            case Kontext.INGREDIENSVY:
                i = self.produktkatalog.data.produkter[self.visa_id]
                i._temp = False
                self.redigerare = Redigerare(
                        self.produktkatalog, [
                        StrRuta("NAMN", i, "namn"),
                        ListRuta("MÄTVÄRDEN", i, "_matvarden", sample.enheter.Tal.tolka)
                        ])
                self.byt_kontext(Kontext.INGREDIENSREDIGERARE)


    def do_upp(self, arg):
        self.byt_kontext(self.kontext.get("upp", Kontext.HUVUDMENY))

    def do_meny(self, arg):
        self.byt_kontext(Kontext.HUVUDMENY)

    def do_rec(self, arg):
        self.byt_kontext(Kontext.RECEPTLISTA)

    def do_ingr(self, arg):
        self.byt_kontext(Kontext.INGREDIENSLISTA)

    def do_pris(self, arg):
        match self.kontext:
            case Kontext.RECEPTVY:
                aktuellt_recept = self.recept[self.visa_id]
                print(aktuellt_recept.data.totalkostnad(True))
                print(f"")

    def do_mod(self, arg):
        match self.kontext:
            case Kontext.RECEPTVY | Kontext.INGREDIENSVY:
                self.andra_objekt(arg)
            case Kontext.RECEPTREDIGERARE | Kontext.RECEPTLISTA | Kontext.INGREDIENSREDIGERARE | Kontext.INGREDIENSLISTA:
                self.andra_falt(arg)

    def do_visa(self, arg):
        if kmd.VISA in self.kontext["komm"]:
            try:
                index = int(arg)
            except ValueError:
                print(f"Fel: {arg} är inte en siffra.")
                return
            self.visa_id = index
            self.byt_kontext(self.kontext["ned"])

    def do_skapa(self, arg):
        match self.kontext:
            case Kontext.RECEPTLISTA:
                if recept_file_exists(arg):
                    print(f"Fel: {arg}.json finns redan.")
                    return
                ny_receptfil = create_recept_file(arg)
                ny_receptfil.data = sample.Recept([], self.produktkatalog.data)
                self.recept.append(ny_receptfil)
                self.visa_id = len(self.recept) - 1
                self.byt_kontext(Kontext.RECEPTVY)
                self.do_mod(arg)
            case Kontext.INGREDIENSLISTA:
                if any([i.namn == arg for i in self.produktkatalog.data.produkter]):
                    for i, produkt in enumerate(self.produktkatalog.data.produkter):
                        if produkt.namn == arg:
                            self.visa_id = i
                            break
                else:
                    self.produktkatalog.data.produkter.append(sample.Produkt(arg, []))
                    self.visa_id = len(self.produktkatalog.data.produkter) - 1
                self.byt_kontext(Kontext.INGREDIENSVY)
                self.do_mod(arg)

    def do_avsluta(self, arg):
        "Avsluta Receptkalkylatorn: Q eller AVSLUTA"
        print("Avslutar Receptkalkylatorn.\n")
        pretty_print_files()
        return True

    do_q = do_avsluta


if __name__=="__main__":
    try:
        global_editor = os.environ["EDITOR"]
    except KeyError:
        global_editor = "nano"
    ReceptShell().cmdloop()
