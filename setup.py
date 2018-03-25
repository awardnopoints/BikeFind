from setuptools import setup

setup(name='bikefind',
      version='0.1',
      description='finds bikes in the city centre',
      author='Eoin Moore, Martin Casey, Conor Hopkins',
      packages=['bikefind'],
      include_package_data=True,
      install_requires=[
          'flask',
          'requests',
          'sqlalchemy',
          'cymysql',
          'pandas'
        ],
#	scripts=['bin/bf_display', 'bin/bf_scrape']
      entry_points={
              'console_scripts':[
                  'bf_display=bikefind.app:appWrapper',
                  'bf_scrape=bikefind.webscraper:main'
                  ]
              }
      )

