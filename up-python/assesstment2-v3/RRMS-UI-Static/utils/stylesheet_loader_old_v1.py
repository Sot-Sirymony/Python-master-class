import os

def load_stylesheet(mode="style", module=None, subdirectory=None):
    """
    Load a QSS stylesheet based on the specified mode, module, and optional subdirectory.

    Args:
        mode (str): The name of the stylesheet to load (default: "style").
        module (str): Optional name of a module-specific stylesheet to load.
        subdirectory (str): Optional subdirectory within the styles folder.

    Returns:
        str: The content of the stylesheet if found, otherwise an empty string.
    """
    # Get the base directory of this script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Base styles directory
    styles_dir = os.path.join(base_dir, "../assets/styles")
    
    # Adjust path if a subdirectory is provided
    if subdirectory:
        styles_dir = os.path.join(styles_dir, subdirectory)
    
    # Construct the base stylesheet path
    stylesheet_path = os.path.join(styles_dir, f"{mode}.qss")
    module_stylesheet_path = None

    # Check if a module-specific stylesheet is specified
    if module:
        module_stylesheet_path = os.path.join(styles_dir, f"{module}_{mode}.qss")

    styles = ""

    # Load the base stylesheet
    if os.path.exists(stylesheet_path):
        try:
            with open(stylesheet_path, "r") as file:
                styles += file.read()
        except Exception as e:
            print(f"Error loading base stylesheet {stylesheet_path}: {e}")
    else:
        print(f"Base stylesheet file not found at {stylesheet_path}. Skipping base styles.")

    # Load the module-specific stylesheet if provided
    if module_stylesheet_path and os.path.exists(module_stylesheet_path):
        try:
            with open(module_stylesheet_path, "r") as file:
                styles += "\n" + file.read()
        except Exception as e:
            print(f"Error loading module stylesheet {module_stylesheet_path}: {e}")
    elif module:
        print(f"Module-specific stylesheet file not found at {module_stylesheet_path}. Skipping module styles.")

    return styles
