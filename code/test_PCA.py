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
import tools

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

#X = pd.DataFrame.from_dict(data, orient='index')

true_k = 5 #nombre de clusters

model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=10)
model.fit(matrix)

#print("Prediction")
print(fic)

liste_predictions =[]
dic_predict = {}
for cpt, ligne in enumerate(matrix):
  prediction = model.predict([ligne])
  dic_predict.setdefault(prediction.tobytes(), [])
  dic_predict[prediction.tobytes()].append(liste_fichiers[cpt])
  print(prediction)
  liste_predictions.append(prediction[0])


from sklearn.decomposition import PCA
iris = {"data":matrix}

pca = PCA(n_components=3).fit(iris["data"])
pca_2d = pca.transform(iris["data"])

colors = ["r", "y", "b", "g", "m"]
liste_noms = [tools.format_name(x) for x in liste_fichiers]
import pylab as pl
for i in range(0, pca_2d.shape[0]):
  color = colors[liste_predictions[i]]
  x, y = pca_2d[i,0],pca_2d[i,1]
  pl.text(x, y, liste_noms[i][:12], fontsize=8)
  c1 = pl.scatter(x, y ,c=color, marker='+')

pl.xlim(-0.003, 0.006)
pl.ylim(-0.003, 0.004)
pl.title("ACP sur le CDF (min=4_min=5)")
pl.show()
