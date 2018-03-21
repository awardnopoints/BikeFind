from setuptools import setup

setup(name='bikefind',
      version='0.1',
      description='finds bikes in the city centre',
      author='Eoin Moore, Martin Casey, Conor Hopkins',
      packages=['bikefind'],
      include_package_data=True,
      install_requires=[
          'flask',
          'request',
          'sqlalchemy',
          'cymysql',
        ],
      entry_points={
              'console_scripts':[
                  'bf_display=bikefind.app:app.run',
                  'bf_scrape=bikefind.webscraper:main'
                  ]
              }
      )

