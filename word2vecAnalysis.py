from gensim.models import word2vec
import logging
import os
import re
import pandas as pd
import xlsxwriter

# Define the function that will cleanup the categories' names:
# delete non-alphabetic symbols and make them lower-case
def cleant(t):
    t = re.sub("[^\w\s]", ' ', t)
    t = t.lower()
    return t
# Train the classification model on the Wikipedia text corpus.
# DO NOT retrain the model unless you absolutely need it.
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
sentences = word2vec.Text8Corpus('text8')
model = word2vec.Word2Vec(sentences, size=200)
#Save the model, to avoid re-training.
model.save('text8.model')

#Load trained model. I recommend starting the analysis from here:
model = word2vec.Word2Vec.load('text8.model')

# Load the categories names from the relevant files.
datadir="C:\\Full path to the directory where you store these files\\"
df=pd.read_excel(os.path.join(datadir,"Affinity categories.xlsx"),header=None)
afcat = df[0].tolist()
df=pd.read_excel(os.path.join(datadir,"Interests.xlsx"),header=None)
interests = df[0].tolist()
df=pd.read_excel(os.path.join(datadir,"In-market audiences.xlsx"),header=None)
inaud = df[0].tolist()
df=pd.read_excel(os.path.join(datadir,"Behaviors.xlsx"),header=None)
behaviors = df[0].tolist()

# Calculate the affinity of "Affinity categories" with "Interests".
afcatVSsinterests=[]
for cat in afcat:
    clcat=cleant(cat)
    # For the "affinity category" under consideration create a set of words
    # which are also present in the Wikipedia dataset model.
    s1 = set(clcat.split()).intersection(model.wv.vocab)
    ints=[]
    # Do the same for "Interests".
    # In case not any word from an "interest" is present in the model vocabulary,
    # just add an empty set.
    for i in interests:
        try:
            ints.append((i,set(cleant(i).split()).intersection(model.wv.vocab)))
        except:
            ints.append((i,set()))
    # Create a list of word2vec semantic similarites between
    # the "affinity category" under consideration and each "interest".
    sims=[]
    for s in ints:
        try:
            sims.append(model.n_similarity(s1, s[1]))
        except:
            sims.append(0)
    # Find which "affinity category"+"interest" pair has
    # the highest similarity.
    maxsim=max(sims)
    # Append to the "Affinity categories" with "Interests" list
    # a tuple of the "affinity category" under consideration, original
    # "interest" name which has a maximum value of similarity with the
    # "affinity category", and the value of similarity.
    afcatVSsinterests.append((cat,ints[sims.index(maxsim)][0],maxsim))

# Save the results to the Excel file of proper name.
workbook = xlsxwriter.Workbook(os.path.join(datadir,"In-market audiences VS Behaviors.xlsx"))
worksheet = workbook.add_worksheet()
for row, line in enumerate(afcatVSsinterests):
    for col, cell in enumerate(line):
        worksheet.write(row, col, cell)
workbook.close()

# Calculate the affinity of "Interests" with "Affinity categories".
# Logic is the same as the first affinity calculation (see above).
interestsVSafcat=[]
for i in interests:
    cli=cleant(i)
    s1 = set(cli.split()).intersection(model.wv.vocab)
    afcats=[]
    for a in afcat:
        try:
            afcats.append((a,set(cleant(a).split()).intersection(model.wv.vocab)))
        except:
            afcats.append((a,set()))
    sims=[]
    for s in afcats:
        try:
            sims.append(model.n_similarity(s1, s[1]))
        except:
            sims.append(0)
    maxsim=max(sims)
    interestsVSafcat.append((i,afcats[sims.index(maxsim)][0],maxsim))

workbook = xlsxwriter.Workbook(os.path.join(datadir,"Interests VS Affinity categories.xlsx"))
worksheet = workbook.add_worksheet()
for row, line in enumerate(interestsVSafcat):
    for col, cell in enumerate(line):
        worksheet.write(row, col, cell)
workbook.close()

# Calculate the affinity of "In-market audiences" with "Behaviors".
# Logic is the same as the first affinity calculation (see above).
inaudVSbehaviors=[]
for aud in inaud:
    claud=cleant(aud)
    s1 = set(claud.split()).intersection(model.wv.vocab)
    behs=[]
    for b in behaviors:
        try:
            behs.append((b,set(cleant(b).split()).intersection(model.wv.vocab)))
        except:
            behs.append((b,set()))
    sims=[]
    for s in behs:
        try:
            sims.append(model.n_similarity(s1, s[1]))
        except:
            sims.append(0)
    maxsim=max(sims)
    inaudVSbehaviors.append((aud,behs[sims.index(maxsim)][0],maxsim))

workbook = xlsxwriter.Workbook(os.path.join(datadir,"In-market audiences VS Behaviors.xlsx"))
worksheet = workbook.add_worksheet()
for row, line in enumerate(inaudVSbehaviors):
    for col, cell in enumerate(line):
        worksheet.write(row, col, cell)
workbook.close()

# Calculate the affinity of "Behaviors" with "In-market audiences".
# Logic is the same as the first affinity calculation (see above).
behaviorsVSinaud=[]
for b in behaviors:
    clb=cleant(b)
    s1 = set(clb.split()).intersection(model.wv.vocab)
    auds=[]
    for a in inaud:
        try:
            auds.append((a,set(cleant(a).split()).intersection(model.wv.vocab)))
        except:
            auds.append((a,set()))
    sims=[]
    for s in auds:
        try:
            sims.append(model.n_similarity(s1, s[1]))
        except:
            sims.append(0)
    maxsim=max(sims)
    behaviorsVSinaud.append((b,auds[sims.index(maxsim)][0],maxsim))

workbook = xlsxwriter.Workbook(os.path.join(datadir,"Behaviors VS In-market audiences.xlsx"))
worksheet = workbook.add_worksheet()
for row, line in enumerate(behaviorsVSinaud):
    for col, cell in enumerate(line):
        worksheet.write(row, col, cell)
workbook.close()