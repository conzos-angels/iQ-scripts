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
apply_changes = True

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
OPTIONS_FLIP = [
    'Flip None',
    'Flip Vertical'
    'Flip Horizontal'
    ]
OPTIONS_ROTATION = [
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
    any_files_changed = False
    for f in files:
        config = configparser.RawConfigParser()    # To use optionxform.
        config.optionxform = lambda option: option # Don't change case.
        config.read(str(f))
        sections = config.sections()
        file_changed = False
        for section in sections:
            section_changed = False
            # Check if the section has a serial number.
            if OPTION_SERIAL in config[section]:
                serial = config[section][OPTION_SERIAL]
                # Find which of the flip/rotation options are there.
                for option in OPTIONS_FLIP + OPTIONS_ROTATION:
                    if option in config[section]:
                        # Advise the modification to be made.
                        camera = cameras[int(serial)]
                        key = option.lower().split()[0]
                        new_option = camera[key]
                        if camera[key] != option:
                            if file_changed == False:
                                any_files_changed = True
                                file_changed = True
                                print(f.stem) # Print header.
                            if section_changed == False:
                                section_changed = True
                                print('  {0}'.format(section))
                            print('    {0}: {1} -> {2}'.format(serial, option, new_option))
                            # Make the modification.  Note it's not
                            # applied till the file is saved.
                            config.remove_option(section, option)
                            config[section][new_option] = '1'
                            
        if apply_changes and file_changed:
            print('Updating file {0} ... '.format(f.name), end='')
            with open(str(f), 'w') as configfile:
                config.write(configfile)
            print('OK')
    if any_files_changed == False:
        print('...None.  Camera orientation is consistent with requested orientation.')
