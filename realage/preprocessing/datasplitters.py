from typing import Union, List
import numpy as np
from pandas import DataFrame


class CtCalcificationsDataSetSplitter:
    DEFAULT_FEATURES = ['tot_vol_cor', 'tot_vol_aor', 'tot_vol_eci', 'tot_vol_ici', 'tot_vol_vbac']

    def __init__(self, data: DataFrame, *,
                 feature_cols: Union[List[str], str] = 'default',
                 sample_size: Union[int, str] = 100):
        self.data = data.copy()

        if isinstance(feature_cols, str) and feature_cols != 'default':
            raise ValueError(f'a single str cannot be {feature_cols}')
        self._feature_cols = feature_cols

        if isinstance(sample_size, str) and sample_size != 'all':
            raise ValueError(f'a single str cannot be {sample_size}')
        self._sample_size = sample_size

    @property
    def feature_cols(self) -> List[str]:
        return CtCalcificationsDataSetSplitter.DEFAULT_FEATURES \
            if self._feature_cols == 'default' else self._feature_cols

    @property
    def target_col(self):
        return 'age'

    @property
    def sample_size(self) -> int:
        return len(self.data) if self._sample_size == 'all' else self._sample_size

    def split(self) -> (np.ndarray, np.ndarray):
        """
        This function:
        1. sub-samples the dataset
        2. returns a tuple of (features, labels)
        :return: (2d array, 1d array)
        """
        df = self.data.sample(self.sample_size, random_state=100)
        return self._get_features(df), self._get_labels(df)

    def _get_features(self, df: DataFrame) -> np.ndarray:
        return df[self.feature_cols].to_numpy()

    def _get_labels(self, df: DataFrame):
        labels = df[self.target_col].astype(float)  # age in days
        return labels.to_numpy()

# %%
# from realage.preprocessing.dataloaders import CtCalcificationsDataLoader, MriDimReducedDataLoader
# from realage.preprocessing.agecalculator import AgeCalculator
# from realage.preprocessing.datamergers import CtCalMriDimReducedDataMerger
#
# df_ct = CtCalcificationsDataLoader().load_dataframe()
# df_ct = AgeCalculator(df_ct).clean()
# df_mri = MriDimReducedDataLoader().load_dataframe()
# df = CtCalMriDimReducedDataMerger(ct_df=df_ct, mri_df=df_mri).merge()
#
# splitter = CtCalcificationsDataSetSplitter(df, sample_size='all',
#                                            feature_cols=['tot_vol_aor'])

# x, y = CtCalcificationsDataSetSplitter(df, sample_size='all').split()
# print(x.shape)
# print(y.shape)

# x, y = CtCalcificationsDataSetSplitter(df, sample_size='all', feature_cols=['tot_vol_cor']).split()
#
# print(x.shape)
# print(y.shape)
#
# try:
#     x, y = CtCalcificationsDataSetSplitter(df, sample_size='should_fail', feature_cols=['tot_vol_cor']).split()
# except:
#     print('expected')
