import pandas as pd

class DFPlus(pd.DataFrame):
    @property
    def _constructor(self):
        return DFPlus

    @classmethod
    def from_csv(cls, filepath, **kwargs):
        df = pd.read_csv(filepath, **kwargs)
        return cls(df)

    def print_with_headers(self):
        rows = len(self)
        for start in range(0, rows, 10):
            end = min(start + 10, rows)
            rows_to_print = super().iloc[start:end]
            print(rows_to_print)
            print("-" * 40)

if __name__ == "__main__":
    dfp = DFPlus.from_csv("../csv/products.csv")
    dfp.print_with_headers()
