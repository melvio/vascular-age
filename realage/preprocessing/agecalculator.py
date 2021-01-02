# %%
from pandas import DataFrame


class UnexpectedColumns(Exception):
    pass


class FailedCreatingAgeColumn(Exception):
    pass


class AgeCalculator:
    def __init__(self, data: DataFrame, *,
                 create_age=True):

        self.create_age = create_age  # append age column calculated from from scandate and birthdate
        self.data: DataFrame = data.copy()

    def calculate(self) -> DataFrame:
        self.validate()
        if self.create_age:
            self.data = self._create_age()

        return self.data

    def validate(self) -> None:
        """ Check if this is the DataFrame that we expected"""
        expected_columns = ['ergoid', 'birthdate', 'scandate', 'tot_vol_cor', 'tot_vol_aor',
                            'tot_vol_eci', 'tot_vol_ici', 'tot_vol_vbac']
        valid_columns = all([col in expected_columns for col in self.data.columns])
        valid_col_length = len(expected_columns) == len(self.data.columns)
        if not valid_columns or not valid_col_length:
            raise UnexpectedColumns(self.data.columns)

    # TODOn2h: put this in a 'column' creating class (feature creation)
    def _create_age(self) -> DataFrame:
        # age at scan time
        self.data['age'] = (self.data['scandate'] - self.data['birthdate']).astype('timedelta64[D]') / 365.25
        if self.data['age'].hasnans:
            raise FailedCreatingAgeColumn()

        return self.data

# %%

# from realage.preprocessing.dataloaders import CtCalcificationsDataLoader
# df = CtCalcificationsDataLoader().load_dataframe()
# df = AgeCalculator(df).calculate()
# print(df)
