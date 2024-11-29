Sovellus ei ole vielä testattavissa fly.iossa. Kutakuinkin samat ohjeet sovelluksen käynnistämiseen, kuin kurssimateriaalissa. Kloonaa siis repositorio, johon luot .env tiedoston johon kirjoitat sisällöksi:
DATABASE_URL=(tietokannan-paikallinen-osoite)
SECRET_KEY=(salainen-avain)
Seuraavaksi aktivoi virtuaaliympäristö ja asenna sovelluksen riippuvuudet seuraavilla komennoilla:
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r ./requirements.txt
Luo app.py python tiedosto johon kopioit repositoriosta app.py tiedoston sisällön
Sitten määrittele tietokannan rakenne komennolla:
$ psql < schema.sql
ja sovellus käynnistetään komennolla flask run


Kaikki joiden edessä on # ei ole vielä toimivia 
Luon ravintolasovelluksen, jossa näkyy lista ravintoloista. Ravintoloista voi nähdä tietoa ja lukea arvioita. Jokainen käyttäjä on joko peruskäyttäjä tai ylläpitäjä.
- Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
- Käyttäjä näkee listan ravintoloista ja voi painaa ravintolasta, jolloin siitä näytetään lisää tietoa (kuten kuvaus, arviot ja aukioloajat).
- Käyttäjä voi antaa arvioita tähdillä ja kommenteilla ravintoloista ja lukea muiden antamia arvioita.
- Ylläpitäjä voi lisätä ja poistaa ravintoloita sekä määrittää ravintolasta näytettävät tiedot.
- Käyttäjä voi etsiä kaikki ravintolat, joiden kuvauksessa on annettu sana.
- Käyttäjä näkee myös listan, jossa ravintolat on järjestetty parhaimmasta huonoimpaan arvioiden (tähdet) mukaisesti.
- Ylläpitäjä voi tarvittaessa poistaa käyttäjän antaman arvion.
- #Ylläpitäjä voi luoda ryhmiä, joihin ravintoloita voi luokitella. Ravintola voi kuulua yhteen tai useampaan ryhmään.
