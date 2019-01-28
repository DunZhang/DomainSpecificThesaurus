from setuptools import setup, find_packages

setup(
    name='domain-thesaurus',
    version="1.0",
    description=('extract domain thesaurus automatically'),
    long_description=open('README.rst').read(),
    author='ZhangDun, ChenXiang, Chunyang Chen',
    author_email='dunnzhang0@gmail.com, xchencs@ntu.edu.cn, chunyang.chen@monash.edu',
    maintainer='ZhangDun',
    maintainer_email='dunnzhang0@gmail.com',
    license='MIT',
    packages=find_packages(),
    url='https://github.com/DunZhang/DomainSpecificThesaurus',
    install_requires=['gensim>=3.6.0', 'networkx>=2.1'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Operating System :: MacOS',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering :: Artificial Intelligence'
    ],
)
