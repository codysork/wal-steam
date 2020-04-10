"""wal_steam - setup.py"""
import setuptools

try:
    import wal_steam
except (ImportError):
    print("error: wal_steam requires Python 3.5 or greater.")
    quit(1)

VERSION = wal_steam.VERSION
DOWNLOAD = "https://github.com/codysork/wal_steam/archive/%s.tar.gz" % VERSION

setuptools.setup(
    name="wal_steam",
    version=VERSION,
    author="Cody Sork",
    author_email="codysork@pm.me",
    description="A fork of Dakota Walsh's original wal_steam script.",
    license="MIT",
    url="https://github.com/codysork/wal_steam",
    download_url=DOWNLOAD,
    classifiers=[
        "Environment :: X11 Applications",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    install_requires="pywal >= 0.6.7",
    scripts=['wal_steam.py'],
    entry_points={
        "console_scripts": ["wal-steam=wal_steam:main"]
    },
    python_requires=">=3.5",
    include_package_data=True
)
