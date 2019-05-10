#IMPORTS
from nltk.tag import StanfordPOSTagger 
import os
import re
import sys, json

#FONCTIONS
def getTags (texte) :
	txtToken = nltk.word_tokenize(texte)
	txtTag = nltk.pos_tag(txtToken)
	return txtTag

def getTagsSimplified (texteTag) :
	txtTagSimplif = [(word, nltk.map_tag('en-ptb', 'universal', tag)) for word, tag in texteTag]
	return txtTagSimplif

def getListPOS(texteTag) :
	listePOS = []
	for i, j in texteTag :
		listePOS.append(j)
	return listePOS
## settings.json doit contenir :
# base 	: le répertoire du stanford tagger
# jarname: le nom du fichier jar 
# on peut s'inspirer de settings.json.example

f = open("settings.json")
settings = json.load(f)
f.close()

base = settings["base"]
jar = base+ settings["jarname"]

##Modèle à utiliser (pour quelle langue)
model = base+'models/french.tagger'
model = base+'models/english-bidirectional-distsim.tagger'

#CODE
##Appel du StanfordPOSTagger
pos_tagger = StanfordPOSTagger(model, jar, encoding='utf8' )


#phrase = "Rencontre avec Dodo La Saumure : \u00ab Je ne connais pas #DSK, mais j'aurais aim\u00e9 le rencontrer \u00bb http://bit.ly/xsc2yb #carlton"
#import time
import json

for fic in sys.argv[1:]:
  print(fic)
  f = open(fic)
  lignes = f.readlines()
  f.close()
  tagged = "%s.StanfordTagged.json"%fic
  if os.path.exists(tagged):
    print("  -> %s already DONE"%tagged)
    continue
  nbLines = str(len(lignes))
  print("  %s lignes"%nbLines)
  liste_phrases = []
  cut = 0.1
  for cpt, phrase in enumerate(lignes):
    if len(phrase)<2:continue
    res = pos_tagger.tag(phrase.split())
    res = [list(elmt) for elmt in res] #Liste de listes
    liste_phrases.append(res)
    if cpt>int(nbLines)*cut:
      print ("-")
      cut+=0.1
  w = open(tagged, "w")
  w.write(json.dumps(liste_phrases, indent=2))
  w.close()
  print("Output written: %s"%tagged)
  liste_infos = ["lemmes", "tags"]
  for cpt, nom in enumerate(liste_infos):
    phrases = []
    for phr in liste_phrases:
      out = " ".join([x[cpt] for x in phr])
      phrases.append(out)
    out_name = "%s.StanfordTagged_%s.txt"%(fic, nom)
    w = open(out_name, "w")
    w.write("\n".join(phrases)+"\n")
    w.close()
