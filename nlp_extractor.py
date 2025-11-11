# nlp_extractor.py

import json
import re
from openai import OpenAI

client = OpenAI()

PROMPT_INSTRUCTIONS = """
You are an assistant that interprets production scheduling commands for a small factory
planning demo.

The user will say short commands like:
- "Delay order 52 by thirty minutes"
- "Delay ORD-005 by 2 days"
- "Advance order 10 by half a day"
- "Bring forward order seven by 3 hours"
- "Swap order 67 and 83"
- "Swap ORD-003 with ORD-007"
- "Delay order 12 by tomorrow"

You must return ONLY a single JSON object with these exact keys:

- intent: "delay_order" | "swap_orders" | "unknown"
- order_id: string like "ORD-001" (uppercase) or null
- order_id_2: string like "ORD-002" (only used for swap_orders, otherwise null)
- days: number (can be negative for advancing) – default 0
- hours: number (can be negative for advancing) – default 0
- minutes: number (can be negative for advancing) – default 0

NORMALIZATION RULES (VERY IMPORTANT):

1. ORDER IDs
   - "order 1" / "order one" / "order 001" → "ORD-001"
   - "order 52" → "ORD-052"
   - If the user says "swap order 67 and 83", interpret this as:
       order_id   = "ORD-067"
       order_id_2 = "ORD-083"
     i.e. the second bare number "83" is also an order number.
   - Always output order IDs in the "ORD-XYZ" format, 3 digits, zero-padded.

2. DELAY vs ADVANCE (direction)
   - Words like "delay", "push", "postpone", "move later" mean move LATER in time:
       → use POSITIVE durations (days/hours/minutes > 0).
   - Words like "advance", "advanced", "bring forward", "pull in", "move earlier"
     mean move EARLIER in time:
       → use NEGATIVE durations (days/hours/minutes < 0).
   - Example:
       "Advance order 5 by 2 days"  → intent: "delay_order", order_id: "ORD-005",
                                      days: -2, hours: 0, minutes: 0
       "Advanced order 5 by 2 days" (past tense) should be treated the SAME as
       "Advance order 5 by 2 days".

3. DURATION PHRASES
   Interpret flexible natural language durations:
   - "half a day" or "half day"        → 12 hours
   - "half an hour" or "half hour"     → 30 minutes
   - "a day and a half"                → 1.5 days (or 1 day and 12 hours)
   - You may decompose mixed units into (days, hours, minutes).
   - If the user says "by tomorrow" (without a specific number of hours):
       → treat it as 1 day from now at roughly the same hour
       → output: days = 1, hours = 0, minutes = 0
   - If the duration is ambiguous but clearly means "around tomorrow", prefer:
       days = 1 (and hours = 0, minutes = 0).

4. SWAP COMMANDS
   - If the user wants to swap two orders:
       → intent = "swap_orders"
       → order_id   = first order (normalized "ORD-XYZ")
       → order_id_2 = second order (normalized "ORD-ABC")
       → days, hours, minutes should be 0.
   - Examples:
       "Swap order 67 and 83"
       "Swap order 1 with order 10"
       "Switch ORD-005 and ORD-010"

5. WHEN YOU ARE UNSURE
   - If you cannot confidently detect a valid delay or swap command:
       → intent = "unknown"
       → order_id = null
       → order_id_2 = null
       → days = 0, hours = 0, minutes = 0

FORMAT RULES:
- Return ONLY the JSON object, no extra text.
- Ensure all required keys are present.
- Use numbers for days/hours/minutes (can be 0 or negative).
"""

def _pre_normalize_text(text: str) -> str:
    """
    Light pre-normalization before sending to the model.
    - Handle common STT quirks like 'advanced' vs 'advance'.
    - Keep it simple; we still want the model to see most of the raw phrasing.
    """
    if not text:
        return text

    # Normalize common STT mistake: "advanced" -> "advance"
    # We do this in a case-insensitive way but preserve original casing roughly
    def repl_advanced(m):
        word = m.group(0)
        # keep capitalization of the first letter
        if word[0].isupper():
            return "Advance"
        else:
            return "advance"

    text = re.sub(r"\badvanced\b", repl_advanced, text, flags=re.IGNORECASE)

    return text


def ai_extract_intent(text: str) -> dict:
    """
    Uses the new OpenAI SDK (openai>=1.x style) to extract a structured intent
    from a free-form text command.

    Returns a dict with at least:
      - intent
      - order_id
      - order_id_2
      - days
      - hours
      - minutes
      - _source (always "openai")
      - optionally _error if something went wrong
    """
    cleaned = _pre_normalize_text(text or "")

    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",  # keep your existing model choice
            messages=[
                {"role": "system", "content": PROMPT_INSTRUCTIONS},
                {"role": "user", "content": cleaned},
            ],
            temperature=0.0,
            response_format={"type": "json_object"},
        )

        content = resp.choices[0].message.content
        data = json.loads(content)

        # Ensure all required keys exist & have sensible defaults
        data.setdefault("intent", "unknown")
        data.setdefault("order_id", None)
        data.setdefault("order_id_2", None)
        data.setdefault("days", 0)
        data.setdefault("hours", 0)
        data.setdefault("minutes", 0)

        # Tag source so your debug panel knows where it came from
        data["_source"] = "openai"
        return data

    except Exception as e:
        # Graceful fallback: unknown intent + error string for debug
        return {
            "intent": "unknown",
            "order_id": None,
            "order_id_2": None,
            "days": 0,
            "hours": 0,
            "minutes": 0,
            "_error": str(e),
            "_source": "openai",
        }
