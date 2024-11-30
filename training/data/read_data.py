import os
import sys
from sklearn.model_selection import train_test_split
import pandas as pd


def main(inp, out):
    csv = pd.read_csv(f"{inp}/train.csv",  index_col=False)

    x = csv.drop(columns=["class"])
    y = csv["class"]

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1, random_state=123)

    x_train.to_csv(os.path.join(out, 'x_train.csv'), index=False)
    x_test.to_csv(os.path.join(out, 'x_test.csv'), index=False)
    y_train.to_csv(os.path.join(out, 'y_train.csv'), index=False)
    y_test.to_csv(os.path.join(out, 'y_test.csv'), index=False)

main(sys.argv[1], sys.argv[2])