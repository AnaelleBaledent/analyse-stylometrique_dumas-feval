import sys
import json
import re
import numpy

def moyenne(liste):
  somme = 0
  for l in liste:
    somme+=l
  return somme/len(liste)

def somme(liste):
  somme = 0
  for l in liste:
    somme+=l
  return somme

if len(sys.argv)!=2:
  print("USAGE:\n arg1 = json_file_with_patterns.json")
  exit()
min_supp = 200
min_len = 1

f = open(sys.argv[1])
dic_patt = json.load(f)
f.close()

liste_patt = dic_patt["all_patt"]

#recuperer les moyennes pour chaque pattern
dic_vec = {}
for filename, patt_vector in dic_patt["all_files"].items():
  directory, auteur, fichier = re.split("/", filename)
#  dic_vec.setdefault(auteur, [[]]*len(patt_vector))
  dic_vec.setdefault(auteur, [])
  #pour chaque auteur eon fait la moyenne de chaque dimension du vecteur
  for dim, valeur in enumerate(patt_vector):
    if len(dic_vec[auteur])==dim:
       dic_vec[auteur].append([])
    #dic_vec[auteur][dim].append(valeur)
    dic_vec[auteur][dim].append(valeur)

ans = []
dic_moy = {}
for auteur, vecteur in dic_vec.items():
  dic_moy.setdefault(auteur, [])
  for dim, liste_valeurs in enumerate(vecteur):
    dic_moy[auteur].append(somme(liste_valeurs))
#    1/0
liste_GR = []
#Calculer GR pour chaque dimension

vec_dumas = dic_moy["Dumas"]
vec_feval = dic_moy["Feval"]
L = []
for i, val in enumerate(vec_dumas):
  if val+vec_feval[i]<=min_supp:
    continue
  if val==0:
    GR= "00++Feval"
  elif vec_feval[i]==0:
    GR= "99++Dumas"
  else:
    GR = str(round(val/vec_feval[i], 4))
  L.append([GR, liste_patt[i], val, vec_feval[i]])

L_s = [[patt,GR, dumas, feval] for GR, patt, dumas, feval in sorted(L)]

L_eff = sorted([[dumas+feval, GR, patt] for GR,patt,dumas,feval in L], reverse=True)

for toto in L_s:
  print(toto)

for eff, GR, patt in L_eff[:10]:
  print("%s\t &%s\t &%s"%(str(eff),str(GR), patt))
