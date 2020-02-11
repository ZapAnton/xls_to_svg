from setuptools import setup, find_packages

setup(name='xls_to_svg',
      version='0.1.1',
      description='Convert XLS tables into SVG charts',
      url='https://github.com/ZapAnton/xls_to_svg',
      author='ZapAnton',
      python_requires='>=3.5',
      packages=find_packages(),
      install_requires=['matplotlib==3.1.2', 'numpy==1.18.1', 'xlrd==1.2.0'],
      entry_points={
          'console_scripts': [
              'xls_to_svg = xls_to_svg.__main__:main',
          ]
      })
