import sys
import json

print("Prend en entrée un argument : un fichier de retour au texte (JSON)")
print("Exemple : python 04_get_examples.py retour_au_texte_min\=4_max\=5.json.resultat.json")
path_file = sys.argv[1]

f = open(path_file)
retour_au_texte = json.load(f)
f.close()

liste_sequences = retour_au_texte.keys()

query = "a"
while query != "":
  print("Veuillez entrer une séquence (sous la forme 'tag_tag_tag_tag') : ")
  query = input()
  if query in liste_sequences :
    print(json.dumps(retour_au_texte[query], indent = 2))