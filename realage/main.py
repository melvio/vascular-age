#!/usr/bin/env python3
import logging
import sys

import pandas as pd

from realage.appconfig import ApplicationConfiguration
from realage.pipeline.pipe import Pipeline
from realage.researchenv import Environment

#%%
pd.set_option('display.max_columns', None)


#%%


def configure_logging() -> logging.Logger:
    # TODOn2h: logfile
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    return logging.getLogger(__name__)


log = configure_logging()


#%%
def setup_researchenv() -> Environment:
    return Environment().setup()


#%%
def main():
    configure_logging()
    setup_researchenv()

    config = ApplicationConfiguration(file='config.yaml').load_and_store()
    Pipeline(**config).pipe()

    return 0


if __name__ == '__main__':
    main()
