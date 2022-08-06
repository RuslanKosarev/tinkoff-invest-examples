# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Optional, Union

from pydantic import BaseSettings

ROOT_PATH = Path(__file__).parent

SUFFIX = '_api_key'
SECRETS_DIR_NAME = '../secrets'
SECRETS_ENV_FILE_NAME = 'secrets.env'
DEFAULT_SECRETS_DIR = ROOT_PATH.parent / SECRETS_DIR_NAME
DEFAULT_SECRETS_ENV_FILE_PATH = ROOT_PATH.parent / SECRETS_ENV_FILE_NAME


class SecretNotFoundError(Exception):
    pass


class Secrets(BaseSettings):
    """API key and tokens storage

    See Also
    --------
    get_secrets

    """

    alphavantage_api_key: Optional[str]
    iexcloud_api_key: Optional[str]
    quandl_api_key: Optional[str]
    polygon_api_key: Optional[str]
    finnhub_api_key: Optional[str]
    intrinio_api_key: Optional[str]
    tinvest_api_key: Optional[str]

    def get_api_key(self, module: str) -> Union[None, str]:
        provider_name = module.rsplit('.', maxsplit=1)[-1]

        dict_keys = self.__dict__
        key_name = f'{provider_name}{SUFFIX}'

        if key_name in dict_keys.keys():
            return dict_keys[key_name]
        else:
            return None

    class Config:
        env_file = None
        secrets_dir = None

    def __getattribute__(self, name):
        """Lazy checking/validating secret values
        """

        getattribute = super().__getattribute__
        fields = getattribute('__fields__')

        if name not in fields:
            return getattribute(name)

        value = getattribute('__dict__')[name]

        if not value:
            raise SecretNotFoundError(
                f"'{name}' secret was not found.\n\n"
                f"You need to create '{DEFAULT_SECRETS_ENV_FILE_PATH}' file or use your custom secrets env file "
                f"via `get_secrets` function or `_env_file` constructor argument with line: "
                f"{name}=SECRET_VALUE\n\n"
                f"Also you can create {DEFAULT_SECRETS_DIR} directory or use your custom secrets directory via "
                f"`get_secrets` function or `_secrets_dir` constructor argument with secret file with name '{name}' "
                f"that contains the secret value.\n\n"
                f"See pydantic documentation for more info: https://pydantic-docs.helpmanual.io/usage/settings/"
            )

        return value


def get_secrets(*,
                secrets_dir: Optional[Path] = None,
                secrets_env_file: Optional[Path] = None) -> Secrets:
    """Returns settings object with secrets (keys, tokens, etc)

    - If ``secrets_dir`` and ``secrets_env_file`` were not set, default ``secrets_dir`` and ``secrets_env_file``
      will be used
    - If ``secrets_dir`` was set, ``secrets_env_file`` will not be used
    - If ``secrets_env_file`` was set, ``secrets_dir`` will not be used
    - If ``secrets_dir`` and ``secrets_env_file`` were set, both will be used

    Parameters
    ----------
    secrets_dir : Path, None
        A path to secrets directory to find secret files or None for default
    secrets_env_file : Path, None
        A path to env file that contains secrets in environment variables or None for default

    Returns
    -------
    secrets : Secrets
        Secrets instance

    See Also
    --------
    Secrets

    """

    if secrets_dir and not secrets_dir.exists():
        print("The given secrets directory '%s' does not exist", secrets_dir)

    if secrets_env_file and not secrets_env_file.exists():
        print("The given secrets env file '%s' does not exist", secrets_env_file)

    if not secrets_dir and not secrets_env_file:
        secrets_dir = DEFAULT_SECRETS_DIR
        secrets_env_file = DEFAULT_SECRETS_ENV_FILE_PATH

    is_secrets_dir = secrets_dir is not None and secrets_dir.is_dir()
    is_secrets_env_file = secrets_env_file is not None and secrets_env_file.is_file()

    if not is_secrets_dir and not is_secrets_env_file:
        print("Secrets directory and secrets .env file do not exist. Loading secrets from env vars.")

    if is_secrets_dir and not is_secrets_env_file:
        print("Loading secrets from secrets directory '%s'.", secrets_dir)
    elif not is_secrets_dir and is_secrets_env_file:
        print("Loading secrets from secrets .env file '%s'.", secrets_env_file)
    elif is_secrets_dir and is_secrets_env_file:
        print("Loading secrets from secrets .env file '%s' and secrets directory '%s'.", secrets_env_file, secrets_dir)

    kwargs = {}

    if is_secrets_dir:
        kwargs['_secrets_dir'] = secrets_dir

    if is_secrets_env_file:
        kwargs['_env_file'] = secrets_env_file

    return Secrets(**kwargs)
