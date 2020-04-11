"""wal-steam - setup.py"""
import setuptools

try:
    import wal_steam
except (ImportError):
    print("error: wal-steam requires Python 3.5 or greater.")
    quit(1)

VERSION = wal_steam.VERSION
DOWNLOAD = "https://github.com/codysork/wal_steam/archive/%s.tar.gz" % VERSION

setuptools.setup(
    name="wal-steam-codys-fork",
    version=VERSION,
    author="Cody Sork",
    author_email="codysork@pm.me",
    description="""A fork of Dakota Walsh's original wal_steam script.
    Copyright (C) 2019 Dakota Walsh""",
    license="MIT",
    url="https://github.com/codysork/wal-steam",
    download_url=DOWNLOAD,
    classifiers=[
        "Environment :: X11 Applications",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    install_requires="pywal >= 0.6.7",
    scripts=['wal-steam.py'],
    entry_points={
        "console_scripts": ["wal-steam=wal-steam:main"]
    },
    python_requires=">=3.5",
    include_package_data=True
)
