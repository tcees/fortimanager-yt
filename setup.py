#!/usr/bin/env python

from distutils.core import setup

setup(name='fortimanager_yt',
      version='1.0',
      description='Automatização de liberação de videos do YouTube no FortiManager',
      author='Tribunal de Contas do Espirito Santo, STI',
      url='https://tce.es.gov.br',
      packages=['fortimanager_yt'],
      include_package_data=True,
      install_requires=['bs4', 'requests', 'jinja2']
     )
