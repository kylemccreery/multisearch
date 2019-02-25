from setuptools import setup, find_packages

version = '3.0.0'

setup(name='multisearch',
      version=version,
      description='HI LGS web price scraper for MTG',
      url='https://github.com/kylemccreery/multisearch',
      author='Kyle McCreery',
      author_email='mccreery.kyle@gmail.com',
      packages=find_packages(),
      install_requires=['BeautifulSoup4','bs4','requests'],
      keywords=['multisearch', 'MTG', 'Hawaii', 'LGS'],
      license='MIT',
      classifiers=[
          # Indicate who your project is intended for
          'Intended Audience :: Developers',
          # Pick your license as you wish (should match "license" above)
          'License :: OSI Approved :: MIT License',

          # Specify the Python versions you support here. In particular, ensure
          # that you indicate whether you support Python 2, Python 3 or both.
          'Programming Language :: Python :: 3'
      ])
