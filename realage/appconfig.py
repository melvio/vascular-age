import yaml
import logging
from pathlib import Path
from realage.researchenv import Environment

log = logging.getLogger()


class NoFoundFile(Exception):
    pass


class ApplicationConfiguration:
    def __init__(self, *, file=None):
        self.file = file

    def load_and_store(self) -> dict:
        # todon2h: pull defaults from objects in configuration
        if self.file is None:
            log.info(f'no config file used. We looked in: {Path.cwd()}')
            return {}

        path = Path(self.file)
        if not path.is_file():
            raise NoFoundFile(f'Is {self.file} the correct path? Is it a file?')

        with open(self.file) as configfile:
            config = yaml.safe_load(configfile)

        ApplicationConfiguration._store_config_as_metadata(path)
        return config

    @staticmethod
    def _store_config_as_metadata(configfile: Path) -> None:
        metadatafile = Environment().result_folder / 'config_used.yaml'
        metadatafile.write_text(configfile.read_text())
