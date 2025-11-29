import os
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import joblib

MODEL_DIR = './models'
if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR, exist_ok=True)

# Generate or load demo data for diabetes
DIAB_CSV = './data/sample_diabetes.csv'
if not os.path.exists('./data'):
    os.makedirs('./data', exist_ok=True)

# If CSV not present, create a small synthetic dataset based on Pima-like features
if not os.path.exists(DIAB_CSV):
    import random
    rows = []
    for _ in range(500):
        age = random.randint(20,80)
        bmi = round(random.uniform(18,40),1)
        sugar = random.randint(70,220)
        bp = random.randint(80,160)
        # synthetic rule: higher sugar and bmi -> higher chance
        score = 0.01*age + 0.04*bmi + 0.02*(sugar-100) + 0.01*(bp-100)
        outcome = 1 if score + random.uniform(-1,1) > 2 else 0
        rows.append([age,bmi,sugar,bp,outcome])
    df = pd.DataFrame(rows, columns=['age','bmi','sugar','bp','outcome'])
    df.to_csv(DIAB_CSV, index=False)

# Train diabetes model
print('Training diabetes model...')
df = pd.read_csv(DIAB_CSV)
X = df[['age','bmi','sugar','bp']]
y = df['outcome']
clf = LogisticRegression(max_iter=1000).fit(X,y)
joblib.dump(clf, os.path.join(MODEL_DIR, 'diabetes_model.joblib'))
print('Saved diabetes_model.joblib')

# Create synthetic data for cardiac risk
CARD_CSV = './data/sample_cardiac.csv'
if not os.path.exists(CARD_CSV):
    import random
    rows = []
    for _ in range(500):
        age = random.randint(30,85)
        chol = random.randint(150,320)
        bp = random.randint(90,170)
        smoker = random.choice([0,1])
        score = 0.02*age + 0.01*(chol-170) + 0.01*(bp-110) + 0.8*smoker
        outcome = 1 if score + random.uniform(-1,1) > 3 else 0
        rows.append([age,chol,bp,smoker,outcome])
    df2 = pd.DataFrame(rows, columns=['age','chol','bp','smoker','outcome'])
    df2.to_csv(CARD_CSV, index=False)

print('Training cardiac model...')
df2 = pd.read_csv(CARD_CSV)
X2 = df2[['age','chol','bp','smoker']]
y2 = df2['outcome']
clf2 = LogisticRegression(max_iter=1000).fit(X2,y2)
joblib.dump(clf2, os.path.join(MODEL_DIR, 'cardiac_model.joblib'))
print('Saved cardiac_model.joblib')

print('Training complete. Models are in ./models')
