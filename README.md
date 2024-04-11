<img src="docs/logo.svg">

Une application d'étude de la mobilité en Wallonie et à Bruxelles

→ https://g25.linfo1002.ovh/


## Données
CityPace utilise les données des capteurs [Telraam](https://telraam.net/en/what-is-telraam). Telraam utilise une caméra collée à une fenêtre qui donne sur la rue et un algorithme de vision par ordinateur pour compter le nombre de voitures, piétons, cyclistes et poids lourds. Toutes les heures, le capteur renvoie le nombre d'objets détectés et leurs vitesses agrégées à Telraam.net.

## Équipe
- [Enzo Andrade Orletti](https://g25.linfo1002.ovh/enzo)
- [Tom Deglume](https://g25.linfo1002.ovh/tom)
- [Nicolas Mertens](https://g25.linfo1002.ovh/nicolas)
- [Johannes Radesey](https://g25.linfo1002.ovh/johannes)
- [Liam Vander Becken](https://g25.linfo1002.ovh/liam)

## Création de l'environnement
```
    python3 -m venv .venv
    source .venv/bin/activate
    pip3 install -r requirements.txt
```

## Lancement
```
    flask --app=mobility --debug run
```
## tests
```
    coverage run -m unittest
    coverage html
```

