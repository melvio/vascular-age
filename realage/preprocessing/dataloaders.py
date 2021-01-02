import abc
from abc import abstractmethod

import pandas as pd
from pandas import DataFrame

from realage.researchenv import Environment


class FailedColumnRename(Exception):
    pass


class DataLoader(abc.ABC):
    """
    Base class that can be reused to load any csv
    """

    # todo: determine if copying is really needed in this class
    def __init__(self, filepath):
        """
        :param filepath: relative path starting from, but not including, DATA/
"""
        self.filepath = filepath

    def full_datapath(self):
        return Environment().data_rootpath / self.filepath

    def standardize_column_names(self, data: DataFrame) -> DataFrame:
        new_columns: pd.Index = data.columns.str.casefold()
        new_columns: pd.Index = new_columns.str.strip()
        if not new_columns.is_unique:
            raise FailedColumnRename("`casefold()` created columns with the same name.\n"
                                     f"Maybe check the input columns: {data.columns}")

        data.columns = new_columns
        return data

    def dates_in_days(self, data: DataFrame) -> DataFrame:
        data = data.copy()
        # N2H fix: NumPy does not seem to be very cooperative here
        data['scandate'] = data['scandate'].astype('datetime64[D]')
        data['birthdate'] = data['birthdate'].astype('datetime64[D]')
        return data

    @abstractmethod
    def load_dataframe(self) -> DataFrame:
        pass


# %%
class DefaultDataLoader(DataLoader):
    """
      Extend from this class if you only want to set 'ergoid' as index col and don't want any other transformations
      to happen.
     """

    def __init__(self, filepath: str):
        DataLoader.__init__(self, filepath)

    def load_dataframe(self) -> pd.DataFrame:
        return pd.read_csv(self.full_datapath(), index_col='ergoid')


class CtCalcificationsDataLoader(DataLoader):
    """
    A dataloader loads the data in consistent manner.
    """

    def __init__(self, filepath: str = 'ct/calcifications/acv_impute_dots.csv'):
        DataLoader.__init__(self, filepath)

    def load_dataframe(self) -> DataFrame:
        df = pd.read_csv(self.full_datapath(), parse_dates=['Birthdate', 'Scandate'])
        df = self.standardize_column_names(df)
        return self.dates_in_days(df)


# %%
class MriDimReducedDataLoader(DataLoader):

    def __init__(self, filepath: str = 'mri/lowdim/mri_06aug2020.csv'):
        DataLoader.__init__(self, filepath)

    def load_dataframe(self) -> pd.DataFrame:
        df = pd.read_csv(self.full_datapath())
        return self.standardize_column_names(df)


# %%
class ResultTestDatasetLoader(DefaultDataLoader):

    def __init__(self, filepath: str = 'ct/calcifications/test/test_data_results.csv'):
        DataLoader.__init__(self, filepath)


# %%
class ResultTrainDatasetLoader(DefaultDataLoader):

    def __init__(self, filepath: str = 'ct/calcifications/train/train_data_results.csv'):
        DataLoader.__init__(self, filepath)


# %%
class ResultCombinedDatasetLoader(DefaultDataLoader):

    def __init__(self, filepath: str = 'ct/calcifications/combined/combined_results.csv'):
        DataLoader.__init__(self, filepath)


class ResultCombinedWithGenderDatasetLoader(DefaultDataLoader):

    def __init__(self, filepath: str = 'ct/calcifications/combined/singlelsvr_with_gender.csv'):
        DataLoader.__init__(self, filepath)


# %%
class GenderDatasetLoader(DefaultDataLoader):

    def __init__(self, filepath: str = 'ct/calcifications/gender/gender_combined.csv'):
        DataLoader.__init__(self, filepath)


# %%
class MaleDatasetLoader(DefaultDataLoader):

    def __init__(self, filepath: str = 'ct/calcifications/gender/male/male_all.csv'):
        DataLoader.__init__(self, filepath)


# %%
class FemaleDatasetLoader(DefaultDataLoader):

    def __init__(self, filepath: str = 'ct/calcifications/gender/female/female_all.csv'):
        DataLoader.__init__(self, filepath)


# %%
class MaleTestDatasetLoader(DefaultDataLoader):

    def __init__(self, filepath: str = 'ct/calcifications/gender/male/male_test.csv'):
        DataLoader.__init__(self, filepath)


# %%
class MaleTrainDatasetLoader(DefaultDataLoader):

    def __init__(self, filepath: str = 'ct/calcifications/gender/male/male_train.csv'):
        DataLoader.__init__(self, filepath)


# %%
class FemaleTestDatasetLoader(DefaultDataLoader):

    def __init__(self, filepath: str = 'ct/calcifications/gender/female/female_test.csv'):
        DataLoader.__init__(self, filepath)


# %%
class FemaleTrainDatasetLoader(DefaultDataLoader):

    def __init__(self, filepath: str = 'ct/calcifications/gender/female/female_train.csv'):
        DataLoader.__init__(self, filepath)


# %%
class FemaleTestResultDatasetLoader(DefaultDataLoader):
    def __init__(self, filepath: str = 'ct/calcifications/gender/results/female_test_results.csv'):
        DataLoader.__init__(self, filepath)


class FemaleTrainResultDatasetLoader(DefaultDataLoader):
    def __init__(self, filepath: str = 'ct/calcifications/gender/results/female_train_results.csv'):
        DataLoader.__init__(self, filepath)


# %%

class MaleTestResultDatasetLoader(DefaultDataLoader):
    def __init__(self, filepath: str = 'ct/calcifications/gender/results/male_test_results.csv'):
        DataLoader.__init__(self, filepath)


class MaleTrainResultDatasetLoader(DefaultDataLoader):
    def __init__(self, filepath: str = 'ct/calcifications/gender/results/male_train_results.csv'):
        DataLoader.__init__(self, filepath)


# %%
class PooledFemaleDatasetLoader(DefaultDataLoader):
    def __init__(self, filepath: str = 'ct/calcifications/gender/results/female_results_pooled.csv'):
        DataLoader.__init__(self, filepath)


class PooledMaleDatasetLoader(DefaultDataLoader):
    def __init__(self, filepath: str = 'ct/calcifications/gender/results/male_results_pooled.csv'):
        DataLoader.__init__(self, filepath)


class PooledDatasetLoader(DefaultDataLoader):
    def __init__(self, filepath: str = 'ct/calcifications/gender/results/results_pooled.csv'):
        DataLoader.__init__(self, filepath)
