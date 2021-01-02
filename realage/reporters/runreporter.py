from pandas import DataFrame

from realage.reporters.base import Reporter, ReportStrategy, UnsupportedStrategy, MissingColumn
from realage.researchenv import Environment


#%%
class CtCalcificationsReporter(Reporter):

    def __init__(self, result_data: DataFrame, *,
                 strategy: ReportStrategy = ReportStrategy.TO_FILE,
                 prettify: bool = True):
        """
        :param result_data: The data that we will report on
        :param strategy: Whether to write to file, print to stdout or just return.
        :param prettify: When True, enhance the output
        """
        self.result_data = result_data.copy()
        if strategy not in ReportStrategy:
            raise UnsupportedStrategy(f'{strategy} is not in the supported ReportStrategy')
        self.strategy = strategy
        self.prettify = prettify

    def report(self) -> DataFrame:
        if self.prettify:
            self.result_data = self._prettify_results()

        if ReportStrategy.TO_FILE == self.strategy:
            self.report_to_file()
        elif ReportStrategy.TO_STDOUT == self.strategy:
            print(self.result_data)

        return self.result_data

    def report_to_file(self) -> None:
        """ Write the report to a csv file."""
        filename = 'results.csv'
        self.result_data.to_csv(Environment().result_folder / filename)

    def _prettify_results(self) -> DataFrame:
        if 'score' not in self.result_data.columns:
            raise MissingColumn(f"could not find 'score' column in {self.result_data.columns} ")
        return self.result_data.sort_values(by='score')

#%%
#
# import numpy as np
#
# string = "test wordst"
#
# df = DataFrame(np.arange(10).reshape((5, 2)), columns=['score', 'other_value'])
#
# reporter = CtCalcificationsReporter(df)
# Warn: report() writes to a file
# df = reporter.report()
# print(df)
