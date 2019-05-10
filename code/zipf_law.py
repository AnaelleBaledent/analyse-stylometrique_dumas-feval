import json
import sys
from operator import itemgetter
import matplotlib.pyplot as plt
import math
import re

#Ouverture du fichier passé en paramètre (liste des séquences par )
fic = sys.argv[1]

f = open(fic)
dic = json.load(f)
f.close()

nom_abrege = re.sub(r".*(min\=\d_max\=\d).*", r"\1", fic)

#Récupération des sous-dictionnaires
liste_sequences = dic["all_patt"]
liste_textes = dic["all_files"]

dic_effectif_sequences = {}

for index, sequence in enumerate(liste_sequences) :
	dic_effectif_sequences[sequence] = 0
	for texte, vecteur in liste_textes.items() :
		dic_effectif_sequences[sequence] = dic_effectif_sequences[sequence] + vecteur[index]

dic_effectif_sequences = reversed(sorted(dic_effectif_sequences.items(), key = itemgetter(1)))

dic_effectif_sequences = dict((x, y) for x, y in dic_effectif_sequences)

#Écriture du résultat dans le fichier
w = open("%s_zipf_law.json"%fic, "w")
w.write(json.dumps(dic_effectif_sequences, indent=2))
w.close()

#Récupération des effectifs (values) pour chaque séquences (key)
effectifs = [t[1] for t in dic_effectif_sequences.items()]

ranks = range(len(effectifs))

#Création et affichage du graphique
plt.loglog(ranks,effectifs)
plt.xlabel('Rang de la séquence dans la table ordonnée des effectifs')
plt.ylabel('Effectifs (en log)')
plt.title('Distribution des séquences (%s) dans le corpus CDF'%nom_abrege)
plt.savefig("zipf_law/zipf_law_plot%s.png"%nom_abrege, bbox_inches='tight')
plt.savefig("zipf_law/zipf_law_plot%s.svg"%nom_abrege, bbox_inches='tight')
