# Cookbook

A tool built for creating recipes in a simple formatted structure.

## Usage

### Note

* HTML template and recipe JSON schema are in `~/templates`.
    * Schema outlines general recipe file structure for compatability with cookbook.py.
* Completed recipe HMTL files can be found in `~/recipes`.

### Making recipes

1. Build recipe JSON file following `~/templates/recipe_schema.json` format.
    * Simple "step" format. Steps with same position will be kept in parallel.
2. Run cookbook.py pointing to JSON file.
    * Outputs HTML of recipe JSON file.

### Planned Updates

* Add difficulty rating.
* Add overall time estimate.
* Add way to summarize ingredients that get split.
* Adjust argparse to default to desired folders.