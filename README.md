# `wal-steam`

A little program that themes the colors for Metro for steam from `wal`or `wpg`. This is a fork of the original script by kotajacob, which is no longer actively being maintained.

## Changes in This Fork

- The executable for running this script is now ` wal-steam `, not ` wal_steam `.
- The [community patch](https://steamcommunity.com/groups/metroskin/discussions/0/141136086931804907) is currently disabled in this fork, because it was causing my steam library to fail to display.

## About

`wal-steam` is a tiny program that is meant to work with either `wal` or `wpgtk`, by reading the colors they generate and making a color theme for a slightly tweaked version of Metro for Steam.

[Wal](https://github.com/dylanaraps/pywal) is a little program for linux that creates a terminal color scheme based on your wallpaper (in addition to being able to set the wallpaper and a few other
interesting features).

[Wpgtk](https://github.com/deviantfero/wpgtk) is based on wal, but with the added feature of being able to generate gtk themes with the colors and bring a nice simple ui to wal.

[Metro for steam](http://metroforsteam.com/) is a very nice looking skin for steam. 

## Install

**Note for Windows users:** You're going to need to install [python 3](https://www.python.org/) then [imagemagick](https://www.imagemagick.org/script/download.php) first. Then search for command prompt, right click it and open as administrator, then run the pip command below but without the sudo part.

### Packages

**Python PIP:** Not available yet with pip.

**Arch Linux AUR:** Not available yet in the AUR.

### Manual

**Pre-install:** Make sure [Wal](https://github.com/dylanaraps/pywal) or [Wpgtk](https://github.com/deviantfero/wpgtk) is installed and working.

**Install:** `git clone https://github.com/codysork/wal-steam.git`

**Post-install:** See the "Using" section of this readme.

## Using

**Make sure you've run wal or wpgk at least once to generate the colors and set the wallpaper.**

**Note:** On some distros, notably **Ubuntu** you'll have to run the command python3 instead of python or you'll have an error about failing to import urllib.request. Additionally, OSx users may   need to use the system certificate store (outlined [here](https://stackoverflow.com/questions/41691327/ssl-sslerror-ssl-certificate-verify-failed-certificate-verify-failed-ssl-c)).

If you cloned the repo all you need to do is run the script with python 3 from wherever you downloaded it.

Example:

`wal-steam -w`

```
Usage:
  wal-steam.py (-w | -g | -u) [-d]
  wal-steam.py ( -s ) ["/home/kota/bin/custom_steam_install/skins/"]
  wal-steam.py (-h | --help)
  wal-steam.py (-v | --version)
  wal-steam.py (-f | --fonts) ["Ubuntu, Ubuntu Bold, Ubuntu Medium, Ubuntu Light"]

Options:
  -h --help            show this help message and exit
  -v --version         show version and exit
  -w                   use wal for colors
  -g                   use wpg for colors
  -u                   force update cache and config file
  -d                   apply HiDPI community patch
  -s "/steam/skins"    specify a custom steam skins folder to use
  -f --fonts           specify custom fonts
  -a --attempts        specify the max number of patch download attempts (DEFAULT=5)
```
