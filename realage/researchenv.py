#!/usr/bin/env/ python3

import datetime
import logging
import os
import sys
from pathlib import Path

log = logging.getLogger(__name__)


class DirectoryNotFound(Exception):
    pass


class Environment:
    _START_TIME = None

    def __init__(self):
        nodename = os.uname().nodename
        self.is_server_env = nodename == 'scs-kpsy-01.erasmusmc.nl'
        self.is_cartesius = 'bullx' in nodename  # todo: does this also work in batch server?

    def _get_env(self):
        """ Use polymorphism based on which machine this app is running """
        if self.is_server_env:
            return _ServerEnv()
        elif self.is_cartesius:
            return _CartesiusEnv()
        else:
            return _MockEnv()

    @property
    def project_dir(self) -> Path:
        return self._get_env().project_dir

    @property
    def data_rootpath(self) -> Path:
        rootpath = self._get_env().data_rootpath
        if not rootpath.is_dir():
            raise DirectoryNotFound(rootpath)
        return rootpath

    @property
    def data_ctcalcificationpath(self):
        return self.data_rootpath / 'ct' / 'calcifications'

    @property
    def start_date(self) -> datetime.date:
        return Environment._START_TIME.date()

    @property
    def start_time(self) -> datetime.time:
        # get start time without unused microseconds
        return Environment._START_TIME.time().replace(microsecond=0)

    @property
    def model_path(self) -> Path:
        return self._get_env().project_dir / 'models'

    @property
    def result_rootpath(self) -> Path:
        rootpath = self._get_env().project_dir / 'var' / 'results'
        if not rootpath.is_dir():
            raise DirectoryNotFound(rootpath)
        return rootpath

    @property
    def result_folder(self) -> Path:
        """Folder that will contain the results for this specific run"""
        # TODO:
        # (1) In next phase, update the 'ctcalcifications' part of the application
        # (2) make sure names are unique
        return self.result_rootpath \
               / 'ctcalcifications' \
               / self.start_date.strftime('%d-%m-%Y') \
               / self.start_time.strftime('%H%M%S')

    @property
    def fig_folder(self) -> Path:
        return self._get_env().project_dir / 'var' / 'figures'

    @property
    def is_running_in_interactive_pycharm_mode(self) -> bool:
        return sys.argv[0].endswith('pydevconsole.py')

    @property
    def remove_entry_when_missing_mri_by_default(self) -> bool:
        return self.is_server_env or self.is_cartesius

    def setup(self):
        """
        Setup environment.
        Call this function once when starting the application.
        """
        self._setup_startdatetime()
        self._create_resultfolder()
        return self

    def _create_resultfolder(self) -> None:
        folder = self.result_folder
        try:
            folder.mkdir(parents=True)
        except FileExistsError as e:
            log.debug('expected if parent dir already exists', exc_info=e)
        log.info(f"after run the result can be found in {folder}")

    def _setup_startdatetime(self) -> None:
        if Environment._START_TIME is None:
            Environment._START_TIME = datetime.datetime.now()
            log.info(f"started application at {self.start_time}")
        else:
            log.debug(f"Environment already setup")


class _ServerEnv(Environment):
    def __init__(self):
        super().__init__()
        self._project_dir = Path.home() / 'data' / 'd' / 'project'

    @property
    def project_dir(self) -> Path:
        return self._project_dir

    @property
    def data_rootpath(self) -> Path:
        return self.project_dir / 'DATA'


class _CartesiusEnv(Environment):
    def __init__(self):
        super().__init__()
        self._project_dir = Path.home() / 'Documents' / 'lcl' / 'old_realage'

    @property
    def project_dir(self):
        return self._project_dir

    @property
    def data_rootpath(self) -> Path:
        return self.project_dir / 'DATA'


class _MockEnv(Environment):
    def __init__(self):
        super().__init__()
        self._project_dir = Path.home() / 'Documents' / 'lcl' / 'scs-kpsy-01' / 'd' / 'project'

    @property
    def project_dir(self) -> Path:
        return self._project_dir

    @property
    def data_rootpath(self) -> Path:
        # files without any real data
        return self.project_dir / 'DATA' / 'mock'

# %%
# print(Environment().setup())
# print(Environment().is_cartesius)
# print(Environment().data_rootpath)
# print(Environment().result_rootpath)
# print(Environment().result_folder)
