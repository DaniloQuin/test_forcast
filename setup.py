from setuptools import setup, find_packages

setup(name='trainer_codes',
	  version='0.2',
	  packages=find_packages(),
	  install_requires=['tensorflow>=1.13'],
	  include_package_data=True,
	  description='Humano detectado',
	  author='Danilo Quinteros',
	  author_email='daquinteros@uc.cl',
	  zip_safe=False)