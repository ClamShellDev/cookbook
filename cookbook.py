from jinja2 import Environment, FileSystemLoader
import json
import argparse

def parse_args() -> argparse.Namespace:
    """Parse user arguments from command line.

    Returns:
        - Argparse namespace.
    """
    parser = argparse.ArgumentParser(description="Recipe HTML generator.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        '-i',
        '--input',
        type=str,
        required=True,
        help="Input file path of recipe.json."
    )
    parser.add_argument(
        '-o',
        '--output',
        type=str,
        help="Output file path without file extension.",
        default='output'
    )

    args = parser.parse_args()
    return args

def load_recipe(json_file:str) -> dict:
    """Load raw recipe file from JSON.

    Args:
        - json_file (str): Path to raw recipe file.

    Returns:
        - Python dictionary of JSON file.
    """
    with open(json_file, 'r', encoding='utf-8') as file:
        return json.load(file)

def sort_ingredients(steps:list[dict]) -> dict:
    """Collect ingredients from all steps and sorts alphabeticaly.

    Args:
        - steps (list of dict): List of steps as dictionaries.

    Returns:
        - Sorted dictionary of {"ingredient_name": "quantity", ...}.
    """
    ingredients = dict()
    for step in steps:
        if 'step_ingredients' in step:
            for ing in step['step_ingredients']:
                ingredients[ing['name']] = ing['quantity']
    return sorted(ingredients.items())

def group_steps_by_position(steps:list[dict]) -> dict:
    """Groups steps by position to track parallel steps.

    Args:
        - steps (list of dict): List of steps as dictionaries.

    Returns:
        - Dictionary of positions with lists of steps sharing position.
    """
    grouped = dict()
    for step in steps:
        pos = step['step_position']
        if pos not in grouped:
            grouped[pos] = []
        grouped[pos].append(step)
    return grouped

def generate_html(recipe_json:str, output_file:str, template_name:str="recipe_template.html") -> None:
    """Generates HTML file from recipe template.

    Args:
        - recipe_json (str): Path to raw recipe file.
        - template_path (str): Name of recipe template in ~/templates.
        - output_file (str): Path to output HTML file.
    """
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template(template_name)
    
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
    generate_html(args.input, f"{args.output}.html")