# Early Turnover Prediction System

## Project description

This is a small web application for **early employee turnover prediction**. You can add employees with HR-style fields, get a **risk score** and **risk level** (Low / Medium / High), browse them on a dashboard, and record **interventions** (for example coaching or check-ins) per employee. Everything runs locally: a Python backend serves both the API and the web pages.

---

## Features

- **Add employees** through a simple form; data is saved in a local SQLite database.
- **Automatic risk prediction** after saving a new employee (the backend updates risk score and level).
- **Dashboard** to list employees, filter by risk or department, and sort by risk.
- **Employee detail page** (use `?id=` in the URL) to view one employee and their interventions.
- **Add interventions** linked to an employee (type, date, notes).
- **REST API** with interactive documentation at `/docs` for testing endpoints.
- **Works without a trained ML file**: if `model.pkl` is missing, the app uses a built-in rule-based fallback for risk.

---

## Technologies used

| Area | Technology |
|------|------------|
| Backend & API | [FastAPI](https://fastapi.tiangolo.com/) |
| Database | [SQLite](https://www.sqlite.org/) via [SQLAlchemy](https://www.sqlalchemy.org/) |
| Data validation | [Pydantic](https://docs.pydantic.dev/) |
| Machine learning (optional) | [scikit-learn](https://scikit-learn.org/) model loaded with [joblib](https://joblib.readthedocs.io/) |
| Data handling for the model | [pandas](https://pandas.pydata.org/) |
| Server | [Uvicorn](https://www.uvicorn.org/) |
| Frontend | Plain HTML, CSS, and JavaScript (no build step) |

---

## Prerequisites

- **Python 3.10+** (3.11+ recommended)
- A terminal (PowerShell on Windows, or Terminal on macOS/Linux)

---

## Create and activate a virtual environment

A virtual environment keeps this project’s packages separate from other Python projects.

**1. Open a terminal** in the project folder (the folder that contains `main.py`).

**2. Create the environment** (only needed once):

**Windows (PowerShell):**

```powershell
python -m venv venv
```

**macOS / Linux:**

```bash
python3 -m venv venv
```

**3. Activate it** (do this every time you open a new terminal for this project):

**Windows (PowerShell):**

```powershell
.\venv\Scripts\Activate.ps1
```

If execution policy blocks this, you can use Command Prompt instead:

```cmd
venv\Scripts\activate.bat
```

**macOS / Linux:**

```bash
source venv/bin/activate
```

When it works, your prompt usually shows `(venv)`.

---

## Install requirements

With the virtual environment **activated**, run:

```bash
pip install -r requirements.txt
```

This installs FastAPI, Uvicorn, SQLAlchemy, and the other libraries listed in `requirements.txt`.

---

## Run the backend

Stay in the project folder with `venv` **activated**, then start the server:

```bash
uvicorn main:app --reload
```

- **`main:app`** means “load the `app` object from `main.py`”.
- **`--reload`** restarts the server when you change code (handy while learning).

You should see log lines indicating the server is listening (by default on port **8000**). Leave this terminal open while you use the app.

**Optional — demo data:** to insert a few sample employees:

```bash
python seed_sample_employees.py
```

**Optional — real ML model:** place a file named **`model.pkl`** in the same folder as `main.py`. If it is absent, risk prediction still runs using the built-in fallback.

---

## Open and use the frontend

The frontend is **not a separate server**. FastAPI serves the HTML pages and static files from the `frontend/` folder.

1. With the backend running (`uvicorn main:app --reload`), open a web browser.
2. Use these addresses (same machine):

| Page | URL | What to do |
|------|-----|------------|
| **Home — Add employee** | http://127.0.0.1:8000/ | Fill the form and click **Save and predict risk**. You should see a success message and a risk summary. |
| **Dashboard** | http://127.0.0.1:8000/dashboard | See all employees; use filters and **Refresh**. Click **View details** for one row. |
| **Employee details** | http://127.0.0.1:8000/employee?id=1 | Replace `1` with an ID from the dashboard. View fields, list interventions, and add a new intervention. |
| **API docs** | http://127.0.0.1:8000/docs | Try API calls in the browser (Swagger UI). |

Static assets (CSS and shared JavaScript) load from paths like `/static/style.css` and `/static/app.js`.

If the page says it cannot reach the API, confirm Uvicorn is running and you used the correct URL (`127.0.0.1:8000`).

---

## How prediction works (simple explanation)

1. **Input**  
   The app collects employee information (age, department, satisfaction scores, income, attendance, and similar fields). That information describes “what we know about this person today.”

2. **Two possible paths**  
   - If **`model.pkl`** loads successfully, the backend turns those fields into the column layout the model expects, runs the model, and reads a **probability** (how likely turnover is in the model’s view). That probability is turned into a **risk level** (Low / Medium / High) using fixed thresholds.  
   - If there is **no model** or it fails to load, the app uses a **simple heuristic**: it combines a few key numbers (for example satisfaction and attendance) into a score and maps that to the same kind of **risk level**. So the UI always gets a risk result for normal flows.

3. **Where it shows up**  
   After you create an employee, the frontend calls an endpoint that **recomputes** risk and **saves** the new `risk_score` and `risk_level` on that employee row in the database. The dashboard and employee page read those stored values.

4. **Separate “raw” endpoint**  
   `POST /predict` is for sending **IBM-style feature names** directly to the model; it **requires** a working `model.pkl`. The employee flows use the mapping + model or fallback described above.

---

## Quick API reference

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/health` | Check that the API is running |
| GET | `/employees` | List employees (optional filters) |
| GET | `/employees/{id}` | Get one employee |
| POST | `/employees` | Create an employee |
| POST | `/employees/{id}/predict-risk` | Recalculate risk for that employee |
| GET | `/interventions/{employee_id}` | List interventions |
| POST | `/interventions` | Add an intervention |
| POST | `/predict-risk` | Predict from employee-shaped JSON (model or fallback) |
| POST | `/predict` | Predict from raw features (**needs** `model.pkl`) |

---

## Troubleshooting

| Problem | What to try |
|---------|-------------|
| **Network error** in the browser | Start `uvicorn` from the project folder with `venv` activated. |
| **503** on `POST /predict` | Add a valid `model.pkl` or use `/predict-risk` and the employee UI instead. |
| **Database issues** | Stop the server, delete `turnover.db` in the project root, start again (tables recreate; **data is lost**). |

---

## License / academic use

Use and adapt this project for learning and thesis work as needed for your institution’s rules.
