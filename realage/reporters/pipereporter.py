#%%
import pandas as pd

from realage.pipeline.pipelineinfo import PipelineInfo
from realage.reporters.base import ReportStrategy, Reporter, UnsupportedStrategy
from realage.researchenv import Environment


class PipelineReporter(Reporter):
    def __init__(self, pipeline_info: PipelineInfo, *,
                 strategy: ReportStrategy = ReportStrategy.TO_FILE):
        self.pipeline_info = pipeline_info
        self.strategy = strategy

    def report(self) -> PipelineInfo:
        if self.strategy == ReportStrategy.TO_FILE:
            self.report_to_file()
        elif self.strategy == ReportStrategy.TO_STDOUT:
            print(PipelineInfo())
        else:
            raise UnsupportedStrategy(f'{self.strategy} not supported')

        return PipelineInfo()

    def report_to_file(self):
        report = pd.Series(
            data=self._pipeline_attrs_to_dict(),
            name='pipeline_attr_values',
        ).to_frame()

        filename = 'pipeline_info.csv'
        report.to_csv(Environment().result_folder / filename)

    def _pipeline_attrs_to_dict(self):
        # get all attributes from a the pipeline
        # TODOn2h: This needs some serious refactoring later
        return {attr: getattr(self.pipeline_info, attr) for attr in dir(self.pipeline_info)
                if not attr.startswith('_')}

#%%
# from realage.pipelineinfo import PipelineInfo
#
# Environment().setup()
# PipelineInfo.n = 3
# p = PipelineReporter(PipelineInfo())
# p.report()
