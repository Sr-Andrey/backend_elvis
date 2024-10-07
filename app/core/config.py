import os
import toml

current = os.path.dirname(os.path.abspath(__file__))

filename_with_settings = current + '/settings.toml'

current_config = toml.load(filename_with_settings)

POSTGRESQL = current_config['postgresql']
API = current_config['API']
