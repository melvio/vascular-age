from typing import Union, List
from pandas import DataFrame


class ColumnSelector:
    DEFAULT_KEEP_COLUMNS = [
        'tot_vol_cor', 'tot_vol_aor', 'tot_vol_eci',
        'tot_vol_ici', 'tot_vol_vbac'
    ]
    DEFAULT_KEEP_LABEL = 'age'

    def __init__(self, data: DataFrame, *,
                 keep_columns: Union[str, List[str]] = 'default'):
        self.data = data
        self._keep_columns = keep_columns

    @property
    def keep_columns(self):
        feature_cols = ColumnSelector.DEFAULT_KEEP_COLUMNS \
            if self._keep_columns == 'default' \
            else self._keep_columns
        return feature_cols + [ColumnSelector.DEFAULT_KEEP_LABEL]

    def select(self):
        self.data = self.data.set_index('ergoid') # hidden side effect!
        self.data = self.data[self.keep_columns]
        return self.data
