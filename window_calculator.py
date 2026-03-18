#!/usr/bin/env python3
"""
Window Manufacturing Calculator
Calculates frame, glass, and part dimensions based on input parameters.
"""

import json
from typing import Dict, Any, Optional


def load_window_data(file_path: str = "window_data.json") -> list:
    """Load window data from JSON file."""
    with open(file_path, "r") as file:
        return json.load(file)


def calculate_frame_parts(frame_parts: Dict[str, Dict[str, Any]], width: int, height: int) -> Dict[str, Dict[str, Any]]:
    """Calculate frame part dimensions and quantities."""
    result = {}
    for key, part in frame_parts.items():
        if isinstance(part, dict):
            formula = part["formula"]
            if isinstance(formula, str):
                if formula.startswith("("):
                    # Evaluate mathematical expressions like ((L-80)/2)
                    try:
                        value = eval(formula.replace("L", str(width)).replace("K", str(height)))
                        if value <= 0:
                            raise ValueError(f"Calculated frame part dimension for {key} is not positive.")
                        result[key] = {"dimension": value, "tk": part["tk"]}
                    except Exception as e:
                        raise ValueError(f"Error calculating frame part {key}: {e}")
                elif "-" in formula or "+" in formula or "/" in formula:
                    # Evaluate simple arithmetic like L-86 or (L-80)/2
                    try:
                        # Replace L and K with actual dimensions
                        expr = formula.replace("L", str(width)).replace("K", str(height))
                        # Handle expressions like L-86 or (L-80)/2
                        if expr.startswith("("):
                            value = eval(expr)
                        else:
                            # Split into parts for simple arithmetic (e.g., L-86)
                            parts = expr.replace("-", "+").replace("/", "+").split("+")
                            if len(parts) == 2:
                                if parts[1].isdigit():
                                    value = width - int(parts[1]) if "-" in formula else width + int(parts[1])
                                else:
                                    value = eval(expr)
                            else:
                                value = eval(expr)
                        if value <= 0:
                            raise ValueError(f"Calculated frame part dimension for {key} is not positive.")
                        result[key] = {"dimension": value, "tk": part["tk"]}
                    except Exception as e:
                        raise ValueError(f"Error calculating frame part {key}: {e}")
                else:
                    result[key] = {"dimension": formula, "tk": part["tk"]}
            else:
                result[key] = {"dimension": formula, "tk": part["tk"]}
        else:
            result[key] = part
    return result


def calculate_vertical_parts(vertical_parts: Dict[str, Dict[str, Any]], width: int, height: int) -> Dict[str, Dict[str, Any]]:
    """Calculate vertical part dimensions and quantities."""
    result = {}
    for key, part in vertical_parts.items():
        if isinstance(part, dict):
            try:
                # Replace L and K with actual dimensions
                expr = part["formula"].replace("L", str(width)).replace("K", str(height))
                # Evaluate the expression
                value = eval(expr)
                if value <= 0:
                    raise ValueError(f"Calculated vertical part dimension for {key} is not positive.")
                result[key] = {"dimension": value, "tk": part["tk"]}
            except Exception as e:
                raise ValueError(f"Error calculating vertical part {key}: {e}")
        else:
            result[key] = part
    return result


def calculate_glass_strips(glass_strips: Dict[str, Dict[str, Any]], width: int, height: int) -> Dict[str, Dict[str, Any]]:
    """Calculate glass strip dimensions and quantities."""
    result = {}
    for key, strip in glass_strips.items():
        if isinstance(strip, dict):
            try:
                # Replace L and K with actual dimensions
                expr = strip["formula"].replace("L", str(width)).replace("K", str(height))
                # Evaluate the expression
                value = eval(expr)
                if value <= 0:
                    raise ValueError(f"Calculated glass strip dimension for {key} is not positive.")
                result[key] = {"dimension": value, "tk": strip["tk"]}
            except Exception as e:
                raise ValueError(f"Error calculating glass strip {key}: {e}")
        else:
            result[key] = strip
    return result


def calculate_window_parameters(
    window_type: str,
    product_type: str,
    width: int,
    height: int,
    tk: int,
    hand: str
) -> Dict[str, Any]:
    """Calculate all window parameters based on input."""
    # Validate input dimensions
    if width <= 0 or height <= 0 or tk < 0:
        raise ValueError("Dimensions must be positive.")
    
    # Calculate frame dimensions based on window type
    if window_type == "A":
        frame_L = width - 86
        frame_H = height - 96
    else:  # TA type
        frame_L = (width - 80) // 2
        frame_H = height - 96
    
    frame_tk = tk
    
    # Calculate glass dimensions
    glass_L = frame_L - 100
    glass_H = frame_H - 100
    
    # Validate frame and glass dimensions
    if frame_L <= 0 or frame_H <= 0:
        raise ValueError("Frame dimensions must be positive.")
    
    if glass_L <= 0 or glass_H <= 0:
        raise ValueError("Glass dimensions must be positive.")
    
    # Define formulas based on window type
    if window_type == "A":
        vertical_parts = {
            "ÜH": {"formula": "L-100", "tk": 1},
            "AH": {"formula": "K-50", "tk": 2},
            "VERT": {"formula": "L-86", "tk": 1}
        }
        frame_parts = {
            "ÜH": {"formula": "L-86", "tk": 1},
            "AH": {"formula": "K-96", "tk": 2},
            "VERT": {"formula": "L-86", "tk": 1}
        }
        glass_strips = {
            "HOR": {"formula": "L-86-100+4", "tk": 2},
            "VERT": {"formula": "K-96-100+4", "tk": 2}
        }
    else:  # TA type
        vertical_parts = {
            "ÜH": {"formula": "L-100", "tk": 1},
            "AH": {"formula": "K-50", "tk": 2},
            "VERT": {"formula": "(L-80)/2", "tk": 2}
        }
        frame_parts = {
            "ÜH": {"formula": "(L-80)/2", "tk": 2},
            "AH": {"formula": "K-96", "tk": 4},
            "VERT": {"formula": "(L-80)/2", "tk": 2}
        }
        glass_strips = {
            "HOR": {"formula": "((L-80)/2)-100+4", "tk": 4},
            "VERT": {"formula": "K-96-100+4", "tk": 4}
        }
    
    # Calculate frame parts
    frame_parts_calculated = calculate_frame_parts(frame_parts, width, height)
    
    # Calculate vertical parts
    vertical_parts_calculated = calculate_vertical_parts(vertical_parts, width, height)
    
    # Calculate glass strips
    glass_strips_calculated = calculate_glass_strips(glass_strips, width, height)
    
    return {
        "type": window_type,
        "product_type": product_type,
        "width": width,
        "height": height,
        "tk": tk,
        "hand": hand,
        "frame": {"L": frame_L, "H": frame_H, "tk": frame_tk},
        "glass": {"L": glass_L, "H": glass_H, "tk": None},
        "vertical_parts": vertical_parts_calculated,
        "frame_parts": frame_parts_calculated,
        "glass_strips": glass_strips_calculated,
    }


def format_output(result: Dict[str, Any]) -> str:
    """Format the output for readability."""
    output = []
    output.append("=" * 50)
    output.append("Window Manufacturing Calculation Results")
    output.append("=" * 50)
    output.append(f"Type: {result['type']}")
    output.append(f"Product Type: {result['product_type']}")
    output.append(f"Width: {result['width']} mm")
    output.append(f"Height: {result['height']} mm")
    output.append(f"Tolerance (tk): {result['tk']} mm")
    output.append(f"Hand: {result['hand']}")

    output.append("-" * 50)
    
    # Frame dimensions
    output.append("Frame Dimensions:")
    output.append(f"  Length (L): {result['frame']['L']} mm")
    output.append(f"  Height (H): {result['frame']['H']} mm")
    output.append(f"  Tolerance (tk): {result['frame']['tk']} mm")
    
    # Glass dimensions
    output.append("Glass/KLP Dimensions:")
    output.append(f"  Length (L): {result['glass']['L']} mm")
    output.append(f"  Height (H): {result['glass']['H']} mm")
    if result['glass']['tk'] is not None:
        output.append(f"  Tolerance (tk): {result['glass']['tk']} mm")
    
    # Vertical parts
    output.append("Vertical Parts:")
    for key, part in result['vertical_parts'].items():
        if isinstance(part, dict):
            output.append(f"  {key}: {part['dimension']} mm (tk: {part['tk']})")
        else:
            output.append(f"  {key}: {part if part is not None else 'N/A'}")
    
    # Frame parts
    output.append("Frame Parts:")
    for key, part in result['frame_parts'].items():
        if isinstance(part, dict):
            output.append(f"  {key}: {part['dimension']} mm (tk: {part['tk']})")
        else:
            output.append(f"  {key}: {part}")
    
    # Glass strips
    output.append("Glass Strips:")
    for key, strip in result['glass_strips'].items():
        if isinstance(strip, dict):
            output.append(f"  {key}: {strip['dimension']} mm (tk: {strip['tk']})")
        else:
            output.append(f"  {key}: {strip if strip is not None else 'N/A'}")
    
    # Customizations applied by AI agent
    if result.get("customization_request"):
        output.append("-" * 50)
        output.append(f"Kliendi erisoov: {result['customization_request']}")
        if result.get("customizations_applied"):
            output.append("Rakendatud muutused:")
            for item in result["customizations_applied"]:
                output.append(f"  • {item}")
        if result.get("customization_explanation"):
            output.append(f"Selgitus: {result['customization_explanation']}")

    output.append("=" * 50)
    return "\n".join(output)


def get_parts_list(window_type: str, width: int, height: int, tk: int, hand: str) -> Dict[str, Any]:
    """
    Calculate and return the parts list for a given window configuration.
    
    Args:
        window_type: Type of window (e.g., "A" or "TA").
        width: Width of the window in mm.
        height: Height of the window in mm.
        tk: Tolerance value.
        hand: Hand orientation (e.g., "P" or "V").
    
    Returns:
        Dictionary containing the calculated parts list.
    """
    # Determine product type based on window type
    product_type = "77STAND60x70" if window_type == "TA" else "40STAND60x70"
    
    try:
        result = calculate_window_parameters(
            window_type, product_type, width, height, tk, hand
        )
        return result
    except ValueError as e:
        raise ValueError(f"Error calculating parts list: {e}")


def main():
    """Example usage."""
    # Example input
    window_type = "A"
    width = 900
    height = 900
    tk = 3
    hand = "P"
    config = "P44-14"
    
    try:
        result = get_parts_list(window_type, width, height, tk, hand, config)
        print(format_output(result))
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()