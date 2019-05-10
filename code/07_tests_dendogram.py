#création des matrices

#IMPORTS
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
from scipy.cluster.hierarchy import dendrogram, linkage  
from matplotlib import pyplot as plt
import glob
import codecs
import sys
from numpy import ndarray
import array
import re
#import scipy.cluster.hierarchy as shc


fic = sys.argv[1]

#Ouverture/récupération du fichier des patterns
#f = open("patterns/patt_dumas_feval_minlen=1_maxlen=1.json")
f = open(fic)
dic = json.load(f)
f.close()
data = dic["all_files"]

patterns = dic["all_patt"]

liste_fichiers = list(data.keys()) #l'ordre est fixe | list() est obligatoire pour liste_fichiers[cpt]

matrix = []

for fichier in liste_fichiers :
    matrix.append(data[fichier])

noms_abreges = [re.sub(r"corpus1\/(.*\/.*).txt.*", r"\1", nom) for nom in liste_fichiers]
labelList = noms_abreges

#OK
#plt.figure(figsize=(10, 7))  
#plt.title("Customer Dendograms")  
#dend = shc.dendrogram(shc.linkage(matrix, method='ward'))

liste_methodes = ['single', 'complete', 'average', 'weighted', 'centroid', 'median', 'ward']

for methode in liste_methodes :
    linked = linkage(matrix, methode)
    plt.figure(figsize=(10, 7))
    plt.title("Dendrogramme (méthode '%s', paramètres par défaut)"%methode)
    dendrogram(linked, orientation='top', labels=labelList, leaf_rotation = 90., distance_sort='descending', show_leaf_counts=True)
    plt.savefig("results/scipy_dendogram_cdf_%s_default.png"%methode, bbox_inches='tight')
