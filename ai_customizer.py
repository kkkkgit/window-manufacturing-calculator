#!/usr/bin/env python3
"""
AI Agent for applying customer special requests to window configurations.

Uses Mistral AI (via OpenAI-compatible API) to interpret natural language
requests and apply physically consistent changes to the window configuration.

Requires MISTRAL_API_KEY environment variable.
"""

import copy
import json
import os
from pathlib import Path

from openai import OpenAI


def _load_env():
    """Load .env file from project directory if present."""
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, _, value = line.partition("=")
                    os.environ.setdefault(key.strip(), value.strip())


_load_env()


MISTRAL_BASE_URL = "https://api.mistral.ai/v1"
MISTRAL_MODEL = "mistral-large-latest"

SYSTEM_PROMPT = """Sa oled kogenud aknatootmise insener. Tead aknaehituse füüsikat läbi ja lõhki.

OLULINE TOOTMISALANE TEADMINE:
- "leng" = akna tiiva raamprofii (sash profile)
- Praegune valem: klaas_L = raami_L - 100 (50 mm profiil kummalgi pool horisontaalselt)
- Praegune valem: klaas_K = raami_K - 100 (50 mm profiil kummalgi pool vertikaalselt)
- Kui leng on 10 mm kitsam (40 mm i.o. 50 mm): säästetakse 10 mm mõlemal pool → klaas_L = raami_L - 80 ja klaas_K = raami_K - 80
- Üldiselt: kui leng on N mm kitsam, suureneb klaas 2×N mm (mõlemalt poolt kokku)
- Klaasiliistud (glass_strips) on dekoratiivsed — neid saab vabalt lisada/eemaldada/muuta
- Vertikaalsed klaasiliistud (VERT): nende pikkus = klaasi K (kõrgus), arv = tk väljal
- Horisontaalsed klaasiliistud (HOR): nende pikkus = klaasi L (laius), arv = tk väljal
- Klaas PEAB alati raamis kinni jääma — ära vähenda klaasi ilma raami muutmata

Kui klient teeb erisoovi:
1. Mõista füüsikalisi tagajärgi
2. Rakenda KÕIK vajalikud kaskaad-muutused (nt kitsam leng → suurem klaas)
3. Kasuta update_configuration tööriista muutuste rakendamiseks
4. Selgita lühidalt mida ja miks muutsid"""


def apply_customer_customization(base_config: dict, customer_request: str) -> dict:
    """
    Use Mistral AI to interpret and apply a customer's special request.

    Args:
        base_config: The calculated window configuration dictionary.
        customer_request: Customer's special request in natural language.

    Returns:
        Modified configuration with customizations applied.
    """
    api_key = os.environ.get("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError(
            "MISTRAL_API_KEY keskkonna muutuja on seadmata. "
            "Seadista see enne rakenduse käivitamist:\n"
            "  export MISTRAL_API_KEY=sinu_võti"
        )

    client = OpenAI(api_key=api_key, base_url=MISTRAL_BASE_URL)

    tools = [
        {
            "type": "function",
            "function": {
                "name": "update_configuration",
                "description": (
                    "Rakenda muutused akna konfiguratsioonile, säilitades füüsikalise "
                    "terviklikkuse (nt kitsam leng → suurem klaas)."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "glass_changes": {
                            "type": "object",
                            "description": "Klaasi mõõtude muutused (kui vaja)",
                            "properties": {
                                "L": {"type": "number", "description": "Uus klaasi laius mm"},
                                "H": {"type": "number", "description": "Uus klaasi kõrgus mm"},
                            },
                        },
                        "frame_changes": {
                            "type": "object",
                            "description": "Raami mõõtude muutused (kui vaja)",
                            "properties": {
                                "L": {"type": "number"},
                                "H": {"type": "number"},
                            },
                        },
                        "glass_strips": {
                            "type": "object",
                            "description": (
                                "Klaasiliistude uus konfiguratsioon. "
                                "Tühi objekt {} eemaldab kõik liistud. "
                                "Näide 2 vertikaalse ja 1 horisontaalsega: "
                                '{"VERT": {"dimension": 708, "tk": 2}, '
                                '"HOR": {"dimension": 718, "tk": 1}}'
                            ),
                            "additionalProperties": {
                                "type": "object",
                                "properties": {
                                    "dimension": {"type": "number"},
                                    "tk": {"type": "integer"},
                                },
                                "required": ["dimension", "tk"],
                            },
                        },
                        "customizations_applied": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Loend rakendatud muutustest (kuvamiseks)",
                        },
                        "explanation": {
                            "type": "string",
                            "description": "Lühike selgitus tehtud muutustest ja põhjustest",
                        },
                    },
                    "required": ["customizations_applied", "explanation"],
                },
            },
        }
    ]

    user_message = (
        f"Praegune akna konfiguratsioon:\n"
        f"{json.dumps(base_config, indent=2, ensure_ascii=False)}\n\n"
        f'Kliendi erisoov: "{customer_request}"\n\n'
        f"Analüüsi soovi ja rakenda vajalikud muutused."
    )

    response = client.chat.completions.create(
        model=MISTRAL_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        tools=tools,
        tool_choice="any",
    )

    modified_config = copy.deepcopy(base_config)
    explanation = ""
    customizations = []

    message = response.choices[0].message
    if message.tool_calls:
        for tool_call in message.tool_calls:
            if tool_call.function.name == "update_configuration":
                inp = json.loads(tool_call.function.arguments)
                explanation = inp.get("explanation", "")
                customizations = inp.get("customizations_applied", [])

                if inp.get("glass_changes"):
                    modified_config["glass"].update(inp["glass_changes"])

                if inp.get("frame_changes"):
                    modified_config["frame"].update(inp["frame_changes"])

                if "glass_strips" in inp:
                    modified_config["glass_strips"] = inp["glass_strips"]

    modified_config["customization_request"] = customer_request
    modified_config["customization_explanation"] = explanation
    modified_config["customizations_applied"] = customizations

    return modified_config
