from pandas import DataFrame
from scipy.stats import mannwhitneyu


def confidence_interval95(data: DataFrame) -> DataFrame:
    return data.quantile([0.025, 0.975])


def compare_gender(*, data_male: DataFrame, data_female: DataFrame, col: str) -> (float, float):
    """ compare a male DataFrame and Female DataFrame based on data in column `col` """
    analysis = mannwhitneyu(x=data_male[col], y=data_female[col],
                            alternative='two-sided')
    print(f"analysis for {col}: {analysis}")
    return analysis


def percentage_zero_or_lower(*, data: DataFrame, col: str) -> float:
    """
    Return percentage of cells in column `col` that are (essentially)
    zero or lower
    """
    # reasonable enough delta for floating point:
    # https://docs.python.org/3/tutorial/floatingpoint.html
    delta = 0.001
    nominator = data[data[col] <= delta].shape[0]
    denominator = data[col].shape[0]
    return 100 * nominator / denominator
