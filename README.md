# A plugin for `ropt` to support tabular output in Everest
This package installs a plugin for the `ropt` robust optimization package, adding tabular output to Everest.

`everest-table` is developed by the Netherlands Organisation for Applied Scientific Research (TNO).

## Installation

Installation must be done from source. First find the appropriate version of the plugin by listing the available tags:

```bash
$ git tag -l
ert-14.3.0
ert-14.3.3
ert-14.4.0
ert-latest
```

The `ert-latest` tag just points to the newest tag, use it if the ERT/Everest version is the latest stable version.

Check out the selected tag using:

```bash
git checkout <tag>
```
replacing `<tag>` with the selected tag.

For older versions of ERT/Everest, select the highest version equal to or lower than the ERT/Everest version. For example, for ERT/Everest version 14.3.3 use `ert-14.3.3`. For version 14.3.2, `ert-14.3.0` would be needed.

**NOTE**: Adjust the tag according to the actual output of `git tag -l`!

After checking out the right tag, install the plugin using `pip`:

```bash
pip install .
```

## Usage

To enable the plugin, edit or create the following JSON file `<python-install-dir>/share/ropt/options.json`, or `<virtualenv-dir>/share/ropt/options.json`, and add this entry to the contents:
```json
{
    "basic_optimizer": {
        "event_handlers": ["everest_table/table"]
    }
}
```
