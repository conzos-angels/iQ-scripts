'''
Set camera rotation and flip for all iQ3 protocols.

Summary:

This is needed to fix the protcol importer not importing the camera
orientation settings that are stored in iQ2 protocols.  The script
matches the camera serial number to the expected orientation, so the
name of the camera in the "Camera Selection" tab is not important.

Usage:

Edit the values of 'User variables' as needed.  After the script has
been successfully run once for a specific system, only the
'configuration' value would likely need to be changed for subsequent
runs.
'''

#-----------------------------------------------------------------------
# User variables.
#-----------------------------------------------------------------------
# iQ3 Configuration name to change.
configuration = 'Haibing'

# If apply_changes is set to True, files are changed on disk. If set
# to False, one can read the script output to see what changes will be
# made without applying.  Note Python's boolean capitalization is case
# sensitive; i.e. set "True", not "true".
apply_changes = False

# Dictionaty of settings for each camera. The parent key is the camera
# serial number.  Allowed values for the child values are listed in
# OPTION_FLIP and OPTION_ROTATION.
cameras = {
    5872: {                    # Confocal iXon3
        'flip': 'Flip Horizontal',
        'rotation': 'Rotation 180 degrees'
        },

    5877: {                    # TIRF iXon3
        'flip': 'Flip Horizontal',
        'rotation': 'Rotation 180 degrees'
        },

    1855: {                    # Confocal Clara
        'flip': 'Flip Horizontal',
        'rotation': 'Rotation 90 degrees anti-clockwise'
        },
    }

#-----------------------------------------------------------------------
# Script constants.
#-----------------------------------------------------------------------
PROGRAMDATA_FOLDER = 'Kinetic Imaging'
IQ_VERSION = '3'
EXT = 'KI_LZEXP'
## iQ LZEXP INI file options.
OPTION_SERIAL = 'Camera Serial Number'
OPTION_FLIP = [
    'Flip None',
    'Flip Vertical'
    'Flip Horizontal'
    ]
OPTION_ROTATION = [
    'Rotation None',
    'Rotation 90 degrees',
    'Rotation 90 degrees anti-clockwise',
    'Rotation 180 degrees'
    ]

#-----------------------------------------------------------------------
# Main script.
#-----------------------------------------------------------------------
import configparser
import os
from pathlib import Path

if __name__ == '__main__':

    # Find all the files to modify.
    cfg_path = os.path.join(
        os.getenv('PROGRAMDATA'),
        PROGRAMDATA_FOLDER,
        'iQ' + IQ_VERSION,
        configuration
        )
    print('Checking path exists: {0} ... '.format(cfg_path), end='')
    if not os.path.exists(cfg_path):
        raise IOError ('Could not find {0}'.format(cfg_path))
    print('OK')
    print('Checking for protocols ... ', end='')
    # Don't use os.chdir() because it interferes with ipython.
    files = sorted(Path(cfg_path).glob('*.{0}'.format(EXT)))
    print('{0} found'.format(len(files)))

    # Print settings that would be changed.
    print('Settings to be changed:')
    for f in files:
        config = configparser.ConfigParser()
        config.read(str(f))
        sections = config.sections()
        changes_made = False
        for section in sections:
            # Check if the section has a serial number.
            if OPTION_SERIAL in config[section]:
                serial = config[section][OPTION_SERIAL]
                # Find which of the flip/rotation options are there.
                for option in OPTION_FLIP + OPTION_ROTATION:
                    if option in config[section]:
                        # Advise the modification to be made.
                        camera = cameras[int(serial)]
                        camera_option = option.lower().split()[0]
                        new_option = camera[camera_option]
                        if camera[camera_option] != option:
                            changes_made = True
                            print('  {fname}: {serial}: '.format(
                                    fname=f.name,
                                    serial=serial),
                                  end='')
                            print('{0} -> {1}'.format(option, new_option))
                            # Make the modification.  Note it's not
                            # applied till the file is saved.
                            config.remove_option(section, option)
                            config[section][option] = '1'
        if apply_changes:
            with open(str(f), 'w') as configfile:
                config.write(configfile)
