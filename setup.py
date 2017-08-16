from setuptools import setup

setup(name='scrorg',
      version='1.0',
      description="Screenshot tool for Emacs' org-mode",
      url='https://github.com/RetepRennelk/scrorg.git',
      author='Peter Klenner',
      author_email='peterklenner@gmx.de',
      license='MIT',
      packages=['scrorg'],
      entry_points = {
        'console_scripts': ['scrorg=scrorg:main']}
      )