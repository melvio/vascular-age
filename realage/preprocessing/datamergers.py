from pandas import DataFrame

from realage.researchenv import Environment


class CtCalMriDimReducedDataMerger:
    _MRI_COLUMN_SUFFIX = '_mri'

    def __init__(self, *, ct_df: DataFrame, mri_df: DataFrame,
                 drop_when_not_in_both_datasets: bool = Environment().remove_entry_when_missing_mri_by_default):
        self.ct_df = ct_df.copy()
        self.mri_df = mri_df.copy()

        self.drop_when_not_in_both_datasets = drop_when_not_in_both_datasets

    def merge(self) -> DataFrame:
        if self.drop_when_not_in_both_datasets:
            result_df = self._drop_when_not_in_both_datasets(self.full_df)
        else:
            raise NotImplementedError(f"`self.drop_when_not_in_both_datasets=False` is not extensively tested"
                                      " but is likely to just work. "
                                      " Throwing NotImplementedError just as reminder to you to "
                                      "verify that it does work, might you ever need it.")

        return result_df

    @property
    def full_df(self) -> DataFrame:
        return self.ct_df.join(self.mri_df.set_index('ergoid'), on='ergoid',
                               rsuffix=CtCalMriDimReducedDataMerger._MRI_COLUMN_SUFFIX)

    def _drop_when_not_in_both_datasets(self, data: DataFrame) -> DataFrame:
        result_df = data.dropna(subset=['has_ct'])
        # everybody should have had should hold if the datasets where properly intersected in the first place
        # this will probably fail if we type check MRI data when loading.. Which is okay
        assert all(result_df['has_ct'] == 1.0)
        return result_df

#%%
# from realage.preprocessing.dataloaders import MriDimReducedDataLoader, CtCalcificationsDataLoader
# from realage.preprocessing.datacleaners import CtCalcificationsCleaner
#
# ct_df = CtCalcificationsDataLoader().load_dataframe()
# ct_df = CtCalcificationsCleaner(ct_df).clean()
# mri_df = MriDimReducedDataLoader().load_dataframe()
#
# merger = CtCalMriDimReducedDataMerger(ct_df=ct_df, mri_df=mri_df)
# df_result = merger.merge()
