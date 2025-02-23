from jinja2 import Environment, FileSystemLoader
import json
import argparse

# Parse user args
def parse_args():
    parser = argparse.ArgumentParser(description="Recipe HTML generator.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i','--input', type=str, required=True, help="Input file path of recipe.json.")
    parser.add_argument('-o','--output', type=str, help="Output file path without file extension.", default='output')
    args = parser.parse_args()
    return args

# Load JSON recipe file
def load_recipe(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        return json.load(file)

# Sort ingredients alphabetically
def sort_ingredients(steps):
    ingredients = {}
    for step in steps:
        if 'step_ingredients' in step:
            for ing in step['step_ingredients']:
                ingredients[ing['name']] = ing['quantity']
    return sorted(ingredients.items())

# Group steps by position
def group_steps_by_position(steps):
    grouped = {}
    for step in steps:
        pos = step['step_position']
        if pos not in grouped:
            grouped[pos] = []
        grouped[pos].append(step)
    return grouped

# Generate HTML file
def generate_html(recipe_json, template_path, output_file):
    env = Environment(loader=FileSystemLoader(template_path))
    template = env.get_template("recipe_template.html")
    
    recipe = load_recipe(recipe_json)
    ingredients = sort_ingredients(recipe['steps'])
    steps_grouped = group_steps_by_position(recipe['steps'])
    
    html_content = template.render(
        title=recipe['name'],
        description=recipe['description'],
        ingredients=ingredients,
        steps_grouped=steps_grouped
    )
    
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(html_content)
    print(f"HTML file generated: {output_file}")


if __name__ == "__main__":
    args = parse_args()
    generate_html(args.input, "templates", f"{args.output}.html")