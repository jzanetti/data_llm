from os.path import join

from pandas import read_parquet, DataFrame, read_csv

from data import  SAMPLE_DATA_PATH

def load_sample_data() -> DataFrame:
    """Load sample data, Wellington synthetic population

    Returns:
        DataFrame: sample data in dataframe
    """
    if SAMPLE_DATA_PATH.endswith("parquet"):
        return read_parquet(SAMPLE_DATA_PATH)
    elif SAMPLE_DATA_PATH.endswith("csv"):
        return read_csv(SAMPLE_DATA_PATH)