import os
from example import env

# -- Read .env Variables
env.read("%s/.env" % os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)))

#==============================================================================
# Load Configuration File
# -- heroku config:add ENVIRONMENT=production
#==============================================================================

ENV_LOCAL = 'local'
ENV_DEVELOPMENT = 'dev'
ENV_STAGING = 'staging'
ENV_PRODUCTION = 'production'

ENVIRONMENT = env.get( 'ENVIRONMENT', ENV_LOCAL )
exec( 'from %s import *' % ENVIRONMENT )
