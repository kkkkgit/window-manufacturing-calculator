#!/usr/bin/env python3
"""
Window Manufacturing Calculator CLI
Allows users to input window parameters via command line and view the calculated parts list.
"""

from window_calculator import get_parts_list, format_output
from ai_customizer import apply_customer_customization


def main():
    """Run the CLI application."""
    print("=" * 60)
    print("Window Manufacturing Calculator CLI")
    print("=" * 60)

    # Get user input
    window_type = input("Window Type (A/TA): ").strip().upper()
    while window_type not in ["A", "TA"]:
        print("Invalid window type. Please enter 'A' or 'TA'.")
        window_type = input("Window Type (A/TA): ").strip().upper()

    try:
        width = int(input("Width (mm): "))
        height = int(input("Height (mm): "))
        tk = int(input("Tolerance (tk): "))
        hand = input("Hand (P/V): ").strip().upper()
        while hand not in ["P", "V"]:
            print("Invalid hand orientation. Please enter 'P' or 'V'.")
            hand = input("Hand (P/V): ").strip().upper()

        # Validate inputs
        if width <= 0 or height <= 0 or tk < 0:
            print("Error: Dimensions must be positive.")
            return

        # Calculate parts
        result = get_parts_list(window_type, width, height, tk, hand)

        # Display base results
        print("\n" + "=" * 60)
        print("Calculation Results")
        print("=" * 60)
        print(format_output(result))

        # Ask for customer special requests
        print("\n" + "-" * 60)
        custom_request = input(
            "Kliendi erisoovid (jäta tühjaks kui pole): "
        ).strip()

        if custom_request:
            print("\nRakendан erisoove AI agendi abil...")
            try:
                modified = apply_customer_customization(result, custom_request)
                print("\n" + "=" * 60)
                print("Muudetud detailide nimekiri")
                print("=" * 60)
                print(format_output(modified))
            except Exception as e:
                print(f"Erisoovide rakendamisel tekkis viga: {e}")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()