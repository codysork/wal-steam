#!/usr/bin/env python3
"""
wal_steam (Cody's fork)
Copyright (C) 2019 Dakota Walsh
Maintained by Cody Sork
"""

# Disable pylint warnings
# -------------------------
# pylint: disable-msg=C0103

import shutil  # copying files
import os  # getting paths
import urllib.request  # downloading the zip files
import zipfile  # extracting the zip files
import sys
import argparse  # argument parsing
import textwrap
import time
import re
from argparse import RawTextHelpFormatter

# HOME_DIR should be crossplatform
HOME_DIR = os.getenv("HOME", os.getenv("USERPROFILE"))
CACHE_DIR = os.path.join(HOME_DIR, ".cache", "wal_steam")
CONFIG_DIR = os.path.join(HOME_DIR, ".config", "wal_steam")
SKIN_NAME = "metro-wal-mod"
VERSION = "0.1.1"
CONFIG_FILE = "wal_steam.conf"
COLORS_FILE = os.path.join(CACHE_DIR, "custom.styles")
CONFIG_URL = ("https://raw.githubusercontent.com/kotajacob/" +
              "wal_steam_config/master/wal_steam.conf")

STEAM_DIR_OTHER = os.path.expanduser("~/.steam/steam/skins")
STEAM_DIR_OSX = os.path.expanduser(
    "~/Library/Application Support/Steam/" +
    "Steam.AppBundle/Steam/Contents/MacOS/skins")
STEAM_DIR_UBUNTU = os.path.expanduser("~/.steam/skins")
STEAM_DIR_WINDOWS = r"C:\Program Files (x86)\Steam\skins"
WAL_COLORS = os.path.join(HOME_DIR, ".cache", "wal", "colors.css")
WPG_COLORS = os.path.join(HOME_DIR, ".config", "wpg", "formats", "colors.css")

METRO_URL = ("https://github.com/minischetti/metro-for-steam/" +
             "archive/v4.4.zip")
METRO_ZIP = os.path.join(CACHE_DIR, "metro-for-steam-4.4.zip")
METRO_DIR = os.path.join(CACHE_DIR, "metro-for-steam-4.4")
METRO_COLORS_FILE = os.path.join(METRO_DIR, "custom.styles")

# A link to the version we've tested rather than the latest, just in
# case they break things upstream.
METRO_PATCH_URL = ("https://github.com/redsigma/UPMetroSkin/archive/" +
                   "e43f55b43f8ae565e162da664887051a1c76c5b4.zip")
METRO_PATCH_ZIP = os.path.join(CACHE_DIR, "metroPatchZip.zip")
METRO_PATCH_DIR = os.path.join(CACHE_DIR, "metroPatchZip")
METRO_PATCH_COPY = os.path.join(
    METRO_PATCH_DIR, "UPMetroSkin-e43f55b43f8ae565e162da664887051a1c76c5b4",
    "Unofficial 4.3.1 Patch", "Main Files [Install First]")
METRO_PATCH_HDPI = os.path.join(
    METRO_PATCH_DIR, "UPMetroSkin-e43f55b43f8ae565e162da664887051a1c76c5b4",
    "Unofficial 4.3.1 Patch", "Extras", "High DPI", "Increased fonts",
    "Install")
MAX_PATCH_DL_ATTEMPTS = 5

# CLI colour and style sequences
CLI_RED = "\033[91m"
CLI_YELLOW = "\033[93m"
CLI_BOLD = "\033[1m"
CLI_END = "\033[0m"


def to_string(rgb_tuple):
    """Convert a tupple (rgb color) to a string ready to print"""
    tmp = ' '.join(map(str, rgb_tuple))
    return tmp


# TODO: Reduce the number of variables passed to set_custom_styles by
#       creating a data structure for the style variables
# pylint: disable-msg=R0913
def set_custom_styles(_colors, variables, _wal_colors, _alpha,
                      steam_dir, _fonts):
    """ Patch custom.styles with wal colors and copy to the steam skins
    directory. """
    print("Patching new colors")

    # delete the old colors file if present in cache
    try:
        # just in case it was already there for some reason
        os.remove(COLORS_FILE)
    except FileNotFoundError:
        print("No file to remove")

    with open(METRO_COLORS_FILE) as f:
        custom_styles = f.read()

    patches = []
    ii = 0
    for ii, i in enumerate(variables):
        patches.append('{}="{} {}"'.format(
            i, to_string(_colors[int(_wal_colors[ii])]), _alpha[ii]))

    _wal_styles = "\n".join(patches)
    custom_styles = custom_styles.replace("}\n\nstyles{",
                                          _wal_styles + "}\n\nstyles{")

    if fonts:
        custom_styles = replace_fonts(custom_styles, _fonts)

    with open(COLORS_FILE, "w") as f:
        f.write(custom_styles)

    # now copy it to the proper place based on the os
    shutil.copy(COLORS_FILE, os.path.join(steam_dir, SKIN_NAME))

    # cleanup by removing generated color files
    os.remove(COLORS_FILE)
    print("Wal colors are now patched and ready to go\n"
          "If this is your first run you may have to\n"
          "enable Metro Wal Mod skin in steam then\n"
          "simply restart steam!")


def replace_fonts(styles, _fonts):
    """Patch fonts in custom.styles file"""
    print("Patching custom fonts")

    # attempt to replace font styles with regular expressions
    matches = {
        "^basefont=\"(.+?)\"": "basefont=\"" + _fonts[0] + "\"",
        "^semibold=\"(.+?)\"": "semibold=\"" + _fonts[1] + "\"",
        "^semilight=\"(.+?)\"": "semilight=\"" + _fonts[2] + "\"",
        "^light=\"(.+?)\"": "light=\"" + _fonts[3] + "\"",
    }

    for pattern, replacement in matches.items():
        styles = re.sub(pattern, replacement, styles, 0, re.M)

    return styles


###################
# color functions #
###################
def get_config_alpha():
    """read the config file and return a dictionary of the variables
    and color variables"""
    with open(os.path.join(CONFIG_DIR, CONFIG_FILE)) as f:
        # save the lines of the config file to rawFile
        rawFile = f.readlines()

    # loop through rawFile
    result = []
    for line in rawFile:
        tmpResult = line[line.find(",") + 1:line.find("\n")]
        result.append(tmpResult)
    return result


def get_config_colors():
    """read the config file and return a dictionary of the variables
    and color variables"""
    with open(os.path.join(CONFIG_DIR, CONFIG_FILE)) as f:
        # save the lines of the config file to rawFile
        rawFile = f.readlines()

    # loop through rawFile
    result = []
    for line in rawFile:
        tmpResult = line[line.find("=") + 1:line.find(",")]
        result.append(tmpResult)
    return result


def get_config_var():
    """read the config file and return a dictionary of the variables and color variables"""
    with open(os.path.join(CONFIG_DIR, CONFIG_FILE)) as f:
        # save the lines of the config file to rawFile
        rawFile = f.readlines()

    # loop through rawFile
    result = []
    for line in rawFile:
        tmpResult = line[:line.find("=")]
        result.append(tmpResult)
    f.close()
    return result


def hex_to_rgb(hexColors):
    """Convert hex colors to rgb colors (takes a list)."""
    return [tuple(bytes.fromhex(color.strip("#"))) for color in hexColors]


def get_colors(_mode):
    """ Parse the specied wallpaper colors file and return a list of
    color hex codes"""
    if _mode == 0:
        # using colors from wal
        colorsFile = WAL_COLORS
    else:
        # using colors from wpg
        colorsFile = WPG_COLORS
    # parse the file
    print("Reading colors")
    # try:
    with open(colorsFile) as f:
        rawFile = f.readlines()  # save the lines to rawFile
    # TODO: Specific exception
    # except:
    #     print("Error: Colors file missing. Make sure you've run" +
    #           "pywal/wpg before wal_steam")
    #     sys.exit(1)

    # delete the lines not involving the colors
    del rawFile[0:11]
    del rawFile[16]

    # loop through rawFile and store colors in a list
    _colors = []
    for line in rawFile:
        # delete everything but the hex code
        tmp = line[line.find("#"):]
        tmp = tmp[:7]

        # append the hex code to the colors list
        _colors.append(tmp)

    return _colors


##########################
# checkInstall functions #
##########################


def check_skin(steam_dir, _dpi):
    """Check for skin and patch in cache"""
    if not (os.path.isdir(METRO_DIR) and os.path.isdir(METRO_PATCH_COPY)):
        # metro skin and patch not found in cache, download and make
        make_skin()
    # check for patched skin in steam skin directory
    if not os.path.isdir(os.path.join(steam_dir, SKIN_NAME)):
        # patched skin not found in steam, copy it over
        print("Installing skin")
        try:
            shutil.copytree(METRO_DIR, os.path.join(steam_dir, SKIN_NAME),
                            symlinks=False, ignore=None,
                            copy_function=shutil.copy,
                            ignore_dangling_symlinks=False, dirs_exist_ok=True)
        except FileExistsError:
            pass
    else:
        print("Wal Steam skin found")
        if _dpi == 1:
            # skin was not found, copy it over
            print("Forcing skin install for High DPI patches")
            shutil.copytree(METRO_DIR, os.path.join(steam_dir, SKIN_NAME),
                            symlinks=False, ignore=None,
                            copy_function=shutil.copy,
                            ignore_dangling_symlinks=False, dirs_exist_ok=True)

def download_zip(url, _zip, attempts=5):
    """Download a zip file from the specified url"""
    if attempts == 0:
        print("HTTP 400 error. Please check your connection and try again.")
        sys.exit(1)
    else:
        try:
            opener = urllib.request.build_opener()
            opener.addheaders = [{'User-Agent', 'Mozilla/5.0'}]
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve(url, _zip)
        except urllib.error.HTTPError:
            download_zip(url, _zip, attempts - 1)


def make_skin():
    """Download metro for steam and extract"""
    print("Downloading Metro for steam")
    download_zip(METRO_URL, METRO_ZIP)

    with zipfile.ZipFile(METRO_ZIP, 'r') as z:
        z.extractall(CACHE_DIR)

    # download metro for steam patch and extract
    print("Attempting to download Metro patch")
    patch_dl_attempts = 0
    patch_dld = False
    while (patch_dl_attempts < MAX_PATCH_DL_ATTEMPTS) and not patch_dld:
        try:
            opener = urllib.request.build_opener()
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve(METRO_PATCH_URL, METRO_PATCH_ZIP)
            patch_dld = True
        except:
            patch_dl_attempts += 1
            print("Error: download attempt " + str(patch_dl_attempts) + " failed.")
            if patch_dl_attempts < MAX_PATCH_DL_ATTEMPTS:
                time.sleep(5)

    if not patch_dld:
        print("Error: patch download attempts failed, exiting...")
        sys.exit(1)
    else:
        print("Patch downloaded, proceeding...")

    with zipfile.ZipFile(METRO_PATCH_ZIP, 'r') as z:
        z.extractall(METRO_PATCH_DIR)

    # finally apply the patch
    shutil.copytree(METRO_PATCH_COPY, METRO_DIR,
                    symlinks=False, ignore=None,
                    copy_function=shutil.copy,
                    ignore_dangling_symlinks=False, dirs_exist_ok=True)

def make_config():
    """Download the config for wal_steam"""
    print("Downloading config file")
    try:
        urllib.request.urlretrieve(CONFIG_URL,
                                   os.path.join(CONFIG_DIR, CONFIG_FILE))
    except urllib.error.HTTPError:
        make_config() # Try download again


def make_dpi():
    """Apply the high dpi"""
    print("Applying the high dpi patches")
    shutil.copytree(METRO_PATCH_HDPI, METRO_DIR)


def del_config():
    """Delete the config"""
    if os.path.isdir(CONFIG_DIR):
        shutil.rmtree(CONFIG_DIR)


def del_cache():
    # delete the cache
    if os.path.isdir(CACHE_DIR):
        shutil.rmtree(CACHE_DIR)


def del_skin(steam_dir):
    """Delete the skin"""
    if os.path.isdir(os.path.join(steam_dir, SKIN_NAME)):
        shutil.rmtree(os.path.join(steam_dir, SKIN_NAME))


def check_config():
    """Check for the config"""
    if not os.path.isdir(os.path.join(HOME_DIR, ".config")):
        # make the .config folder
        os.mkdir(os.path.join(HOME_DIR, ".config"))
    if not os.path.isdir(CONFIG_DIR):
        # make the config directory
        os.mkdir(CONFIG_DIR)

        # download or make config file
        make_config()
    elif not os.path.isfile(os.path.join(CONFIG_DIR, CONFIG_FILE)):
        # download or make the config file
        make_config()
    else:
        # config file found!
        print("Wal Steam config found")


def check_cache(_dpi):
    """Check for the cache"""
    if not os.path.isdir(os.path.join(HOME_DIR, ".cache")):
        # make the .cache folder
        os.mkdir(os.path.join(HOME_DIR, ".cache"))
    if not os.path.isdir(CACHE_DIR):
        # make the cache directory
        os.mkdir(CACHE_DIR)

        # download, extract, and patch metro for steam
        make_skin()

        # apply the dpi patches
        if _dpi == 1:
            make_dpi()
    else:
        # cache folder exists
        print("Wal Steam cache found")

        # apply the dpi patches
        if _dpi == 1:
            make_dpi()


def check_install(_o_sys, _dpi):
    """Check if the cache and config file exist and if the skin is installed."""
    # check if the cache exists, make it if not
    check_cache(_dpi)

    # check if the config file exists
    check_config()

    # check if the skin is installed, install it if not
    check_skin(_o_sys, _dpi)


def force_update(_o_sys, _dpi):
    """force update the cache and config files"""
    del_config()
    del_cache()
    del_skin(_o_sys)
    check_cache(_dpi)
    check_config()


def get_os():
    """Check for steam directory"""
    # check if ~/.steam/steam/skins exists
    if os.path.isdir(STEAM_DIR_OTHER):
        steam_dir = STEAM_DIR_OTHER
    # check if ~/.steam/skins exists
    elif os.path.isdir(STEAM_DIR_UBUNTU):
        steam_dir = STEAM_DIR_UBUNTU
    # check if C:\Program Files (x86)\Steam\skins exists
    elif os.path.isdir(STEAM_DIR_WINDOWS):
        steam_dir = STEAM_DIR_WINDOWS
    elif os.path.isdir(STEAM_DIR_OSX):
        steam_dir = STEAM_DIR_OSX # close with error message otherwise
    else:
        print("Error: Steam install not found!")
        sys.exit(1)

    return steam_dir

# TODO: Write a better docstring
def parse_font_args(raw_args):
    """?"""
    split_args = [arg.strip() for arg in raw_args.split(",")]

    if len(split_args) != 4:
        print("Error: You must specify all four custom font styles.")
        sys.exit(1)

    return split_args


def get_args():
    """Get the arguments with argparse"""
    description = "Wal Steam"
    arg = argparse.ArgumentParser(description=description,
                                  formatter_class=RawTextHelpFormatter)

    arg.add_argument("-v",
                     "--version",
                     action="store_true",
                     help="Print wal_steam version.")

    arg.add_argument("-w", action="store_true", help="Get colors from wal.")

    arg.add_argument("-g", action="store_true", help="Get colors from wpg.")

    arg.add_argument("-s", help="Enter a custom steam skin directory.")

    arg.add_argument("-d", action="store_true", help="Apply high dpi patches.")

    arg.add_argument("-u",
                     action="store_true",
                     help=f"Force update cache, skin, and config file. " +
                     "{CLI_RED}WARNING:{CLI_END} WILL OVERWRITE config.json")

    arg.add_argument("-f",
                     "--fonts",
                     help=textwrap.dedent(f'''
            Specify custom fonts. Enter font styles separated by comma.
            {CLI_BOLD}Available styles:{CLI_END} basefont, semibold, semilight, light.
            {CLI_YELLOW}Example:{CLI_END} 'Open Sans, Open Sans Semibold, Open Sans Semilight, Open Sans Light'
            {CLI_RED}WARNING:{CLI_END} Fonts must already be installed on your system.'''
                                          ))

    arg.add_argument(
        "-a",
        "--attempts",
        help="Set the number of patch download attempts (DEFAULT=5)")

    return arg.parse_args()


if __name__ == '__main__':
    # set default mode to wal
    # 0 = wal
    # 1 = wpgtk
    mode = 0

    # parse the arguments
    arguments = get_args()
    if arguments.version:
        print("Wal Steam", VERSION)
        sys.exit()

    # make sure they didn't select both wal and wpg
    if arguments.w and arguments.g:
        print("Error: You must select wpg or wal")
        sys.exit(1)

    # set the mode for either wal or wpg
    if arguments.w:
        mode = 0
    if arguments.g:
        mode = 1

    # check if user wants high-dpi support
    if arguments.d:
        dpi = 1
    if not arguments.d:
        dpi = 0

    # allow the user to enter a custom steam install location
    if arguments.s:
        o_sys = arguments.s
        print("Using custom skin path: {}".format(arguments.s))
    else:
        # check where the os installed steam
        # ~/.steam/steam/skins               - common linux install location
        # ~/.steam/skins                     - used on ubuntu and its derivatives
        # C:\Program Files (x86)\Steam\skins - used on windows
        o_sys = get_os()

    # allow the user to enter custom font styles
    if arguments.fonts:
        fonts = parse_font_args(arguments.fonts)
        print("Using custom font styles: {}".format(arguments.fonts))
    else:
        fonts = ""

    # update the cache and config then exit
    if arguments.u:
        print("Force updating cache and config")
        # first remove the cache and config
        force_update(o_sys, dpi)
        print("Cache and config updated")
        print("Run with -w or -g to apply and re-enable wal_steam")
        sys.exit()

    if arguments.attempts:
        # try:
        attempts_bound = int(arguments.attempts)
        MAX_PATCH_DL_ATTEMPTS = attempts_bound
        # except:
        #   print(
        #       "Error setting maximum patch download attempts, using default (5)."
        #   )

    # check for the cache, the skin, and get them if needed
    check_install(o_sys, dpi)

    # get a list from either wal or wpg based on the mode
    colors = get_colors(mode)

    # convert our list of colors from hex to rgb
    colors = hex_to_rgb(colors)

    # get a dictionary of the config settings from the config file
    config_file_variables = get_config_var()
    wal_colors = get_config_colors()
    alpha = get_config_alpha()

    # finally create a temp colors.styles and copy it in updating the skin
    # set_custom_styles(colors, config_file_variables, wal_colors,
                      # alpha, o_sys, fonts)
