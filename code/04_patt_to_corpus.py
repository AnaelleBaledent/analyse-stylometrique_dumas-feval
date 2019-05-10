import sys
import json

print("Prend en entrée deux arguments: une liste de patterns et un fichier de retour au texte (JSON)")
print("Exemple : python patt_to_corpus.py res_minsupp\=200 retour_au_texte_min\=4_max\=5.json")
print("pour obtenir les fichiers de retour au texte, relancer extract_patterns")
patt_file = sys.argv[1]
path_retour = sys.argv[2]
path_resultats = path_retour+".retour_au_texte.json"

f = open(patt_file)
lignes = f.readlines()
f.close()

dic_files = {}
f = open(path_retour)
retour_au_texte = json.load(f)
f.close()

dic_resultats = {}

for l in lignes:
  liste = eval(l)
  patt = liste[0]
  #print("="*10)
  #print(patt)
  #print("="*10)
  dic_pattern = {}
  for texte_name, liste_indices in retour_au_texte[patt].items():
    if texte_name not in dic_files:
      f = open(texte_name)
      dic = json.load(f)
      f.close()
      dic_files[texte_name] = dic
    #print(texte_name)
    liste_out = []
    for id_phrase, debut, fin in liste_indices:
      phrase = dic_files[texte_name][id_phrase]
      segment = phrase[debut:fin]
      #sequence_txt = "  "+" ".join([mot for mot, etiq in segment])+" (id_phrase = %s)"%str(id_phrase)
      sequence_txt = " ".join([mot for mot, etiq in segment])+" (id_phrase = %s)"%str(id_phrase)
      #liste_out.append("  "+" ".join([mot for mot, etiq in segment])+" (id_phrase = %s)"%str(id_phrase))
      liste_out.append(sequence_txt)
    #dic_texte[texte_name] = set(sorted(liste_out))
    #dic_pattern[texte_name] = list(set(sorted(liste_out)))
    #dic_pattern[texte_name] = list((liste_out))
    dic_pattern[texte_name] = []
    for elt in liste_out :
      if elt not in dic_pattern[texte_name] :
        dic_pattern[texte_name].append(elt)
    #dic_texte = {}
    #print("\n".join(set(sorted(liste_out))))
    #print("-"*10)
  dic_resultats[patt] = dic_pattern

f = open(path_resultats, 'w')
f.write(json.dumps(dic_resultats, indent = 2))
f.close()