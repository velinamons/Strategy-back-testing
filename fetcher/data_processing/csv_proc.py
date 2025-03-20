import io

import pandas as pd

from fetcher.config import data_enums


def to_dataframe(csv_data: io.StringIO) -> pd.DataFrame:
    """
        Reads a CSV and converts it into a Pandas DataFrame with correct dtypes.

        :param csv_data: StringIO object containing the CSV data.
        :return: Pandas DataFrame with parsed Klines data.
        """

    df = pd.read_csv(csv_data, header=None, names=data_enums.CSV_COLUMNS, on_bad_lines="skip")

    missing_columns = [col for col in data_enums.TARGET_COLUMNS if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing columns in CSV: {missing_columns}")

    return df
