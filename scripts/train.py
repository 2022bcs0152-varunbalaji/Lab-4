import json
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, f1_score

DATA_PATH = "Lab_4/dataset/winequality-red.csv"

data = pd.read_csv(DATA_PATH, sep=";")

X = data.drop("quality", axis=1)
y = data["quality"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)

y_test_cls = (y_test >= 6).astype(int)
y_pred_cls = (y_pred >= 6).astype(int)

f1 = f1_score(y_test_cls, y_pred_cls)

metrics = {
    "mse": mse,
    "f1_score": f1
}

joblib.dump(model, "model.pkl")

with open("metrics.json", "w") as f:
    json.dump(metrics, f, indent=4)

print("Training complete")
print(metrics)
