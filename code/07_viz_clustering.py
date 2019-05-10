#création des matrices

#IMPORTS
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
#from matplotlib import pyplot as plt
import glob
import codecs
import sys
from numpy import ndarray
import array


fic = sys.argv[1]

f = open(fic)
dic = json.load(f)
f.close()
data = dic["all_files"]

patterns = dic["all_patt"]

liste_fichiers = list(data.keys()) #l'ordre est fixe | list() est obligatoire pour liste_fichiers[cpt]

matrix = []

for fichier in liste_fichiers :
    matrix.append(data[fichier])

#X = pd.DataFrame.from_dict(data, orient='index')

true_k = 5 #nombre de clusters

model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=10)
model.fit(matrix)

#print("Prediction")
print(fic)

dic_predict = {}
for cpt, ligne in enumerate(matrix):
  prediction = model.predict([ligne])
  #dic_predict.setdefault(prediction, [])
  #dic_predict[prediction].append(liste_fichiers[cpt])
  dic_predict.setdefault(prediction.tobytes(), [])
  dic_predict[prediction.tobytes()].append(liste_fichiers[cpt])
  #print(liste_fichiers[cpt], " : ",prediction)
  print(prediction)

plt.scatter(X[:, 0], X[:, 1], c=y_kmeans, s=50, cmap='viridis')

centers = kmeans.cluster_centers_
plt.scatter(centers[:, 0], centers[:, 1], c='black', s=200, alpha=0.5);