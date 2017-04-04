"""
Program for process config file.
"""
import os
import time
import shutil
import subprocess
import ConfigParser

def process_config(config_file):
    """
    Perform operations from config_file
    Config file has sections and each section has
    "Action", perform that action on section parameters.
    """

    config = ConfigParser.RawConfigParser()

    config.read(config_file)

    # Get to each section to perform operation.
    for section in config.sections():

        # Exit loop if reach to END section
        if section == "END":
            break
        action = config.get(section, "Action")

        # Copy the file, if not exist, if not set for overwrite, dont copy
        if action == "copy" and \
                (not os.path.exists(config.get(section, "Destfile")) or
                 config.get(section, "Overwrite") == "y"):
            try:
                shutil.copy(config.get(section, "Srcfile"),
                            config.get(section, "Destfile"))
            except IOError as ex:
                print "Error: unable to copy file"
                print ex.args[1]
        else:
            try:
                # Run program given in config file
                program = subprocess.Popen([config.get(section, "Program")])
                (_, stderrdata) = program.communicate()
                if stderrdata:
                    print "Error: Got error " + stderrdata
            except OSError:
                print "Error: Something wrong, check program."
            except ValueError:
                print "Error: Can't run program with these arguments."

        print config.get(section, "Message")

        # Wait before ask question.
        if config.has_option(section, "Wait"):
            time.sleep(int(config.get(section, "Wait")))

        user_input = "n"

        while user_input.lower() == "n":
            user_input = raw_input("Continue (Y/N)?")


if __name__ == "__main__":
    process_config("config.txt")
