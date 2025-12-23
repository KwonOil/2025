import numpy as np
import pandas as pd
from tensorflow import keras
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import joblib

df = pd.read_csv('python2/39. 0911/ms001.csv', encoding='euc-kr')

df2 = df.copy()
scaler = joblib.load('python2/39. 0911/minmax_scaler.pkl')

df2[['키','몸무게']] = scaler.fit_transform(df2[['키','몸무게']])
df2['성별'] = df2['성별'].map({'남':0,'여':1})
df2[['키','몸무게','성별']]

df2['학교'] = np.where(df2['학교명'].str.endswith('초등학교'),0, np.where(df2['학교명'].str.endswith('중학교'),1,2))

y = df2['학교']
X = df2[['키','몸무게','성별']]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)

# 모델 불러오기
model = joblib.load('python2/39. 0911/model.pkl')

print(model.summary())

pred = model.predict(X_test)
print("===== 예측결과 =====")
print(pred)
print(pred.shape)
print(y_test)
print(y_test.shape)

history = joblib.load('python2/39. 0911/history.pkl')
train_history = history.history["loss"]
validation_history = history.history["val_loss"]
fig = plt.figure(figsize=(8, 8))
plt.title("Loss History")
plt.xlabel("EPOCH")
plt.ylabel("LOSS Function")
plt.plot(train_history, "red")
plt.plot(validation_history, 'blue')
plt.show()
fig.savefig("train_history.png")

train_history = history.history["accuracy"]
validation_history = history.history["val_accuracy"]
fig = plt.figure(figsize=(8, 8))
plt.title("Accuracy History")
plt.xlabel("EPOCH")
plt.ylabel("Accuracy")
plt.plot(train_history, "red")
plt.plot(validation_history, 'blue')
plt.show()
fig.savefig("accuracy_history.png")

school_types = {0: "초", 1: "중", 2: "고"}
# np.argmax : 각 샘플에 대해 가장 높은 확률을 가진 클래스의 인덱스 반환
predicted_classes = np.argmax(pred, axis=1)
predicted_school_types = [school_types[i] for i in predicted_classes]
print(predicted_school_types)