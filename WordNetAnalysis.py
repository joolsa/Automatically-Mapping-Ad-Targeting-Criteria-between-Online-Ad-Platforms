from sematch.semantic.similarity import WordNetSimilarity
import re
import pandas as pd
import codecs
import csv
from nltk.stem import WordNetLemmatizer

wordnet_lemmatizer = WordNetLemmatizer()

csvFile = codecs.open('S:/path/Stopwords.csv', 'rU', 'cp1251')
df = pd.read_csv(csvFile, sep=';',header=None)
stop = df[0].tolist()
stop = "\\b|\\b".join(stop)
# You can use these lists of categories for testing model parameters
categoryList1 = ["Digital Activities / Canvas Gaming / Plays 5 out of 7 days","Mobile Device User / LG / LG V10"]
categoryList2 = ["Apparel & Accessories","Consumer Electronics/Mobile Phones", "Consumer Electronics/Game Consoles"]
# OR
# full data for real calculations (beware that it's rather slow process):
# csvFile = codecs.open('S:/path/Behaviors.csv','rU','cp1251')
# df1 = pd.read_csv(csvFile, sep=';',header=0)
# df1 = df1.fillna('')
# categoryList1 = df1['Facebook'].tolist()
# csvFile = codecs.open('S:/path/In-market audiences.csv','rU','cp1251')
# df2 = pd.read_csv(csvFile, sep=';',header=0)
# df2 = df2.fillna('')
# categoryList2 = df2['Google'].tolist()

def cleanTexts(texts):
    clean=[]
    for t in texts:
        t = str(t)
        t=t.lower()
        t = re.sub(" ?(f|ht)(tp)(s?)(://)(.*)[.|/](.*)", ' ', t)
        t = re.sub("@\w+ ?", ' ', t)
        t = re.sub("[^\w\s]|[\d]", ' ', t)
        t = re.sub(stop, ' ', t)
        t = re.sub("\s+", ' ', t)
        t = t.split()
        t = [w for w in t if w.isalpha()]
        t = [wordnet_lemmatizer.lemmatize(w) for w in t]
        clean.append(t)
    return clean
cleanCleanCat1=cleanTexts(categoryList1)
cleanCleanCat2=cleanTexts(categoryList2)

wns = WordNetSimilarity()
similarCategories=[]
for cat in cleanCleanCat1:
    sims=[]
    for t in cleanCleanCat2:
        TextSim=[]
        for w in cat:
            # wdsSim=[1 if w == wr else wns.word_similarity(w, wr, 'li') for wr in t]
            wdsSim = [wns.word_similarity(w, wr, 'li') for wr in t]
            TextSim.extend(wdsSim)
        sims.append((cleanCleanCat2.index(t),sum(TextSim)))
    if max(sims,key=lambda x:x[1])[1]>0:
        similarCategories.append((max(sims,key=lambda x:x[1])[0],max(sims,key=lambda x:x[1])[1]))
    else:
        similarCategories.append('')
    print('{0} texts out of {1} done'.format(cleanCleanCat1.index(cat)+1, len(cleanCleanCat1)))

with open('S:/path/In-market audiences_sim.csv', 'w', newline='',
          encoding='utf-8') as csvfile:
    wr = csv.writer(csvfile, delimiter=';',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for row in similarCategories:
        wr.writerow(row)