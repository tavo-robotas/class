import os
import yaml


def load_use_case_config():
    return load_config("./config.yaml")


def load_config(config_file):
    with open(os.path.join(os.getcwd(), config_file), 'r') as f:
        config = yaml.safe_load(f)

    assert config
    return config
