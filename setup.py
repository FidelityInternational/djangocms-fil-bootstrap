from setuptools import find_packages, setup

import djangocms_fil_bootstrap


INSTALL_REQUIREMENTS = [
    "Django>=1.11,<3.0",
    "django-cms",
    "djangocms-column",
    "factory_boy>=2.11",
]

setup(
    name="djangocms-fil-bootstrap",
    packages=find_packages(),
    include_package_data=True,
    version=djangocms_fil_bootstrap.__version__,
    description=djangocms_fil_bootstrap.__doc__,
    long_description=open("README.md").read(),
    classifiers=[
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
    ],
    install_requires=INSTALL_REQUIREMENTS,
    test_suite="test_settings.run",
    author="Fidelity International",
    url="http://github.com/FidelityInternational/djangocms-fil-bootstrap",
    license="BSD",
    dependency_links=[
        "http://github.com/divio/django-cms/tarball/release/4.0.x#egg=django-cms-4.0.0",
    ]
)
