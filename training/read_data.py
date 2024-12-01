from sklearn.model_selection import train_test_split
import pandas as pd


train_data = pd.read_csv(f"data/train.csv")

x = train_data.drop(columns=["Rain"])
y = train_data['Rain'].replace({"no rain": 0}).replace({"rain": 1})

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1, random_state=123)


x_train.to_csv('data/x_train.csv', index=False)
x_test.to_csv('data/x_test.csv', index=False)
y_train.to_csv('data/y_train.csv', index=False)
y_test.to_csv('data/y_test.csv', index=False)