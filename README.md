# Window Manufacturing Calculator

## Overview
The Window Manufacturing Calculator is a tool designed to calculate the dimensions and quantities of parts required for manufacturing windows of types `A` and `TA`. It provides both a command-line interface (CLI) and a graphical user interface (GUI) for ease of use.

## Features
1. **Dynamic Calculations**: Calculates parts based on window type, dimensions, tolerance, and hand orientation.
2. **No Configuration Required**: Works without requiring a configuration code.
3. **Support for Two Window Types**:
   - **Type A**: Single window.
   - **Type TA**: Double window.
4. **Output Includes**:
   - Frame dimensions.
   - Glass/KLP dimensions.
   - Vertical parts (ÜH, AH, VERT).
   - Frame parts (ÜH, AH, VERT).
   - Glass strips (HOR, VERT).

## Files
1. **`window_calculator.py`**: Core logic for calculations.
2. **`window_calculator_cli.py`**: Command-line interface.
3. **`window_calculator_gui.py`**: Graphical user interface.
4. **`test_cli.py`**: Test script with predefined inputs.
5. **`window_data.json`**: Structured data for window configurations.

## How to Use

### Command-Line Interface (CLI)
Run the CLI to input parameters interactively:
```bash
python3 window_calculator_cli.py
```

#### Example:
```bash
Window Type (A/TA): A
Width (mm): 900
Height (mm): 900
Tolerance (tk): 3
Hand (P/V): P
```

### Graphical User Interface (GUI)
Run the GUI for a user-friendly interface:
```bash
python3 window_calculator_gui.py
```

#### Input Fields:
- **Window Type**: Choose `A` or `TA`.
- **Width (mm)**: Enter the window width.
- **Height (mm)**: Enter the window height.
- **Tolerance (tk)**: Enter the tolerance value.
- **Hand**: Choose `P` or `V`.

Click **Calculate** to see the results.

### Core Function
Use the `get_parts_list` function in your own code:
```python
from window_calculator import get_parts_list

# Example usage
result = get_parts_list("A", 900, 900, 3, "P")
print(result)
```

## Formulas

### Type A Windows
- **Frame Dimensions**:
  - Length (L): `width - 86`
  - Height (H): `height - 96`
- **Glass Dimensions**:
  - Length (L): `frame_L - 100`
  - Height (H): `frame_H - 100`
- **Parts**:
  - Vertical Parts:
    - ÜH: `L - 100`
    - AH: `K - 50`
    - VERT: `L - 86`
  - Frame Parts:
    - ÜH: `L - 86`
    - AH: `K - 96`
    - VERT: `L - 86`
  - Glass Strips:
    - HOR: `L - 86 - 100 + 4`
    - VERT: `K - 96 - 100 + 4`

### Type TA Windows
- **Frame Dimensions**:
  - Length (L): `(width - 80) // 2`
  - Height (H): `height - 96`
- **Glass Dimensions**:
  - Length (L): `frame_L - 100`
  - Height (H): `frame_H - 100`
- **Parts**:
  - Vertical Parts:
    - ÜH: `L - 100`
    - AH: `K - 50`
    - VERT: `(L - 80) / 2`
  - Frame Parts:
    - ÜH: `(L - 80) / 2`
    - AH: `K - 96`
    - VERT: `(L - 80) / 2`
  - Glass Strips:
    - HOR: `((L - 80) / 2) - 100 + 4`
    - VERT: `K - 96 - 100 + 4`

## Example Output
```
==================================================
Window Manufacturing Calculation Results
==================================================
Type: A
Product Type: 40STAND60x70
Width: 900 mm
Height: 900 mm
Tolerance (tk): 3 mm
Hand: P
--------------------------------------------------
Frame Dimensions:
  Length (L): 814 mm
  Height (H): 804 mm
  Tolerance (tk): 3 mm
Glass/KLP Dimensions:
  Length (L): 714 mm
  Height (H): 704 mm
Vertical Parts:
  ÜH: 800 mm (tk: 1)
  AH: 850 mm (tk: 2)
  VERT: 814 mm (tk: 1)
Frame Parts:
  ÜH: 814 mm (tk: 1)
  AH: 804 mm (tk: 2)
  VERT: 814 mm (tk: 1)
Glass Strips:
  HOR: 718 mm (tk: 2)
  VERT: 708 mm (tk: 2)
==================================================
```

## Requirements
- Python 3.x
- `tkinter` (for GUI)

## Installation
1. Clone the repository or download the files.
2. Ensure `tkinter` is installed:
   ```bash
   brew install python-tk
   ```

## Group Members
1. **John Doe** - Lead Developer
2. **Jane Smith** - UI/UX Designer
3. **Alice Johnson** - QA Engineer
4. **Bob Brown** - Documentation Specialist

## Support
For any issues or questions, please refer to the documentation or contact support.
