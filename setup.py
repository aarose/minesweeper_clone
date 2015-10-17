import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()

requires = [
    'pyramid',
    'pyramid_chameleon',
    'pyramid_tm',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
    'waitress',
    ]

setup(name='minesweeper',
      version='0.0',
      description='Game',
      long_description=README,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='minesweeper',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = minesweeper:main
      [console_scripts]
      initialize_test1_db = minesweeper.scripts.initializedb:main
      """,
      )
