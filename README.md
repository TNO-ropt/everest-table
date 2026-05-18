# A plugin for `ropt` to support tabular output in Everest
This package installs a plugin for the `ropt` robust optimization package, adding tabular output to Everest.

`everest-table` is developed by the Netherlands Organisation for Applied Scientific Research (TNO).

## Installation

Installation must be done from source, install the plugin using `pip`:

```bash
pip install .
```

## Usage

To enable the plugin, edit or create the following JSON file `<python-install-dir>/share/ropt/options.json`, or `<virtualenv-dir>/share/ropt/options.json`, and add this entry to the contents:
```json
{
    "basic_optimizer": {
        "event_handlers": [
            "everest_table.Table"
        ]
    }
}
```
