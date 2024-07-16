import litellm
import os


litellm.drop_params = True
os.environ['LITELLM_LOG'] = 'DEBUG'
