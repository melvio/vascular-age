#!/usr/bin/env python3

import numpy as np
import logging
from numpy.random import default_rng, Generator
from pandas import DataFrame


log = logging.getLogger(__name__)


# %%


class MissingRequiredColumns(Exception):
    pass


class CtCalcificationNoiser:
    def __init__(self, data: DataFrame, *,
                 shuffle_ids=True, add_noise_to_ids=True, add_noise_to_dates=True, add_noise_to_floats=True,
                 write_to_file=False):
        """
        :param data:
        :param shuffle_ids:
        :param add_noise_to_ids:
        :param add_noise_to_dates:
        :param add_noise_to_floats:
        :param write_to_file: if False don't write. if True write to test.csv. If string, interpret as path.
        """
        self.data = data.copy()
        self.rng: Generator = default_rng()
        self.shuffle_ids = shuffle_ids
        self.add_noise_to_ids = add_noise_to_ids
        self.add_noise_to_dates = add_noise_to_dates
        self.add_noise_to_floats = add_noise_to_floats
        self.write_to_file = write_to_file

    def noisify(self) -> DataFrame:
        self.validate()
        if self.shuffle_ids:
            self.data = self._shuffle_ids()
        if self.add_noise_to_ids:
            self.data = self._add_noise_to_ids()
        if self.add_noise_to_dates:
            self.data = self._add_noise_to_ids()
        if self.add_noise_to_floats:
            self.data = self._add_noise_to_floats()
        if self.write_to_file:
            self._write_to_calcifications_csv(self.write_to_file)
        return self.data

    def validate(self, *, on_error='raise') -> None:
        # remark: refactoring could make birthdate and scandate not required later on
        required_columns = ['ergoid', 'birthdate', 'scandate']
        valid_columns = all([col in self.data.columns for col in required_columns])
        if not valid_columns:
            if on_error == 'raise':
                raise MissingRequiredColumns(f'required columns are: {required_columns}')
            else:
                raise MissingRequiredColumns(NotImplementedError())
        else:
            log.debug(f'validate found valid dataframe with columns: {self.data.columns}')

    def _shuffle_ids(self) -> DataFrame:
        ids = self.data['ergoid'].to_numpy(dtype=int)
        self.rng.shuffle(ids)  # in place
        return self.data

    def _add_noise_to_ids(self, *, remove_duplicates=False) -> DataFrame:
        self.data['ergoid'] += self.rng.integers(low=-2, high=3, size=self.data['ergoid'].size)
        if remove_duplicates:
            raise NotImplementedError()
        return self.data

    def _add_noise_to_dates(self, *, add_years=10) -> DataFrame:
        # TODO: instead of hardcoding columsn, use select_dtypes
        daydiff1 = self.rng.normal(scale=180, size=self.data['birthdate'].size).astype(int)
        daydiff2 = self.rng.normal(scale=20, size=self.data['scandate'].size).astype(int)

        self.data['birthdate'] += np.array(daydiff1, dtype='timedelta64[D]')
        self.data['scandate'] += np.array(daydiff1 + daydiff2, dtype='timedelta64[D]')

        # N2H: adhere to single resp. principle
        if add_years:
            self.data['birthdate'] += np.timedelta64(add_years, 'Y')
            self.data['scandate'] += np.timedelta64(add_years, 'Y')

        return self.data

    def _add_noise_to_floats(self, *, round_ndigits=2) -> DataFrame:
        """
        get all float entries of 'data' and add some percentage.
        The percentage is normally distributed with mean=0 and std=0.15
        """
        df_floats = self.data.select_dtypes('float')
        diff = self.rng.normal(scale=0.15, size=df_floats.shape)
        df_floats += df_floats * diff
        df_floats = round(df_floats, round_ndigits)

        # check if negative values were created:
        # assert not (df_floats.to_numpy() < 0).any()
        self.data.loc[:, df_floats.columns] = df_floats
        return self.data

    def _write_to_calcifications_csv(self, path):
        out = self.data.copy()
        out = out.sort_values('ergoid')
        out.columns = out.columns.str.capitalize()

        csv_params = dict(index=False, date_format='%d/%m/%Y')
        out.to_csv('test.csv' if path is True else path, **csv_params)

# %%

# df = CtCalcificationsDataLoader().load_dataframe()
# df = CtCalcificationsCleaner(df, create_age=False, remove_when_no_mri=False).clean()
#
# print(df)
#
# noiser1 = CtCalcificationNoiser(df)
# df2 = noiser1.noisify()
#
# print(f'df2: {df2}')
# noiser2 = CtCalcificationNoiser(df2)
# print(f'df3: {noiser2.noisify()}')
#
