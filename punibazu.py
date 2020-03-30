from TaskRestAPI.models import *
from django.utils.timezone import timezone
from string import ascii_lowercase as lista
import random
from django.utils import timezone


# korisnici

def randomm(podatak=''):
    if(podatak=='ulica'):
        ulica = ""
        reci = random.randint(1,2)
        brojUlice = random.randint(1,150)
        duzina = random.randint(10,17)
        if(reci>1):
            recDuzina = int(duzina/2)

            # ulica = str(lista[random.randint(1,25)]).upper()
            for i in range(recDuzina):
                if(len(ulica)==0):
                    ulica = str(lista[random.randint(1, 25)]).upper()
                else:
                    ulica += str(lista[random.randint(1, 25)])
            ulica += " "
            for i in range(recDuzina):
                if(ulica[-1] == " "):
                    if(random.randint(1,2)==1):
                        ulica = str(lista[random.randint(1, 25)]).upper()
                    else:
                        ulica += str(lista[random.randint(1, 25)])
                else:
                    ulica += str(lista[random.randint(1, 25)])
            ulica += " "+str(brojUlice)
            return ulica

        elif(reci==1):
            for i in range(duzina):
                if(len(ulica)==0):
                    ulica = str(lista[random.randint(1, 25)]).upper()
                else:
                    ulica += str(lista[random.randint(1, 25)])
            ulica += " " + str(brojUlice)
            return ulica
    elif(podatak=='brojPoste'):
        brojPoste = random.randint(1000,5000)
        return brojPoste
    elif (podatak == 'grad'):
        grad = ""
        duzina = random.randint(10, 17)
        for i in range(duzina):
            if (len(grad) == 0):
                grad = str(lista[random.randint(1, 25)]).upper()
            else:
                grad += str(lista[random.randint(1, 25)])
        return grad
    elif (podatak == 'telefon'):
        telefon = ""
        prefiksi = ["060","061","062","063","064","065","066","068","069"]
        telefon += random.choice(prefiksi)+"-"
        for i in range(2):
            for i2 in range(3):
                telefon+=str(random.randint(1,9))
            if(i!=1):
                telefon+="-"
        return telefon


def kreirajKorisnike():
    zaDodati = 101
    redosled = "korisnik"
    while(True):
        for i in range(1,zaDodati):
            username = redosled + str(i)
            email = redosled + str(i) + '@mejl.com'
            first_name = redosled.capitalize() + str(i)
            last_name = redosled.capitalize()+"ovic" + str(i)

            ulicaIBroj = randomm('ulica')
            brojPoste = randomm('brojPoste')
            grad = randomm('grad')
            telefon = randomm('telefon')
            if(redosled=="korisnik"):
                is_korisnik = True
                korisnik = Korisnici(username=username,email=email,first_name=first_name,
                                    last_name=last_name,ulicaIBroj=ulicaIBroj,brojPoste=brojPoste,
                                    grad=grad,telefon=telefon,is_korisnik=is_korisnik,password="ABC123")
                korisnik.save()
            else:
                is_autor = True
                korisnik = Korisnici(username=username, email=email, first_name=first_name,
                                    last_name=last_name, ulicaIBroj=ulicaIBroj, brojPoste=brojPoste,
                                    grad=grad, telefon=telefon, is_autor=is_autor,password="ABC123")
                korisnik.save()
        if(redosled=="korisnik"):
            zaDodati-=100-36
            redosled="autor"
        elif(redosled=="autor"):
            break

#izdavaci
def kreirajIzdavace():
    for i in range(6):
        ime = 6*str(lista[i]).upper()
        racun = ""
        email=""
        while(True):
            if(len(racun)==3 or len(racun)==9):
                racun+="-"
                continue
            elif(len(racun)==12):
                break
            racun+=str(random.randint(1,9))
        if(i%2==0):
            email = 6*str(lista[i])+"@mejl.com"
        izdavac = Izdavaci(ime=ime,racun=racun,email=email)
        izdavac.save()

def randrange_float(start, stop, step):
    return random.randint(0, int((stop - start) / step)) * step + start

# knjige

def kreirajKnjige():
    for i in range(150):
        isbn = ""
        strana = random.randint(50,370)
        cena = randrange_float(450.00,6500.00,0.50)
        godina = random.randint(1870,2020)
        izdavac = random.randint(1,6)
        autor = random.randint(0,35)
        while (True):
            if (len(isbn) == 3 or len(isbn) == 6) or len(isbn) == 11:
                isbn += "-"
                continue
            elif (len(isbn) == 15):
                break
            isbn += str(random.randint(1, 9))
        knjiga = Knjige(naslov="Prelepi trenutci "+str(godina),strana=strana,cena=(cena),godinaIzdanja=godina,ISBN=isbn)
        knjiga.izdavac = Izdavaci.objects.get(id=izdavac)
        knjiga.autor = Korisnici.objects.filter(is_autor=True)[autor]
        knjiga.save()
# narudzbine
def kreirajNarudzbine():
    for i in range(35):
        narudzbina = Narudzbine()
        narudzbina.datumNarucivanja = timezone.now()
        narudzbina.placeno = False
        narudzbina.korisnik = Korisnici.objects.filter(is_korisnik=True)[random.randint(0,75)]
        narudzbina.save()

# stavke narudzbine
def kreirajNarudzbine():
    for i in range(75):
        knjiga = random.randint(1,140)
        narudzbina = random.randint(1,36)
        querry = StavkeNarudzbine.objects.filter(knjiga=knjiga, narudzbina=narudzbina)
        if(querry.count()==0):
            stavkeNarudzbine= StavkeNarudzbine()
            stavkeNarudzbine.kolicina = random.randint(1,3)
            stavkeNarudzbine.knjiga = Knjige.objects.get(id=knjiga)
            stavkeNarudzbine.narudzbina = Narudzbine.objects.get(id=narudzbina)
            stavkeNarudzbine.save()
# placanje knjiga
def placanjeKnjiga1():
    for i in range(1,Narudzbine.objects.count()+1):
        daNe = [True,False]
        narudzbina = Narudzbine.objects.get(id=i)
        narudzbina.placeno = random.choice(daNe)
        narudzbina.save()
# komentarisanje knjiga
def kreirajKomentareNaKnjigama():
    knk = KomentariNaKnjigama()
    knk.komentar = "vrh je knjiga!!!"
    knk.korisnik = Korisnici.objects.filter(is_korisnik=True)[5]
    knk.knjiga = Knjige.objects.get(id=10)
    knk.save()
def kreirajOceneNaKnjigama():
    korisnik = Korisnici.objects.get(id=4)
    knjiga = Knjige.objects.get(id=124)
    narudzbina = Narudzbine.objects.filter(korisnik = korisnik.id,placeno = True)[0]
    stavka = StavkeNarudzbine.objects.filter(narudzbina = narudzbina.id,knjiga = knjiga)
    onk = OceneKnjiga(korisnik=korisnik,ocena=5)

print('ocenjene.')