from setuptools import setup

setup(name='bikefind',
      version='0.1',
      description='finds bikes in the city centre',
      author='Eoin Moore, Martin Casey, Conor Hopkins',
      packages=['bikefind','bikefind.templates'],
      entry_points={
              'console_scripts':['bikefind=bikefind.app:app.run']
              }
      )
