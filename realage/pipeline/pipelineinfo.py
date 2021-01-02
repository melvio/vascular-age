from dataclasses import dataclass
from typing import Union


class AlreadySet(Exception):
    pass


class PipelineInfo:
    """
    Class containing non-config data relevant to research.
    Config of the pipeline does not belong here, handle that with appconfig.py

    Implementation:
    All attributes start out with a special value and are reassigned at
    most once when the pipeline receives new relevant information.
    Note that this behavior is not enforced right now.
    """
    _START_VALUE = "no_info"

    def __init__(self):
        self.n_before_handling_nans: Union[int, str] = PipelineInfo._START_VALUE
        """number of participants before removing nans"""

        self.n_before_checking_mri_entries: Union[int, str] = PipelineInfo._START_VALUE

        self.n: Union[int, str] = PipelineInfo._START_VALUE
        """ number of participants in final set """

    def __str__(self) -> str:
        return "PipelineInfo(\n" \
               f"    n_before_checking_mri_entries={self.n_before_checking_mri_entries},\n" \
               f"    n_before_handing_nans={self.n_before_handling_nans},\n" \
               f"    n={self.n}\n" \
               ")"

#%%

# pipeline1 = PipelineInfo()
# pipeline1.n = 3
#
# pipeline2 = PipelineInfo()
# print(pipeline2.n)
# pipeline2.n = 12
#
# print(pipeline1.n)
# print(pipeline2.n)
# PipelineInfo.n = 2
# print(pipeline2)
# print(PipelineInfo())
