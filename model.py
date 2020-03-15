import pandas as pd
import numpy as np
from sklearn.externals import joblib
from sklearn.metrics import classification_report,confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
df = pd.read_csv('data_without_shift_latest.csv',header=None)
X=df[df.columns[3:]].values
y=df[df.columns[0:1]].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)
rfc = RandomForestClassifier(n_estimators=100)
rfc.fit(X_train, y_train)
rfc_predict=rfc.predict(X_test)
# print(confusion_matrix(y_test,rfc_predict))
# print(classification_report(y_test,rfc_predict))
joblib.dump(rfc, 'model.pkl')