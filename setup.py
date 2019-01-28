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
    license='BSD License',
    packages=find_packages(),
    platforms=["all"],
    url='https://github.com/DunZhang/DomainSpecificThesaurus',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
)
