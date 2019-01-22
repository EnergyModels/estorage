from setuptools import setup

setup(name='estorage',
      version='0.1',
      description='estorage - TBD',
      url='https://github.com/EnergyModels/estorage',
      author='Jeff Bennett',
      author_email='jab6ft@virginia.edu',
      license = 'MIT',
      packages=['estorage'],
      zip_safe=False,
      install_requires=['CoolProp','pandas', 'numpy', 'matplotlib', 'seaborn'])