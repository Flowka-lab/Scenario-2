# 🧭 GET STARTED — Bulk Production Scheduler

## ⚡ TL;DR — Quick Setup in 4 Steps

1. **Create a GitHub repository**  
   - Make a new repo on your GitHub (example: `bulk-production-scheduler-demo`)
   - Upload the project files:
     - `app.py`
     - `nlp_extractor.py`
     - `requirements.txt`
     - `data/` folder with CSVs (`orders.csv`, `lines.csv`, `vrac_products.csv`)

2. **Go to [streamlit.io](https://streamlit.io)**  
   - Create an account if you don’t have one yet.
   - Click **“New app”** → connect your GitHub repo.

3. **App settings**  
   - In **Advanced Settings**, set **Python version = 3.11**  
   - In **Secrets**, add your OpenAI API key (required):  
     ```toml
     OPENAI_API_KEY = "sk-proj-xxxxxx"
     ```
   - (Optional) You can also add a Deepgram key for voice commands:  
     ```toml
     DEEPGRAM_API_KEY = "dg-xxxxxx"
     ```

4. **That’s it — Deploy! 🎉**  
   Streamlit will build and run your app automatically.  
   After 1–2 minutes, your demo should be live at:  
   `https://<your-app-name>.streamlit.app`

---

## 🧩 Full Instructions — For Local or Detailed Setup

### A. Prepare the GitHub repository

1. Create a new empty repo on GitHub  
   - Example name: `bulk-production-scheduler-demo`
2. On your machine:

   ```bash
   git clone https://github.com/<your-username>/bulk-production-scheduler-demo.git
   cd bulk-production-scheduler-demo
   ```

3. Copy these files into the repo root:
   - `app.py`
   - `nlp_extractor.py`
   - `requirements.txt`
   - `README.md` (this file)
4. Create a folder:

   ```bash
   mkdir data
   ```

5. Put the CSV files into `data/`:
   - `data/orders.csv`
   - `data/lines.csv`
   - `data/vrac_products.csv`

6. Commit & push:

   ```bash
   git add .
   git commit -m "Initial commit: Bulk Production Scheduler demo"
   git push origin main    # or master, depending on repo
   ```

---

### B. Run locally

1. Make sure **Python 3.10+** is installed.

2. (Optional) Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Windows: .venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set environment variables for the APIs:

   ```bash
   export OPENAI_API_KEY="sk-..."   # LLM for intent extraction
   export DEEPGRAM_API_KEY="dg-..." # For voice transcription (optional)
   ```

   > If you don’t have keys yet:  
   > You can still run the app; LLM/voice commands may fail,  
   > but the chart and basic regex commands will work.

5. Start the app:

   ```bash
   streamlit run app.py
   ```

6. Open the URL (usually `http://localhost:8501`) in your browser.

7. Sanity checks:
   - You see a Gantt chart with several orders.
   - Sidebar shows filters (Orders, Products, Machines, Color by).
   - At the bottom you see:
     - 🧠 Command text box
     - 🎤 Voice button

---

### C. Smoke test (text commands)

1. In the **Command** box, type:

   ```text
   delay order 1 by 2 hours
   ```

2. Hit Enter:
   - You should see a success message (if `ORD-001` exists).
   - The bars for that order shift 2 hours to the right.

3. Try a swap:

   ```text
   swap order 1 with order 2
   ```

4. Check that:
   - Both orders exchange their positions on the Gantt chart.

If you see an error like “Unsupported intent” or “Unknown order”, check:

- Did you refer to an order ID that exists?
- Is OpenAI configured properly (for more complex phrasing)?

---

### D. Smoke test (voice commands)

> Requires `DEEPGRAM_API_KEY` and a microphone.

1. Click the **🎤 Voice** button.
2. Say:

   > “Delay order five by thirty minutes.”

3. Stop recording.
4. The app will:
   - Transcribe your speech
   - Normalize “order five” → `ORD-005`
   - Extract intent via OpenAI
   - Apply `delay_order` to that order

5. Check:
   - A success message appears
   - The schedule updates accordingly

If voice fails:

- Check Deepgram key is set.
- Check mic permissions in the browser.
- Look at the “Voice Debug” expander in the sidebar.

---

### E. Deploy to Streamlit Cloud (Detailed)

1. Push your latest code and data to GitHub.
2. Go to [Streamlit Cloud](https://share.streamlit.io) → **New app**.
3. Select your repo + branch, set:

   - **Main file**: `app.py`

4. In **Advanced Settings**:
   - **Python version** → `3.11`
   - **Secrets**:
     ```toml
     OPENAI_API_KEY = "sk-proj-xxxxx"
     DEEPGRAM_API_KEY = "dg-xxxxx"
     ```

5. Click **Deploy**.

6. Once deployed, perform the same smoke tests (delay + swap commands) from the cloud app URL.

---

### F. Share & Demo

Now you can:

- Add the app URL to:
  - LinkedIn posts
  - YouTube video descriptions
  - Personal portfolio

- Use it in live demos:
  - Talk over the Gantt chart
  - Type or speak commands
  - Show how LLMs can enhance the planning experience ✨
