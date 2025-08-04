#importer le module python pour faire des requêtes

import requests
import json
from contextlib import closing
from urllib.request import urlopen
import dateutil.parser
from colorama import Fore,Style, init


##Rajout de cette ligne pour apporter changement dans le script pour test branche git


#à faire au début du script pour que tout fonctionne sur tous les systemes
init()

def texte_couleur(texte,couleur="BLEU"):
     couleurs = {
          "ROUGE": Fore.RED,
          "VERT": Fore.GREEN,
          "JAUNE": Fore.YELLOW,
          "BLEU": Fore.BLUE,
          "MAGENTA": Fore.MAGENTA,
          "CYAN": Fore.CYAN,
          "BLANC":Fore.WHITE
     }

print("Voici le message:",texte_couleur("Soleil","jaune"))


#définition d'une fonction pour 
#import de la clé API personnelle indiquée sur le site: 
#la clé API se situe sur un document format .txt dans le même reportoire que ce script
#récupérer avec with open le nom du fichier:api.txt
# with open dans un bloc try pour gérer les erreurs s'il y en a : fichier n'existe pas, pb de permission, erreur lecture
# "r" indique le mode lecture uniquement = lire ce qu'il contient
#as file = donne un nom temporaire (une variable temporaire) au fichier pour permettre d'appeler des métodes sur le fichier ouvert
# .read() lit tout le contenu du fichier en une fois et retourne le contenu sous forme de string 
#.strip() supprime les espaces, tabulations et retours à la ligne au début et à la fin d'une string
def lire_cle_api(fichier_cle="api.txt"):
    try:
        with open(fichier_cle,"r") as file:
                    api_key = file.read().strip()
                    return api_key
    except Exception as e:
        print(f"Il n'y a une erreur avec le fichier ou la clé API:", e)
        return None



def data_meteo_ville(ville):
    api_key = lire_cle_api()
    if not api_key:
        print("Impossible de récupérer la clé API, arrêt.")
        return

#choix de la ville par l'utilisateur, à développer
#ville = input("Entrez le nom de la ville: ")
#paramètre à connaitre :le code INSEE pour mmétéo par commune: lyon 69123 morance 69140 maringes 42138 à dev pour automatiser
    code_INSEE = 69123


#paramètre à déchiffrer: le temps = clé : forecast['weather'] valeur: un code de 0 à 200 qui permet de décrire le temps
#création d'un fichier JSON avec clé : le code 0 à 200 et valeur: la description du temps
#récupération du fichier code_temps_description.json = dictionnaire des codes : weather_codes
    with open("code_temps_description.json","r") as f:
        weather_codes = json.load(f)

#connexion à l'Api
#url de base :https://api.meteo-concept.com/api/
#prévision meteo journée, daily=0=jour en cours 1=demain, etc   :  forecast/daily/0
#decoded est la réponse en format JSON de l'API
    url = f"http://api.meteo-concept.com/api/forecast/daily/0?token={api_key}&insee={code_INSEE}"
    reponse = requests.get(url)
    decoded = reponse.json()

#les variables city et forecast sont des sous dictionnaires de "decoded"
    city = decoded['city']
    forecast = decoded['forecast']
#récupère le code [weather] de la réponse.json=decoded (pour faire correspondre la description) et le mettre en string car clés JSON st des strings
    code = str(forecast["weather"])
#faire correspondre le code de la réponse.json=decoded avec le dictionnaire des codes qui sera la valeur de la variable description
    description = weather_codes.get(code,"code non défini")

    print()
    print(u"Aujourd'hui à {}:\n".format(city['name'],forecast['weather']))
    print(f"Temps de la journée: {description}.")
    print(u"Température: minimale de {}°C et maximales de {}°C\n".format(forecast['tmin'],forecast['tmax']))
    print(u"Ensoleillement: {} heures dans la journée\n".format(forecast['sun_hours']))
    print(u"Pluie: Il y a {} '%' de probabilité qu'il pleuve,\non prévoit {} mm (pas plus de {} mm en tous cas) de précipitations.\n".format(forecast['probarain'], forecast['rr10'], forecast['rr1']))
    print(u"Probabilité de gel: {}'%'".format(forecast['probafrost']))
    print(u"Probabilité de brouillard: {}'%'".format(forecast['probafog']))
    print(u"Probabilité de vent au delà de 70km/heure: {}'%'".format(forecast['probawind70']))
    print()

data_meteo_ville("Morancé")

'''à mettre dans une fonction
url2=f"http://api.meteo-concept.com/api/ephemeride/0?token={api_key}&insee={code_INSEE}"
reponse = requests.get(url2)
cityEph = reponse.json()
print(u'Le soleil se lèvera à {} et se couchera à {}.'.format(cityEph['ephemeride']['sunrise'], cityEph['ephemeride']['sunset']))
#print(u'On comptera {} minutes de soleil de {} qu\'aujourd\'hui.'.format(abs(cityEph['ephemeride']['diff_duration_day']), 'moins' if cityEph['ephemeride']['diff_duration_day'] <= 0 else 'plus'))
print()
'''


#url prévision 12h https://api.meteo-concept.com/api/forecast/nextHours
#url3 = f"https://api.meteo-concept.com/api/forecast/nextHours/0?token={api_key}&insee={code_INSEE}"
'''url_period = f"http://api.meteo-concept.com/api/forecast/daily/periods?token={api_key}&insee={code_INSEE}"

reponse_periods = requests.get(url_period)

data_periods = reponse.json()
print("Element data_period")
print(data_periods)'''


'''a mettre dans une fonction

#with closing(urlopen('http://api.meteo-concept.com/api/forecast/daily?token={api_key}&insee={code_INSEE}')) as url_p:
url_previ = f"http://api.meteo-concept.com/api/forecast/daily?token={api_key}&insee={code_INSEE}"

reponse_prev = requests.get(url_previ)

prev = reponse_prev.json()

city1,forecast1 = prev['city'], prev['forecast']



for i, jour in enumerate(forecast1):
    date_obj = dateutil.parser.parse(jour['datetime'])
    date_formatee = date_obj.strftime('%A %d %B %Y')  # Date lisible
    
    code_prev = str(jour['weather'])
    description_prev = weather_codes.get(code_prev, "code non défini")
    
    tmin = jour['tmin']
    tmax = jour['tmax']

    print(f" A {city1['name']}, jour {i + 1} ({date_formatee}): {description_prev}, Températures: min {tmin}°C / max {tmax}°C ")

    '''

'''pour prévi sur 3 prochains jour à voir
jours = ["Aujourd'hui", "Demain", "Après-demain"]

for i in range(min(3, len(forecast1))):  # max 3 jours si dispo
    jour_label = jours[i] if i < len(jours) else f"Jour {i}"
    date_str = forecast1[i]['datetime']
    date = dateutil.parser.parse(date_str).strftime('%A %d %B %Y')  # Exemple : Samedi 25 Mai 2025
    tmin = forecast1[i]['tmin']
    tmax = forecast1[i]['tmax']

    print(f"{jour_label} ({date}) à {city1['name']} : {tmin}°C / {tmax}°C")
'''


#prévoir phase de la lune