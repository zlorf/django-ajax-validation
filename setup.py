from setuptools import setup, find_packages

setup(
    name='django-ajax-validation',
    version='0.1.6-pozytywnie-1',
    description="This is fork of Kuba Janoszek's fork of original Alex Gaynor's django-ajax-validation.",
    author='Jacek Tomaszewski',
    author_email='jacek.tomek@gmail.com',
    url='http://github.com/zlorf/django-ajax-validation/tree/master',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    # Make setuptools include all data files under version control,
    # svn and CVS by default
    include_package_data=True,
    # Tells setuptools to download setuptools_git before running setup.py so
    # it can find the data files under Git version control.
    setup_requires=['setuptools_git'],
    zip_safe=False,
    )
