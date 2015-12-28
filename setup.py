from setuptools import setup, find_packages

version = '0.0.1'

with open('__init__.py') as f:
    for line in f:
        if line.find("__version__") >= 0:
            version = line.split("=")[1].strip()
            version = version.strip('"')
            version = version.strip("'")
            continue


test_requires = [
    'mock',
]

dev_requires = []

setup(name='stockinterface',
      version=version,
      description=u"Stockfighter interface",
      long_description=u"",
      classifiers=[
        'Development Status :: 1 - Pre-Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Gaming',
        'Topic :: Software Development',
        'Topic :: Finance'
      ],
      keywords='stockfighter client API',
      author=u"Lorenzo Moriondo",
      author_email='tunedconsulting@gmail.com',
      url='https://github.com/mec-is',
      license='Apache 2.0',
      packages=find_packages(exclude=['testing']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'asyncio'
      ],
      extras_require={
          'test': test_requires,
          'dev': test_requires + dev_requires,
      },
      entry_points=""
      )
