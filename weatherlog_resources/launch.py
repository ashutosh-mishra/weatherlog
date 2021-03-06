# -*- coding: utf-8 -*-


# This file defines the functions for launching and setting up the application.


# Import json for loading and saving the data.
import json
# Import platform for getting the user's operating system.
import platform
# Import os for creating a directory and other tasks.
import os
# Import os.path for seeing if a directory exists and other tasks.
import os.path
# Import sys for closing the application.
import sys
# Import glob for getting a list of directories.
import glob
# Import datetime for getting the current time.
import datetime
# Import pickle for loading and saving the data.
try:
    import cPickle as pickle
except ImportError:
    import pickle


# Yahoo! Weather condition codes.
codes = {"0":    "Tornado",
         "1":    "Tropical storm",
         "2":    "Hurricane",
         "3":    "Severe thunderstorms",
         "4":    "Thunderstorms",
         "5":    "Mixed rain and snow",
         "6":    "Mixed rain and sleet",
         "7":    "Mixed snow and sleet",
         "8":    "Freezing drizzle",
         "9":    "Drizzle",
         "10":   "Freezing rain",
         "11":   "Showers",
         "12":   "Showers",
         "13":   "Snow flurries",
         "14":   "Light snow showers",
         "15":   "Blowing snow",
         "16":   "Snow",
         "17":   "Hail",
         "18":   "Sleet",
         "19":   "Dust",
         "20":   "Foggy",
         "21":   "Haze",
         "22":   "Smoky",
         "23":   "Blustery",
         "24":   "Windy",
         "25":   "Cold",
         "26":   "Cloudy",
         "27":   "Mostly cloudy (night)",
         "28":   "Mostly cloudy (day)",
         "29":   "Partly cloudy (night)",
         "30":   "Partly cloudy (day)",
         "31":   "Clear (night)",
         "32":   "Sunny",
         "33":   "Fair (night)",
         "34":   "Fair (day)",
         "35":   "Mixed rain and hail",
         "36":   "Hot",
         "37":   "Isolated thunderstorms",
         "38":   "Scattered thunderstorms",
         "39":   "Scattered thunderstorms",
         "40":   "Scattered showers",
         "41":   "Heavy snow",
         "42":   "Scattered snow showers",
         "43":   "Heavy snow",
         "44":   "Partly cloudy",
         "45":   "Thundershowers",
         "46":   "Snow showers",
         "47":   "Isolated thundershowers",
         "3200": "Not available"}


def get_main_dir():
    """Returns the main directory."""
    
    # The main directory is C:\.weatherlog on Windows,
    # and /home/[username]/.share/local/weatherlog for data files,
    # and /home/[username]/.config/weatherlog/ for configuration files on Linux.
    if platform.system().lower() == "windows":
        return "C:\\.weatherlog", "C:\\.weatherlog"
    else:
        base = os.path.expanduser("~")
        return base + "/.local/share/weatherlog", base + "/.config/weatherlog"


def get_ui_info():
    """Get the application's UI info."""
    
    version = "4.0"
    title = "WeatherLog"
    menu_file = open("weatherlog_resources/menu.xml", "r")
    menu_data = menu_file.read()
    menu_file.close()
    icon_small = "weatherlog_resources/images/icon_small.png"
    icon_medium = "weatherlog_resources/images/icon_med.png"
    icon_medium_about = "../images/icon_med.png"
    return version, title, menu_data, icon_small, icon_medium


def check_files_exist(main_dir, conf_dir):
    """Checks to see if the base files exist, and create them if they don't."""
    
    # Check to see if the data directory exists, and create it if it doesn't.
    if not os.path.exists(main_dir) or not os.path.isdir(main_dir):
        
        # Create the default data directory and files.
        os.makedirs(main_dir)
        os.makedirs("%s/profiles/Main Dataset" % main_dir)
        last_prof_data = open("%s/profiles/Main Dataset/weather" % main_dir, "w")
        pickle.dump([], last_prof_data)
        last_prof_data.close()
        create_metadata(main_dir, "Main Dataset")
    
    # Check to see if the configuration directory exists, and create it if it doesn't.
    if not os.path.exists(conf_dir) or not os.path.isdir(conf_dir):
        
        # Create the default configuration directory and files.
        os.makedirs(conf_dir)
        last_prof = open("%s/lastprofile" % conf_dir, "w")
        last_prof.write("Main Dataset")
        last_prof.close()


def get_last_profile(main_dir, conf_dir):
    """Returns the last profile, the original profile to be loaded, and whether the profile exists. Creates the profile if it doesn't exist."""
    
    try:
        # Load the last profile file.
        prof_file = open("%s/lastprofile" % conf_dir, "r")
        last_profile = prof_file.read().rstrip()
        prof_file.close()
        
        # Check to make sure the profile exists:
        # Remember the currect directory and switch to where the profiles are stored.
        current_dir = os.getcwd()
        os.chdir("%s/profiles" % main_dir)
        
        # Get the list of profiles.
        profiles_list = glob.glob("*")
        
        # Switch back to the previous directory.
        os.chdir(current_dir)
        
        # Check if the profile exists:
        if last_profile in profiles_list:
            profile_exists = True
            original_profile = ""
        else:
            profile_exists = False
            original_profile = last_profile
    
    except IOError:
        print("Error reading dataset file (IOError).")
        sys.exit()
    
    # If the profile doesn't exist, switch or make one that does:
    if not profile_exists:
        
        # If the default profile exists, switch to that.
        if "Main Dataset" in profiles_list:
            last_profile = "Main Dataset"
        
        # Otherwise, create the profile:
        else:
            
            # Create the Main Dataset directory and data file.
            os.makedirs("%s/profiles/Main Dataset" % main_dir)
            last_prof_data = open("%s/profiles/Main Dataset/weather" % main_dir, "w")
            pickle.dump([], last_prof_data)
            last_prof_data.close()
            
            # Set the profile name.
            last_profile = "Main Dataset"
    
    return last_profile, original_profile, profile_exists


def get_config(conf_dir):
    """Loads the settings."""
    
    # Get the configuration.
    try:
        config_file = open("%s/config" % conf_dir, "r")
        config = json.load(config_file)
        config_file.close()
    
    except IOError:
        # If there was an error, use the defaults instead.
        config = {"pre-fill": False,
                  "restore": True,
                  "location": "",
                  "units": "metric",
                  "pastebin": "d2314ff616133e54f728918b8af1500e",
                  "show_units": True,
                  "show_dates": True,
                  "confirm_del": True,
                  "show_pre-fill": True,
                  "confirm_exit": False,
                  "import_all": False,
                  "truncate_notes": True,
                  "graph_color": "#0000FF",
                  "line_width": 1,
                  "line_style": "Solid",
                  "hatch_style": "Solid"}
    
    return config


def get_window_size(conf_dir, config):
    """Gets the last window size."""
    
    # If the user doesn't want to restore the window size, set the size to the defaults.
    if not config["restore"]:
        last_width = 900
        last_height = 500
    
    # Otherwise, get the previous window size.
    else:
        
        try:
            wins_file = open("%s/window_size" % conf_dir, "r")
            last_width = int(wins_file.readline())
            last_height = int(wins_file.readline())
            wins_file.close()
        
        except IOError:
            # If there was an error, use the default size instead.
            last_width = 900
            last_height = 500
    
    return last_width, last_height


def get_units(config):
    """Gets the units."""
    
    # Configure the units.
    # Metric:
    if config["units"] == "metric":
        
        # Temperature is Celsius.
        # Precipitation is centimeters.
        # Wind speed is kilometers per hour.
        # Air pressure is hecto-pascals.
        units = {"temp": "°C",
                 "prec": "cm",
                 "wind": "kph",
                 "airp": "hPa",
                 "visi": "km"}
    
    # Imperial:
    elif config["units"] == "imperial":
        
        # Temperature is Fahrenheit.
        # Precipitation is inches.
        # Wind speed is miles per hour
        # Air pressure is millibars.
        units = {"temp": "°F",
                 "prec": "in",
                 "wind": "mph",
                 "airp": "mbar",
                 "visi": "mi"}
    
    return units


def get_data(main_dir, last_profile):
    """Gets the data."""
    
    try:
        # Load the data.
        data_file = open("%s/profiles/%s/weather" % (main_dir, last_profile), "r")
        data = pickle.load(data_file)
        data_file.close()
        
    except IOError:
        print("Error importing data (IOError).")
        sys.exit()
        
    except (TypeError, ValueError):
        print("Error importing data (TypeError or ValueError).")
        sys.exit()
    
    return data


def create_metadata(main_dir, last_profile):
    """Creates the default metadata file."""
    
    # Get the current time.
    now = datetime.datetime.now()
    modified = "%d/%d/%d" % (now.day, now.month, now.year)
    
    # Write the metadata to the file.
    try:
        meta_file = open("%s/profiles/%s/metadata" % (main_dir, last_profile), "w")
        meta_file.write("%s\n%s" % (modified, modified))
        meta_file.close()
    
    except IOError:
        print("Error saving metadata file (IOError).")
