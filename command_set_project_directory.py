import os
import sublime
import sublime_plugin

from FuzzyFilePath.common.config import config
from FuzzyFilePath.project.validate import Validate

"""
    DO:
        trigger update settings, cached CurrentFiles
"""

project_base_directory = ""

class FfpSetProjectDirectoryCommand(sublime_plugin.TextCommand):
    """ opens dialog to change current project directory """

    def run(self, edit):
        global project_base_directory

        directory = Validate.view(self.view, config)
        if directory is False:
            # validates adjusted project directory which may become annoying since project is still valid
            return sublime.status_message("FuzzyFilePath: Abort. Current file is not within a project")

        project_base_directory = directory["base"]
        ffp_settings = get_ffp_project_settings();
        project_directory = ffp_settings.get("project_directory", "")
        sublime.active_window().show_input_panel(
            "FuzzyFilePath: change project directory to a sub directory",
            project_directory,
            changeDirectoryDone,
            changeDirectoryChange,
            changeDirectoryCancel
        )

def get_ffp_project_settings():
    project = sublime.active_window().project_data();
    if project.get("settings") is None:
        project["settings"] = {}

    ffpSettings = project.get("settings").get("FuzzyFilePath")

    if ffpSettings is None:
        ffpSettings = {}
        project.get("settings")["FuzzyFilePath"] = ffpSettings

    sublime.active_window().set_project_data(project)
    return ffpSettings

def changeDirectoryDone(text):
    project = sublime.active_window().project_data();
    ffp_settings = project.get("settings").get("FuzzyFilePath")
    ffp_settings["project_directory"] = text
    sublime.active_window().set_project_data(project)

def changeDirectoryChange(directory):
    global project_base_directory

    directory = Validate.get_valid_path(directory)
    sub_directory = os.path.join(project_base_directory, directory)
    if os.path.exists(sub_directory) is False:
        sublime.status_message("FuzzyFilePath: this directory is not a subdirectory " + sub_directory)
    else:
        sublime.status_message("FuzzyFilePath: project directory " + sub_directory)

def changeDirectoryCancel():
    return