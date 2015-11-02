"""
Utility functions for loading configuration parameters from a configuration file.
"""
import configparser

CONF_FILE_NAME = 'rebrickable.ini'


def _get_config():
    """
    :return: a reference to the config object from configparser
    """
    config = configparser.ConfigParser()
    config.read(CONF_FILE_NAME)
    return config


def get_rebrickable_api_key():
    """
    :return: the Rebrickable.com API key
    """
    try:
        return _get_config()['DEFAULT']['RebrickableApiKey']
    except KeyError:
        return None
