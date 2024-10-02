from os.path import join

from pandas import read_parquet, DataFrame

from data import  SAMPLE_DATA_PATH

def load_sample_data() -> DataFrame:
    """Load sample data, Wellington synthetic population

    Returns:
        DataFrame: sample data in dataframe
    """
    return read_parquet(SAMPLE_DATA_PATH)