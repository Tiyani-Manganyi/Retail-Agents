# 🏪 Retail Agents — Pius General Dealer

Five AI agents that watch your stock, pricing, demand, suppliers and customers 24/7 — and only recommend. You approve, modify or reject every decision.

---

## 🚀 Quick Start (5 minutes)

### 1. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 2. Add your FREE Gemini API key
```bash
cp .env.example .env
# Open .env and paste your key
```
Get a free key at: **https://aistudio.google.com/app/apikey**  
*(No credit card needed — 15 requests/min free)*

### 3. Run the server
```bash
python app.py
```

### 4. Open the dashboard
Go to: **http://localhost:5000**

---

## ☁️ Deploy to Render

The repository needs the application files (`app.py`, `retail-agent.html`, `requirements.txt`, and `render.yaml`) before Render can deploy it. Do not upload `.env`, `.venv/`, or `data/retail.db`; `.gitignore` excludes these local-only files.

1. Push this project to a GitHub repository you control. The repository URL currently shared for this project contains only a README, so upload the app files from this folder before continuing.
2. In Render, choose **New → Blueprint**, connect that GitHub repository, and select the branch containing `render.yaml`.
3. Review the Blueprint and create the web service and database.
4. In the Render service environment settings, set `GEMINI_API_KEY` to your Gemini API key and `STORE_PASSWORD` to a unique, strong password. `GEMINI_API_KEY_2` is optional. Never commit real keys or passwords to GitHub.
5. Wait for the deploy to finish, then open the `onrender.com` URL shown on the Render service. Use that URL for the dashboard; Gemini requires the Flask-backed site and will not work from a directly opened HTML file.

The Blueprint connects the web service to its PostgreSQL database using Render's `DATABASE_URL`. Choose a database plan appropriate for your needs and confirm its persistence/retention policy before using it for production data. After deploying, test login, CSV import, Gemini chat, and database persistence.

---

## 📁 Project Structure

```
retail-project/
├── app.py                  ← Flask backend + Gemini API integration
├── retail-agent.html       ← Standalone dashboard (works without Flask too)
├── requirements.txt        ← Python dependencies
├── .env.example            ← Environment variable template
├── .env                    ← Your secrets (gitignored)
├── data/
│   └── retail.db           ← SQLite database (auto-created on first run)
└── README.md
```

---

## 🤖 Gemini AI Integration

The dashboard's compact AI assistant sends each question and the current dashboard data to the Flask `/api/chat` endpoint. The server calls the Gemini REST API; API keys stay on the server and are never sent to the browser. To use Gemini, start Flask with `python app.py` and open `http://localhost:5000`; a `file://` page cannot reach the API.

| Feature | Details |
|---|---|
| Default model | `gemini-2.5-flash` (override with `GEMINI_MODEL`) |
| Context sent | Every dashboard product's stock, cost, selling/competitor price, sales history, reorder point and forecast; supplier/customer metrics, recommendations, and all five agent roles. Customer names are excluded. |
| Configuration | Set `GEMINI_API_KEY`; optionally set `GEMINI_API_KEY_2` for key rotation |
| Failure behavior | Shows a clear setup, rate-limit, timeout or service error instead of a canned answer |

The **Business Ideas** view uses the same protected server-side Gemini connection to generate five evidence-based suggestions, one for each retail agent. It uses the live store snapshot, does not execute suggestions, and requires owner/manager review. The view is also available from the mobile menu.

**What the AI can answer:**
- "Which products are running low?"
- "Who are my at-risk customers?"
- "Which supplier is most reliable?"
- "What's driving demand this week?"
- "Should I reorder White Bread?"

---

## 🗄️ API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Serve the dashboard HTML |
| GET | `/api/data` | All products, suppliers, customers, decisions |
| GET | `/api/stats` | Today's sales, pending approvals |
| GET | `/api/signals` | Payday/weather signals |
| POST | `/api/chat` | Gemini AI chat |
| POST | `/api/import/products` | Import products CSV |
| POST | `/api/import/suppliers` | Import suppliers CSV |
| POST | `/api/import/customers` | Import customers CSV |
| GET | `/api/template/<kind>` | Download CSV template |
| POST | `/api/decision` | Approve / reject / modify a decision |
| POST | `/api/sale` | Record a sale (reduces stock) |
| GET | `/api/sales-log` | Sales transaction history |
| POST | `/api/clear/<kind>` | Clear a data section |

---

## 📊 The Five AI Agents

| Agent | Code | Function |
|---|---|---|
| Demand & Sales | DSA | Forecasts using moving average + payday/weather signals |
| Inventory | IMA | Monitors stock vs reorder points, flags overstock |
| Pricing | PRA | Compares vs competitors, suggests adjustments |
| Procurement | PCA | Ranks suppliers, flags unreliable ones |
| Customer Engagement | CEA | Tracks segments, identifies at-risk customers |

---

## 📥 Importing Your Own Data

Use the **Data & Import** tab in the dashboard, or POST directly to the API:

Dashboard imports are saved in that browser's local storage, restored on refresh, and included in the live data snapshot sent to Gemini. Added records, cleared sections, and stock reductions from sales are retained locally too. These dashboard changes are not uploaded into the server database, so they do not automatically sync to another browser or device.

```bash
curl -X POST http://localhost:5000/api/import/products \
  -F "file=@products-template.csv"
```

Download the CSV templates from the dashboard or:
```bash
curl http://localhost:5000/api/template/products -o products-template.csv
```

---

## 🔧 Standalone Mode (No Flask)

`retail-agent.html` can render its dashboard in the browser with no server:
- Imported data is retained in that browser's local storage
- Added records, cleared sections, and stock reductions from sales are retained in that browser too
- CSV import, charts, dark mode and local agent recommendations work offline
- Gemini chat and Business Ideas require Flask and a valid server-side Gemini API key; use `http://localhost:5000` for AI features rather than opening the HTML file directly
- The demo login remembers the selected role on that browser until logout; it is not server-side authentication

---

## 📄 License
MIT — free to use, modify and distribute.
Built for South African township and general dealers. 🇿🇦
