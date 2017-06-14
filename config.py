class Config(object):
	"""docstring for Config"""
	DEBUG = True

class DevelopmentConfig(Config):
	"""docstring for DevelopmentConfig"""
	SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
	"""docstring for ProductionConfig"""
	DEBUG = False

class TestingConfig(Config):
	"""docstring for TestingConfig"""
	TESTING = True

app_config = {
	'development' : DevelopmentConfig,
	'production' : ProductionConfig,
	'testing' : TestingConfig
}
		