import os
from setuptools import setup, find_packages

version = "1.0"

description = """ """ 

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()
    
long_description = read('README.rst')
    
setup(name='FlyBehaviors',
      author="",
      author_email="",
      url='http://www.cds.caltech.edu/',
      
      description=description,
      long_description=long_description,
      keywords="PROJECT_KEYWORDS",
      license="PROJECT_LICENSE",
      
      classifiers=[
        'Development Status :: 4 - Beta',
        # 'Intended Audience :: Developers',
        # 'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        # 'Topic :: Software Development :: Quality Assurance',
        # 'Topic :: Software Development :: Documentation',
        # 'Topic :: Software Development :: Testing'
      ],

	  version=version,
      download_url='http://github.com/AndreaCensi/fly_behaviors/tarball/%s' % version,
      
      package_dir={'':'src'},
      packages=find_packages('src'),
      install_requires=[ ],
      tests_require=['nose'],
      entry_points={'console_scripts': [
           'fly_behaviors_simulations = fly_behaviors.manager.main:main'

        ]},
)

