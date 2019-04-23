from setuptools import setup, find_packages

setup(name='trainer_codes',
	  version='0.1',
	  packages=find_packages(),
	  description='Humano detectado',
	  author='Danilo Quinteros',
	  author_email='daquinteros@uc.cl',
	  license='m',
	  install_requieres=['keras.preprocessing.image'],
	  zip_safe=False)