# [FuzzyFilePath](https://github.com/sagold/FuzzyFilePath)

__Sublime Text Plugin__

Fuzzy search and insert filenames inside your current project directory. Highly customizable.

<img src="https://raw.githubusercontent.com/sagold/FuzzyFilePath/develop/FuzzyFilePathDemo.gif" />
<br />
<em style="display: block; text-align: right;">Basic settings support Html, Css and Javascript, but may be adjusted for every language</em>


## <a name="installation">Installation</a>


### [Package Control](https://sublime.wbond.net/)

After [Package Control installation](https://sublime.wbond.net/installation), restart Sublime Text. Use the Command Palette `cmd+shift+p` (OS X) or `ctrl+shift+p` (Linux/Windows) and search for *Package Control: Install Package*. Wait until Package Control downloaded the latest package list and search for *FuzzyFilePath*.


### [github](https://github.com/sagold/FuzzyFilePath.git)

in `<SublimeConfig>/Packages/` call: `git clone https://github.com/sagold/FuzzyFilePath.git`

__Sublime Text 2__

in `<SublimeConfig>/Packages/FuzzyFilePath/` switch to Sublime Text 2 Branch with: `git checkout st2`

Attention: Sublime Text 2 will no longer be supported.



## <a name="usage">Usage</a>

**Filepaths will be suggested if there is a matching [trigger](#configuration_settings_scopes) for the current context** and its property _auto_ is set
to _true_. For a matching [trigger](#configuration_settings_scopes), filepath completions may be forced (ignoring _auto_ property) by the following
shorcuts:

- __`ctrl+alt+space`__ inserts filepaths relative, overriding possible settings
- __`ctrl+shift+space`__ inserts filepaths absolute, overriding possible settings

The current string may modify the suggested filepaths by the following rules:

- `word` suggests all matching files by the type (relative or absolute) as specified in the matched rule
- `./` suggests matching files within the current directory and inserts selection relative
- `../` suggests all matching files and inserts selection relative
- `/folder` suggests all matching files and insert selection absolute

FuzzyFilePath is disabled for single files or files outside the opened folder.

### open file

Use __`alt+enter`__ to open the file under cursor


#### Special Characters

If your projects contains filenames with special characters, consider modifying Sublime Texts `word_separators`.

i.e. in AngularJs filenames may start with `$`. In _Sublime Text | Preferences | Settings - User_ redeclare word
separators, removing `$`:
```js
	"word_separators": "./\\()\"'-:,.;<>~!@#%^&*|+=[]{}`~?"
```


## <a name="getting_started">Getting started</a>

### completions are not suggested

Assuming no errors are logged on console, add a minimum scope rule as first item in settings.scopes. Go to
_Sublime Text | Preferences | Package Settings | FuzzyFilePath | Settings - User_ and add

```js
"scopes": [
	{
		"scope": ".",
		"auto": true,
		// add your extensions here:
		"extensions": ["css", "html", "js"]
	}
]
```

This will propose filepaths for the given extensions in all autocompletion requests. To adjust the trigger see
[settings](configuration_settings). To log trigger evaluation, in settings set `"log": true"`.


### absolute filepaths begin in wrong directory

set your `project_directory` either in project settings or user settings to the correct folder. `project_directory`
must be relative to your sublime project directory.


### relative filepaths are not pointing to the correct file

Relative filepaths point from the current file to the selected file. Folders are moved upwards until the target path
is reachable. i.e. in case of css filepaths, the starting path may be relative from the html file importing the styles.

Set `base_directory` in scope rules to point from project_directory to html file. This will always set the starting
path of the trigger to `base_directory`. i.e.


## <a name="configuration">Configuration</a>

The default options - as always - should be set in user-settings:<br />
_Sublime Text | Preferences | Package Settings | FuzzyFilePath | Settings - User_

Project specific settings may be set in _Project | Edit Settings_:
```js
{
	"settings": {
		"FuzzyFilepath": {
			// adjusted settings
		}
	}
}
```

[See details refer to the wiki](https://github.com/sagold/FuzzyFilePath/wiki/Settings)


#### Related Plugins

##### [AutoFileName](https://github.com/BoundInCode/AutoFileName)

- uses file discovery based on current directory instead of fuzzy search
- adds properties for images in autocompletion description





