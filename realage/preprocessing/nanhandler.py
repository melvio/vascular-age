import logging

import numpy as np
from pandas import DataFrame

log = logging.getLogger(__name__)


class NanStrategyNotImplemented(NotImplementedError):
    pass


class NanHandler:
    def __init__(self, data: DataFrame, *, strategy='drop_rows'):
        self.data = data.copy()
        # TODOn2h: use enum or polymorphism
        self.strategy = strategy

    def handle(self) -> DataFrame:
        if self.strategy == 'drop_rows':
            self.data = self._drop_calcium_missing_rows()
        else:
            raise NanStrategyNotImplemented(f'strategy not supported: "{self.strategy}"')

        return self.data

    def _drop_calcium_missing_rows(self):
        """ dropping rows if they contain a 'nan' in the calcium rows """
        # 88888.8 indicates a missing value
        columns_with_88888_as_nan = [
            'tot_vol_cor', 'tot_vol_aor', 'tot_vol_eci', 'tot_vol_ici', 'tot_vol_vbac'
        ]
        self.data[columns_with_88888_as_nan] = self.data[columns_with_88888_as_nan].replace({88888.8: np.nan})

        return self.data.dropna(subset=columns_with_88888_as_nan)


#%%
# from realage.preprocessing.dataloaders import CtCalcificationsDataLoader

# df = CtCalcificationsDataLoader().load_dataframe()

# columns_with_88888_as_nan = [
#     'tot_vol_cor', 'tot_vol_aor', 'tot_vol_eci', 'tot_vol_ici', 'tot_vol_vbac'
# ]
# #
# df = DataFrame(columns=columns_with_88888_as_nan, data=[[88888.8, 0, 0, 0, 0], [0, 0, 0, 0, 0]])
#
# nanhandler = NanHandler(df)
# nanhandler.handle()
