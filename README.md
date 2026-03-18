# Window Manufacturing Calculator

## Overview
The Window Manufacturing Calculator is a tool designed to calculate the dimensions and quantities of parts required for manufacturing windows of types `A` and `TA`. It provides both a command-line interface (CLI) and a graphical user interface (GUI) for ease of use.

The calculator also includes an **AI agent** that interprets customer special requests in natural language and applies physically consistent changes to the configuration — including complex cascading adjustments (e.g. a narrower sash profile automatically increases glass dimensions).

## Features
1. **Dynamic Calculations**: Calculates parts based on window type, dimensions, tolerance, and hand orientation.
2. **Support for Two Window Types**:
   - **Type A**: Single window.
   - **Type TA**: Double window.
3. **Output Includes**:
   - Frame dimensions.
   - Glass/KLP dimensions.
   - Vertical parts (ÜH, AH, VERT).
   - Frame parts (ÜH, AH, VERT).
   - Glass strips (HOR, VERT).
4. **AI Agent for Customer Special Requests**:
   - Natural language input (Estonian or English).
   - Understands manufacturing constraints and applies cascading changes.
   - Examples: removing glass strips, changing strip counts, narrower sash profile.

## Files
1. **`window_calculator.py`**: Core logic for calculations.
2. **`window_calculator_cli.py`**: Command-line interface.
3. **`window_calculator_gui.py`**: Graphical user interface.
4. **`ai_customizer.py`**: AI agent for applying customer special requests.
5. **`test_cli.py`**: Test script with predefined inputs.
6. **`window_data.json`**: Structured data for window configurations.
7. **`.env.example`**: Template for environment variables (copy to `.env` and fill in).

## Setup

### 1. Install dependencies
```bash
pip3 install openai
```

### 2. Configure API key
```bash
cp .env.example .env
# Open .env and set your MISTRAL_API_KEY
```

Get your Mistral API key at: https://console.mistral.ai/

The `.env` file is excluded from version control (see `.gitignore`).

### 3. Install tkinter (for GUI)
```bash
brew install python-tk
```

## How to Use

### Command-Line Interface (CLI)
```bash
python3 window_calculator_cli.py
```

After the base calculation, you will be prompted for customer special requests.

#### Example session:
```
Window Type (A/TA): A
Width (mm): 900
Height (mm): 900
Tolerance (tk): 3
Hand (P/V): P

[base calculation printed]

Kliendi erisoovid (jäta tühjaks kui pole): soovin, et leng oleks 10 mm kitsam

[modified calculation printed with AI explanation]
```

### Graphical User Interface (GUI)
```bash
python3 window_calculator_gui.py
```

1. Fill in window parameters and click **Calculate**.
2. Type a special request in the **Kliendi erisoovid** field.
3. Click **Rakenda erisoovid** — the AI agent processes the request in the background.

### Core Function
```python
from window_calculator import get_parts_list
from ai_customizer import apply_customer_customization

# Base calculation
result = get_parts_list("A", 900, 900, 3, "P")

# Apply customer special request
modified = apply_customer_customization(result, "sooviks akent ilma klaasiliistudeta")
```

## AI Agent — Special Requests

The AI agent understands manufacturing physics and applies all necessary cascading changes.

### Example requests

| Request | What changes |
|---|---|
| `sooviks akent ilma klaasiliistudeta` | Removes all glass strips |
| `soovin 2 vertikaalset ja ühe horisontaalse klaasiliistu` | Sets VERT tk=2, HOR tk=1 |
| `soovin, et leng oleks 10 mm kitsam` | Sash profile 50mm→40mm, glass grows +20mm on both axes |

### Why does a narrower sash affect glass size?

The current formula: `glass = frame - 100` (50 mm profile on each side).
If the sash profile is made 10 mm narrower (40 mm instead of 50 mm), the glass opening grows by 10 mm on each side = **+20 mm total**. Without this adjustment the glass would fall out.

## Formulas

### Type A Windows
- **Frame**: `L = width - 86`, `H = height - 96`
- **Glass**: `L = frame_L - 100`, `H = frame_H - 100`
- **Vertical Parts**: ÜH: `L-100`, AH: `K-50`, VERT: `L-86`
- **Frame Parts**: ÜH: `L-86`, AH: `K-96`, VERT: `L-86`
- **Glass Strips**: HOR: `L-86-100+4`, VERT: `K-96-100+4`

### Type TA Windows
- **Frame**: `L = (width - 80) / 2`, `H = height - 96`
- **Glass**: `L = frame_L - 100`, `H = frame_H - 100`
- **Vertical Parts**: ÜH: `L-100`, AH: `K-50`, VERT: `(L-80)/2`
- **Frame Parts**: ÜH: `(L-80)/2`, AH: `K-96`, VERT: `(L-80)/2`
- **Glass Strips**: HOR: `((L-80)/2)-100+4`, VERT: `K-96-100+4`

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
--------------------------------------------------
Kliendi erisoov: soovin, et leng oleks 10 mm kitsam
Rakendatud muutused:
  • lengi laius vähenes 10 mm (40 mm → 30 mm)
  • klaasi laius ja kõrgus suurenesid 20 mm (10 mm kummalgi pool)
Selgitus: Kuna leng on 10 mm kitsam, suureneb klaas mõlemalt poolt 10 mm = kokku 20 mm.
==================================================
```

## Requirements
- Python 3.x
- `openai` Python package (`pip3 install openai`)
- `tkinter` (for GUI): `brew install python-tk`
- Mistral API key (set in `.env`)

## Group Members
1. Juss Arus
2. Kristjan Noormets
3. Lisanna Höbemägi
4. Getter Aust

## Support
For any issues or questions, please refer to the documentation or contact support.
