import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, f1_score, recall_score

df = pd.read_csv('week8/day3-4/creditcard.csv')
print(df.shape)
df.head()

df.info()

df.describe()
class_names = {0:'Not Fraud', 1:'Fraud'}
print(df.Class.value_counts().rename(index = class_names))

from sklearn.model_selection import train_test_split

# Target and features for ULB/Kaggle dataset
y = df['Class']
X = df.drop(columns=['Class', 'Time'])  # drop 'Time' unless you explicitly model it

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y)

from sklearn.linear_model import LogisticRegression

model = LogisticRegression()

# we use .ravel() to transform the y_train data into a 1D array because LogisticRegression() expects the target variable (in this case, y_train) to be a 1D array rather than a column vector or a 2D array. 
model.fit(X_train, y_train.values.ravel())

pred = model.predict(X_test)

class_names = ['not_fraud', 'fraud']
matrix = confusion_matrix(y_test, pred)
# Create pandas dataframe
confusion_df = pd.DataFrame(matrix, index=class_names, columns=class_names)
print("Confusion Matrix:", confusion_df)

f1_score = round(f1_score(y_test, pred), 2)
recall_score = round(recall_score(y_test, pred), 2)
print("Sensitivity/Recall for Logistic Regression Model 1 : {recall_score}".format(recall_score = recall_score))
print("F1 Score for Logistic Regression Model 1 : {f1_score}".format(f1_score = f1_score))