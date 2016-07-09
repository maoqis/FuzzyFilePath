import re
import FuzzyFilePath.common.path as Path
from FuzzyFilePath.common.verbose import log
from FuzzyFilePath.common.config import config
from FuzzyFilePath.completion import Completion


class Query:
    """
        Build current query based on received modifiers
    """
    forces = {
        # documentation only, will be removed
        "filepath_type": False,
        "extensions": [],
        "base_directory": "",
        "replace_on_insert": []
    }

    extensions = ["*"]
    base_path = False
    replace_on_insert = []

    def reset():
        print("QUERY RESET")
        Query.extensions = ["*"]
        Query.base_path = False
        Query.replace_on_insert = []
        Query.forces.clear()

    def force(key, value):
        Query.forces[key] = value

    def get(key, default=None):
        return Query.forces.get(key, default)

    def by_command():
        return bool(Query.get("filepath_type", False))

    def get_base_path():
        return Query.base_path

    def get_extensions():
        return Query.extensions

    def get_needle():
        return Query.needle

    def get_replacements():
        return Query.replace_on_insert

    def build(needle, trigger, current_folder):

        query = {}

        print("TRIGGER replace", trigger.get("replace_on_insert"))

        force_type = Query.get("filepath_type", False)
        triggered = Query.by_command()
        filepath_type = "relative"
        needle = Path.sanitize(needle)
        needle_is_absolute = Path.is_absolute(needle)
        needle_is_relative = Path.is_relative(needle)
        needle_is_path = needle_is_absolute or needle_is_relative
        # abort if autocomplete is not available
        if not triggered and trigger.get("auto", False) is False and needle_is_path is False:
            # verbose("FFP no autocomplete")
            return False
        # test path to trigger auto-completion by needle
        if not triggered and trigger["auto"] is False and config["AUTO_TRIGGER"] and needle_is_absolute:
            force_type = "absolute"
        # base_directory: override - trigger - False
        base_directory = trigger.get("base_directory", False)
        base_directory = Query.get("base_directory", base_directory)
        #
        # set current directory by force, else by trigger:
        #
        # trigger       |
        # --------------|--------------------
        # False         | use current file's directory
        # True          | use settings: base_directory
        # String        | use string as base_directory
        # change base folder to base directory
        #
        if base_directory is True:
            current_folder = config["BASE_DIRECTORY"]
        elif base_directory:
            current_folder = Path.sanitize_base_directory(base_directory)
        # notify completion to replace path
        if base_directory and needle_is_absolute:
            Completion.set_base_directory(current_folder)
        #
        # filepath_type
        #
        # needle    | trigger rel   | force     | RESULT
        # ----------|---------------|-----------|---------
        # ?         | relative      | False     | relative
        # ?         | absolute      | False     | absolute
        # absolute  | *             | False     | absolute
        # relative  | *             | False     | relative
        # *         | *             | relative  | relative
        # *         | *             | absolute  | absolute
        #
        if force_type:
            filepath_type = force_type
        elif needle_is_absolute:
            filepath_type = "absolute"
        elif needle_is_relative:
            filepath_type = "relative"
        elif trigger.get("relative") is True:
            filepath_type = "relative"
        elif trigger.get("relative") is False:
            filepath_type = "absolute"

        Query.base_path = current_folder if filepath_type == "relative" else False

        # replacements: override - trigger - None
        Query.replace_on_insert = trigger.get("replace_on_insert", [])
        Query.replace_on_insert = Query.get("replace_on_insert", Query.replace_on_insert)
        # extensions: override - trigger - "js"
        extensions = trigger.get("extensions", ["*"])
        extensions = Query.get("extensions", extensions)
        Query.extensions = extensions
        Query.needle = Query.build_needle_query(needle, current_folder)
        # strip any starting dots or slashes
        Query.needle = re.sub("^[\.\/]*", "", Query.needle)
        # --------------------------------------------------------------------
        # tests throw error if results are set to class
        # Require refactoring of static classes with dynamic properties?
        # --------------------------------------------------------------------
        query["extensions"] = extensions
        query["base_path"] = current_folder if filepath_type == "relative" else False
        query["needle"] = Query.build_needle_query(needle, current_folder)

        if triggered or (config["AUTO_TRIGGER"] if needle_is_path else trigger.get("auto", config["AUTO_TRIGGER"])):
            return query

        return False

    def build_needle_query(needle, current_folder):
        """
            sanitizes requested path and replaces a starting ./ with the current (local) folder
            returns final needle
        """
        current_folder = "" if not current_folder else current_folder
        needle = re.sub("\.\./", "", needle)
        needle = re.sub("[\\n\\t]", "", needle)

        # remove base path from needle
        if Query.base_path and isinstance(current_folder, str) and needle.startswith(current_folder):
            needle = needle[len(Query.base_path):]

        needle = needle.strip()

        if needle.startswith("./"):
            needle = current_folder + re.sub("\.\/", "", needle)

        return needle
