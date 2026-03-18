#!/usr/bin/env python3
"""
Test script for the CLI to verify it works with predefined inputs.
"""

from window_calculator import get_parts_list, format_output


def test_cli():
    """Test the CLI with predefined inputs."""
    print("=" * 60)
    print("Window Manufacturing Calculator CLI - Test Mode")
    print("=" * 60)
    
    # Predefined inputs
    window_type = "A"
    width = 900
    height = 900
    tk = 3
    hand = "P"
    config = "P44-14"
    
    print(f"Window Type: {window_type}")
    print(f"Width: {width} mm")
    print(f"Height: {height} mm")
    print(f"Tolerance (tk): {tk}")
    print(f"Hand: {hand}")
    
    try:
        # Calculate parts
        result = get_parts_list(window_type, width, height, tk, hand)
        
        # Display results
        print("\n" + "=" * 60)
        print("Calculation Results")
        print("=" * 60)
        print(format_output(result))
        
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    test_cli()