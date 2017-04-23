from setuptools import setup, find_packages
#this is a test
setup(name = 'django_carbon',
      description = 'Django Carbon Library',
      version = '0.14',
      url = 'https://github.com/ninapavlich/django-carbon/',
      author = 'Nina Pavlich',
      author_email='nina@ninalp.com',
      license = 'BSD',
      packages=find_packages(exclude=['ez_setup']),
      zip_safe = False,
      include_package_data=True,
      install_requires = ['setuptools', 'Django', 'boto', 'django-ace', 
      'django-appconf', 'django-ckeditor', 'django-debug-toolbar', 
      'django-extensions','django-grappelli', 'django-imagekit', 
      'django-localflavor', 'django-reversion', 'pilkit', 
      'django-storages', 'six', 'sqlparse', 'wsgiref', 'csscompressor', 'slimit'],
      classifiers=[
            'Development Status :: 1 - Planning',
            'Environment :: Web Environment',
            'Framework :: Django',
            'Intended Audience :: Developers',
            'License :: OSI Approved',
            'Operating System :: OS Independent',
            'Programming Language :: Python'
      ]
)