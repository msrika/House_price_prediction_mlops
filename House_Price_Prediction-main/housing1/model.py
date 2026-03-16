import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pickle

# 1. Load dataset
df = pd.read_csv("data/house_price.csv")

# 2. Inspect columns
print(df.columns)

# 3. Set features (X) and target (y)
# 👉 Replace "SalePrice" with your actual target column name
X = df.drop("SalePrice", axis=1)
y = df["SalePrice"]

# 4. Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 5. Train the model
model = LinearRegression()
model.fit(X_train, y_train)

# 6. Save the model
pickle.dump(model, open("model.pkl", "wb"))

print("Model trained & saved successfully!")


