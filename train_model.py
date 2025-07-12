import pandas as pd, os, pickle
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split

X, y = [], []
for file in os.listdir("data"):
    df = pd.read_csv(f"data/{file}", header=None)
    for row in df.values:
        if len(row) == 63:  # Only accept full rows
            X.append(row)
            y.append(file[:-4])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = KNeighborsClassifier(n_neighbors=5)
model.fit(X_train, y_train)

os.makedirs("model", exist_ok=True)
with open("model/gesture_model.pkl", "wb") as f: pickle.dump(model, f)

print("✅ Model trained successfully with only valid rows.")
