# Retail Sales Analytics Dashboard — Python + Streamlit

A complete beginner-friendly project for demonstrating data analysis, interactive visualizations, filters, data validation, and dashboard deployment.

## Project files

- `app.py` — full Streamlit application and chart code
- `requirements.txt` — Python packages needed
- `data/retail_sales.csv` — 500 rows of synthetic practice data (not real customer data)

## What the app demonstrates

- CSV upload (students can use their own compatible CSV)
- Data cleaning and validation with pandas
- KPI cards: sales, profit, quantity, rows/orders, profit margin
- Monthly sales/profit line chart
- Sales by category bar chart
- Profit by region bar chart
- Top 10 products by sales
- Sidebar filters for region, category, and dates
- Data quality summary
- Download filtered data as CSV
- Basic auto-generated observations and trainer notes

## Part A — Run on your Windows computer

### 1. Install Python
1. Go to https://www.python.org/downloads/
2. Download a current Python 3 version.
3. During installation, tick **Add python.exe to PATH**.
4. Open Command Prompt and test:
   ```bash
   py --version
   ```
   If `py` does not work, try `python --version`.

### 2. Extract the project
Extract the ZIP file to a folder such as `C:\\Projects\\streamlit_student_dashboard`.

### 3. Open the folder in VS Code
1. Open VS Code.
2. Select **File → Open Folder**.
3. Select the extracted `streamlit_student_dashboard` folder.
4. Open **Terminal → New Terminal**.

### 4. Create and activate a virtual environment (recommended)
In the VS Code terminal on Windows:
```bash
py -m venv .venv
.venv\\Scripts\\activate
```
If `py` is unavailable but `python` works, replace `py` with `python`.

### 5. Install the packages
Run this from the project folder:
```bash
python -m pip install -r requirements.txt
```

### 6. Start the app
```bash
python -m streamlit run app.py
```
Streamlit will print a local URL, usually `http://localhost:8501`, and may open it in your browser. Keep the terminal running while presenting. To stop the app, click the terminal and press `Ctrl+C`.

### Common issues
- **`streamlit` is not recognized:** use `python -m streamlit run app.py` rather than `streamlit run app.py`.
- **`pip` is not recognized:** use `python -m pip install -r requirements.txt`.
- **Python not recognized:** install Python and reopen VS Code/Command Prompt; try `py --version`.
- **ModuleNotFoundError:** activate `.venv` and run `python -m pip install -r requirements.txt` again in the same terminal.
- **Port already in use:** Streamlit may offer another local port; use the URL it prints.

## Part B — Publish it online with Streamlit Community Cloud

This is the path for sharing a live app link with students. It usually requires a GitHub account and a Streamlit Community Cloud account.

1. Create/sign in to GitHub.
2. Create a **new repository** (for example, `retail-sales-streamlit`).
3. Upload the project files and folders to the repository. Keep this structure:
   ```text
   streamlit_student_dashboard/
   ├── app.py
   ├── requirements.txt
   └── data/
       └── retail_sales.csv
   ```
   You can upload the files at the repository root rather than uploading the outer folder itself.
4. Open https://share.streamlit.io/ and sign in using GitHub.
5. Choose **Create app** (or the current equivalent).
6. Select your repository, branch (usually `main`), and main file path `app.py`.
7. Deploy the app and wait for the build to finish.
8. Copy the app URL and share it with students.

If the deployment page asks for a Python version or advanced settings, start with the defaults unless the platform reports a compatibility problem. If you update `app.py` or `requirements.txt` in GitHub, Streamlit Cloud generally rebuilds/restarts the app.

**Important:** Do not upload private student data, financial records, passwords, API keys, or confidential company files to a public repository. Use the included synthetic dataset for classroom demos. Uploaded CSVs are processed by this app session; do not treat this as a secure production system.

## Part C — How to teach this in class (suggested 45–60 minutes)

1. **5 min:** Explain that Streamlit turns a Python script into a browser-based app.
2. **5 min:** Open `data/retail_sales.csv` and explain rows, columns, dates, sales, profit, and quantity.
3. **10 min:** Show `pd.read_csv`, data type conversion, and validation in `prepare_data()`.
4. **10 min:** Show KPI metrics and explain sales vs. profit vs. profit margin.
5. **10 min:** Demonstrate the monthly trend, category, region, and top-product charts.
6. **5 min:** Change the sidebar filters and ask students what changed.
7. **5 min:** Upload a compatible CSV and download filtered records.
8. **Optional:** Deploy online and share the app link.

## CSV format for students

Your CSV needs these columns (case and spaces do not matter):
- `Order Date` — valid date, e.g. `2025-01-15`
- `Region` — text category
- `Category` — text category
- `Product` — product name
- `Sales` — numeric
- `Profit` — numeric
- `Quantity` — numeric

The app validates required columns, converts date/numeric types, and removes rows with invalid date or numeric values. It does not automatically replace missing financial figures because students should investigate them rather than invent values.

## Learning outcomes

After the demonstration, students should be able to explain how a Python analysis becomes an interactive app, upload a CSV, apply filters, read common charts, interpret KPIs, and identify basic data quality issues.
