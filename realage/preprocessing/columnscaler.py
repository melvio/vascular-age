from typing import Union, List, Tuple
from pandas import DataFrame
from sklearn.base import TransformerMixin
from sklearn.preprocessing import MinMaxScaler, RobustScaler, PowerTransformer, QuantileTransformer
from sklearn.utils.validation import check_is_fitted


class ColumnScaler:
    DEFAULT_COLUMNS = ['tot_vol_cor', 'tot_vol_aor', 'tot_vol_eci', 'tot_vol_ici', 'tot_vol_vbac']

    def __init__(self, data: DataFrame, *,
                 test_data: DataFrame = None,
                 scale_columns: Union[List[str], str] = 'default',
                 scaling: Union[TransformerMixin, bool] = PowerTransformer()):
        self.data = data.copy()
        self.test_data = test_data.copy() if test_data is not None else test_data
        self._scale_columns = scale_columns
        self._scaling = scaling
        self._has_fitted = False
        """If False don't scale, if 'default' use PowerTransformer, else use the specified scalar"""

    def scale(self) -> Union[DataFrame, Tuple[DataFrame, DataFrame]]:
        if self.scaling:
            # mutation!
            self.data[self.scale_columns] = self.scaling.fit_transform(self.data[self.scale_columns])
            self._has_fitted = True
            if self._scaling and self.test_data is not None:
                self.test_data[self.scale_columns] = self.scaling.transform(self.test_data[self.scale_columns])

        return (self.data, self.test_data) if self.test_data is not None else self.data

    @property
    def scale_columns(self) -> List[str]:
        return ColumnScaler.DEFAULT_COLUMNS if self._scale_columns == 'default' \
            else self._scale_columns

    @property
    def scaling(self) -> Union[TransformerMixin, bool]:
        if self._scaling is False:
            return False
        elif self._has_fitted:
            return self._scaling
        elif self._scaling == 'MinMaxScaler':
            return MinMaxScaler()
        elif self._scaling == 'RobustScaler':
            return RobustScaler()
        elif self._scaling == 'default' or self._scaling == 'PowerTransformer':
            return PowerTransformer()
        elif self._scaling == 'QuantileTransformer':
            return QuantileTransformer()
        else:
            assert isinstance(self._scaling, TransformerMixin)
            return self._scaling

