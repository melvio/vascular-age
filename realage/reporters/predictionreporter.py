from pandas import DataFrame

from realage.reporters.base import Reporter, ReportStrategy, UnsupportedStrategy
from realage.researchenv import Environment


class PredictionReporter(Reporter):
    def __init__(self, age_predictions: DataFrame, *,
                 strategy: ReportStrategy = ReportStrategy.TO_FILE):
        self.age_predictions = age_predictions
        self.strategy = strategy

    def report(self) -> DataFrame:
        if self.strategy == ReportStrategy.TO_FILE:
            self.report_to_file()
        elif self.strategy == ReportStrategy.TO_STDOUT:
            print(self.age_predictions)
        else:
            raise UnsupportedStrategy(f'{self.strategy} not supported')

        return self.age_predictions

    def report_to_file(self) -> None:
        filename = 'age_predictions.csv'
        self.age_predictions.to_csv(Environment().result_folder / filename)
