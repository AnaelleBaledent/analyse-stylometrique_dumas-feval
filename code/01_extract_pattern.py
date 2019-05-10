#IMPORTS
import json
import glob
import re, os

#len_min = 1
#len_max = 1

#FONCTIONS
def get_effectif(sequence_forme_tag, set_patt, mini, maxi, retour_au_texte, path):
  dic_patt = {}
  for cpt_phrase, phrase in enumerate(sequence_forme_tag):
    etiquettes = [x[1] for x in phrase]
    #On récupère les patrons de tailles 1 à 5
    for n in range(mini, maxi):
      for position in range(0, len(etiquettes)-n+1):#on part de la position 0 et on s'arrête au dernier token
        patt = etiquettes[position:position+n]
        str_patt = "_".join(patt)
        retour_au_texte.setdefault(str_patt, {})
        retour_au_texte[str_patt].setdefault(path, [])
        retour_au_texte[str_patt][path].append([cpt_phrase, position, position+n])
        set_patt.add(str_patt)
        #if str_patt not in dic:
        #  dic[str_patt]=0
        dic_patt.setdefault(str_patt, 0)#equivalent au if ci-dessus
        dic_patt[str_patt]+=1
  return dic_patt, set_patt, retour_au_texte


#On récupère sous forme de liste les chemins de tous les fichiers du dossier Dumas
force = True
minlength = 3
maxlength = 5
retour_au_texte = {}

for mini in range(minlength,maxlength):
  for maxi in range(mini,maxlength+1):
    #name = "patterns/patt_dumas_feval_min=%s_max=%s.json"%(str(mini), str(maxi))
    name = "patterns/patt_feval_chapters46_min=%s_max=%s.json"%(str(mini), str(maxi))
    if os.path.exists(name) and force ==False:
      print(" file exists : %s, ... passing"%name2)
      continue
    #liste_fic = glob.glob("corpus1/*/*")
    liste_fic = glob.glob("corpus2_tagged/Feval/le-bossu_chapter46.*")
    liste_patt_path = []
    set_patt = set()# ensemble = pas de doublons
    for path in liste_fic:
      f = open(path)
      liste_phr = json.load(f)
      f.close()
      dic_patt, set_patt, retour_au_texte = get_effectif(liste_phr, set_patt, mini, maxi+1, retour_au_texte, path)
      liste_patt_path.append(dic_patt)
      ll = [[len(re.split("_",p)), p] for p in set_patt]
    #Tri alpha des patterns pour avoir le même ordre pour construire la matrice
    #(un set ne peut pas être trié)
    all_patt = sorted(list(set_patt))
    
    #On crée un dictionnaire pour répertorier tous les patterns (all_patt) 
    #et lister les effectifs des patterns/fichier dans 'all_files'
    dic_out = {"all_patt":all_patt, "all_files":{}}
    
    for cpt, titi in enumerate(liste_patt_path):
      liste_eff = []
      for patt in all_patt:
        if patt not in titi:
          liste_eff.append(0)
        else:
          liste_eff.append(titi[patt])
    #liste_eff = [dic_patt[patt] for patt in all_patt] #equivalent au for ci-dessus
      dic_out["all_files"][liste_fic[cpt]] = liste_eff
    
    #On écrit dans un fichier les résultats, au format JSON
    w = open(name, "w")
    w.write(json.dumps(dic_out, indent = 2))
    w.close()
    print("Output : %s"%name)

if len(retour_au_texte)>0:
  name2 = "retour_au_texte_min=%s_max=%s.json"%(str(mini), str(maxi))
  w = open(name2, "w")
  w.write(json.dumps(retour_au_texte))
  w.close()

