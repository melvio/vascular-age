from typing import Union, List
from pandas import DataFrame
from sklearn.base import RegressorMixin, TransformerMixin

from realage.preprocessing.dataloaders import CtCalcificationsDataLoader, MriDimReducedDataLoader
from realage.preprocessing.agecalculator import AgeCalculator
from realage.preprocessing.columnselector import ColumnSelector
from realage.preprocessing.columnscaler import ColumnScaler
from realage.preprocessing.datamergers import CtCalMriDimReducedDataMerger
from realage.preprocessing.nanhandler import NanHandler
from realage.preprocessing.datasplitters import CtCalcificationsDataSetSplitter
from realage.models.runners import CtCalcificationModelRunner, RunResults
from realage.pipeline.pipelineinfo import PipelineInfo
from realage.reporters.predictionreporter import PredictionReporter
from realage.reporters.runreporter import CtCalcificationsReporter
from realage.reporters.pipereporter import PipelineReporter


class Pipeline:
    def __init__(self, *,
                 k: int = 5,
                 scaling: Union[str, bool, TransformerMixin] = 'default',
                 models: [RegressorMixin] = None,
                 feature_cols: Union[str, List[str]] = 'default',
                 pipeline_info: PipelineInfo = None):
        self.k = k
        self.models = models
        self.scaling = scaling
        self.feature_cols = feature_cols
        self.pipeline_info = PipelineInfo() if pipeline_info is None else pipeline_info

    def pipe(self) -> None:
        df = self.preprocess()
        results = self.run_models(df)
        self.report_results(results)

    def preprocess(self) -> DataFrame:
        mri_df = MriDimReducedDataLoader().load_dataframe()
        ct_df = CtCalcificationsDataLoader().load_dataframe()
        ct_df = AgeCalculator(ct_df).calculate()
        self.pipeline_info.n_before_checking_mri_entries = len(ct_df)
        df = CtCalMriDimReducedDataMerger(ct_df=ct_df, mri_df=mri_df).merge()

        self.pipeline_info.n_before_handling_nans = len(df)
        df = NanHandler(df).handle()
        self.pipeline_info.n = len(df)

        # TODOn2h: fix little bit of duplication in the column logic (also see the runner)
        df = ColumnSelector(df, keep_columns=self.feature_cols).select()
        df = ColumnScaler(df, scale_columns=self.feature_cols, scaling=self.scaling).scale()
        return df

    def run_models(self, data: DataFrame) -> RunResults:
        X, y = CtCalcificationsDataSetSplitter(
            data,
            feature_cols=self.feature_cols,
            sample_size='all',
        ).split()
        results = CtCalcificationModelRunner(k=self.k, models=self.models).run_models(features=X, labels=y)
        return results

    def report_results(self, run_result: RunResults) -> None:
        reporters = [
            CtCalcificationsReporter(run_result.kfold_results),
            PipelineReporter(self.pipeline_info),
            PredictionReporter(run_result.age_predictions),
        ]
        for reporter in reporters:
            reporter.report()
