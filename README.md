# Bulk Production Scheduler – LLM & Voice Powered Demo

> **How can LLMs enhance the planning experience?**  
> By letting planners simply *write* or *say* what they want, and having an AI agent reshape the schedule for them.

This project is a **Streamlit demo app** for a **cosmetics / FMCG manufacturer** producing bulk products (e.g. shampoo base, conditioner, hair mask).  

It builds a **multi-stage production schedule** (Mix → Transfer → Fill → Finish), visualizes it as an **interactive Gantt chart**, and lets you adjust the plan using:

-  **Natural language commands** (text)  
-  **Voice commands** (via Deepgram transcription)  
-  **LLM intent extraction** (via OpenAI)

The goal is to showcase how modern LLMs can make production planning **more natural, interactive, and fun to demo**.

---

## Demo Scenario (FMCG / Cosmetics)

We simulate a factory that produces several **bulk VRAC products**:

- VRAC_SHAMPOO_BASE  
- VRAC_CONDITIONER_BASE  
- VRAC_HAIR_MASK  

Each **order**:

- Has an `order_id` (e.g. `ORD-052`)
- Produces a single `sku_id` (product)
- Has a `qty_kg` quantity in kg
- Has a `due_date` by which it should be finished

Each order is broken into 4 operations:

1. **MIX** – Mixing/processing in a bulk tank (`MIX_1`)
2. **TRF** – Transfer/holding (`TRANS_1`)
3. **FILL** – Filling/capping (`FILL_1`)
4. **FIN** – Finishing/QC (`FIN_1`)

Durations are derived from quantity and product-specific time percentages so that you see a realistic planning horizon (roughly a week of activity).

Orders are:

- Sorted by **due date**
- Scheduled forward from a fixed start date
- Passed through all stages without overlapping on the same machine

---

## Key Features

-  **Automatic baseline schedule**
  - Reads `orders.csv` + `lines.csv`
  - Builds a feasible schedule (no double-booking of machines)
-  **Interactive Gantt chart (Altair + Streamlit)**
  - Filter by product and machine
  - Limit number of orders displayed
  - Color by **Order / Product / Machine / Operation**
  - Click to highlight one order’s operations
-  **LLM-assisted scheduling**
  - Type natural language commands: _delay, advance, swap orders_
  - AI parses commands into structured JSON intent
-  **Voice commands (optional)**
  - Press mic button → speak your command (Deepgram STT)
  - LLM interprets the transcript and updates the schedule
-  **Built-in debug panels**
  - Last transcript
  - Last interpreted command
  - Intent payload, extracted durations, etc.

---

## Tech Stack

- **Frontend / App**: [Streamlit](https://streamlit.io/)
- **Data**: `pandas`, CSV files
- **Charts**: `Altair` Gantt chart
- **NLP / LLM**: OpenAI API (intent extraction)
- **Voice**: Deepgram API + `streamlit-mic-recorder`

---

## Project Structure

```text
.
├── app.py                       # Main Streamlit app (UI + scheduling logic)
├── nlp_extractor.py             # LLM intent extraction helper
├── requirements.txt             # Python dependencies
└── Docs/
    ├── Design Document v1.pdf   # Design document of the app
└── data/
    ├── orders.csv               # Production orders
    ├── lines.csv                # Available lines / machines
    └── vrac_products.csv        # Product metadata (rates, families, etc.)

---

## Getting Started

For a detailed, step-by-step guide (clone → run locally → deploy to Streamlit Cloud → test commands), see:
👉 [GET_STARTED.md](./GET_STARTED.md)
