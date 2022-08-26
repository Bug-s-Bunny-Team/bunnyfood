import os

__version__ = '0.1.0'

API_TITLE = 'BunnyFood'
API_DESCRIPTION = 'API for BunnyFood UI'

ENV = os.environ.get('ENV', 'dev')
PREFIX = '/api' if ENV == 'prod' else ''
