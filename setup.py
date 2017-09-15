# -*- coding: utf-8 -*-

from setuptools import setup
from messente.verigator import __version__ as version

setup(
    name="verigator",
    version=version,
    packages=["messente", "messente.verigator"],
    setup_requires=["requests", "requests-mock", "mock"],
    install_requires=["requests", "requests-mock", "mock"],
    author="Verigator.com",
    author_email="admin@verigator.com",
    description="Official Verigator.com API library",
    license="Apache License, Version 2",
    keywords="verigator messente sms verification 2FA pincode",
    url="http://messente.com/documentation/",
    test_suite="test"
)
