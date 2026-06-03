"""
AI Vibe Coding — Excel Analysis Service

A FastAPI service that lets users upload Excel files and ask questions
in natural language. The service analyses the data using pandas/numpy/seaborn
and returns insights + an enriched Excel file.

This is a DEMO that shows the ARCHITECTURE. The AI prompt→code translation
step would integrate with OpenAI/Claude API in production.
"""

import io
import re
import uuid
from pathlib import Path
from typing import Optional

import pandas as pd
import numpy as np
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="AI Vibe Coding — Excel Analysis",
    description="Upload an Excel file, ask questions in plain English, get back insights + enriched Excel.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Temporary storage for uploaded files
TEMP_DIR = Path("temp")
TEMP_DIR.mkdir(exist_ok=True)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Vibe Coding — Excel Analysis</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f7fa; color: #1a1a2e; max-width: 900px; margin: 0 auto; padding: 40px 20px;
        }
        h1 { font-size: 2em; margin-bottom: 8px; }
        .subtitle { color: #666; margin-bottom: 32px; }
        .card {
            background: white; border-radius: 12px; padding: 28px; margin-bottom: 24px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        }
        label { display: block; font-weight: 600; margin-bottom: 8px; }
        input[type=file], textarea, select {
            width: 100%; padding: 12px; border: 2px solid #e0e0e0; border-radius: 8px;
            font-size: 14px; margin-bottom: 16px;
        }
        textarea { min-height: 100px; resize: vertical; font-family: inherit; }
        button {
            background: #6c5ce7; color: white; border: none; padding: 14px 36px;
            border-radius: 8px; font-size: 16px; font-weight: 600; cursor: pointer;
            transition: background 0.2s;
        }
        button:hover { background: #5a4bd1; }
        button:disabled { background: #b0a8e0; cursor: not-allowed; }
        .result { margin-top: 20px; }
        .result a { color: #6c5ce7; font-weight: 600; }
        .error { color: #e74c3c; background: #fdeaea; padding: 12px; border-radius: 8px; }
        .prompt-examples { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 16px; }
        .prompt-chip {
            background: #eeeef8; padding: 6px 14px; border-radius: 20px; font-size: 13px;
            cursor: pointer; transition: background 0.2s; border: none;
        }
        .prompt-chip:hover { background: #ddddf0; }
        .footer { text-align: center; color: #999; font-size: 13px; margin-top: 40px; }
    </style>
</head>
<body>
    <h1>📊 AI Vibe Coding — Excel Analysis</h1>
    <p class="subtitle">Upload an Excel file, describe your analysis in plain English, get results back.</p>

    <div class="card">
        <form id="uploadForm">
            <label for="file">1. Upload Excel File</label>
            <input type="file" name="file" id="file" accept=".xlsx,.xls" required>

            <label for="prompt">2. Describe what you want to analyse</label>
            <div class="prompt-examples">
                <button type="button" class="prompt-chip" onclick="setPrompt('Show me total sales by category and region with a bar chart, then write the pivot table to a new sheet.')">Sales by category & region</button>
                <button type="button" class="prompt-chip" onclick="setPrompt('Analyse monthly profit trends, find the top 5 best-selling products, and create a correlation heatmap of numeric columns. Write results to new sheets.')">Monthly trends + top products</button>
                <button type="button" class="prompt-chip" onclick="setPrompt('Create a pivot table of average order value by customer segment and shipping mode. Show me a summary statistics sheet.')">Pivot table + summary stats</button>
            </div>
            <textarea name="prompt" id="prompt" placeholder="e.g. Show me total sales by category and region, create a pivot table, and write the results to a new sheet..." required></textarea>

            <button type="submit" id="submitBtn">🚀 Analyse</button>
        </form>
        <div id="status" class="result"></div>
    </div>

    <div class="card">
        <h3>How it works</h3>
        <ol style="margin-left: 20px; line-height: 1.8;">
            <li><strong>Upload</strong> your Excel file</li>
            <li><strong>Describe</strong> your analysis in natural language</li>
            <li>The AI <strong>interprets</strong> your intent and generates Python code</li>
            <li>Code <strong>executes</strong> against your data using pandas/numpy/seaborn</li>
            <li>Results are <strong>written back</strong> as new sheets in your Excel file</li>
            <li><strong>Download</strong> the enriched workbook with all insights</li>
        </ol>
    </div>

    <div class="footer">
        AI Vibe Coding Demo — Built with FastAPI + pandas + numpy + openpyxl
    </div>

    <script>
        function setPrompt(text) { document.getElementById('prompt').value = text; }

        document.getElementById('uploadForm').onsubmit = async function(e) {
            e.preventDefault();
            const btn = document.getElementById('submitBtn');
            const status = document.getElementById('status');
            btn.disabled = true;
            status.innerHTML = '<p>⏳ Analysing your data... (this may take a moment)</p>';

            const formData = new FormData();
            formData.append('file', document.getElementById('file').files[0]);
            formData.append('prompt', document.getElementById('prompt').value);

            try {
                const resp = await fetch('/analyse', { method: 'POST', body: formData });
                if (!resp.ok) {
                    const err = await resp.json();
                    throw new Error(err.detail || 'Analysis failed');
                }
                const blob = await resp.blob();
                const url = URL.createObjectURL(blob);
                const filename = resp.headers.get('X-Filename') || 'analysed_output.xlsx';
                status.innerHTML = `✅ <a href="${url}" download="${filename}">Download ${filename}</a> — your enriched workbook is ready!`;
            } catch (err) {
                status.innerHTML = `<div class="error">❌ ${err.message}</div>`;
            } finally {
                btn.disabled = false;
            }
        };
    </script>
</body>
</html>
"""

# ── AI Prompt → Code Engine (Demo) ────────────────────────────────────
# In production, this would call GPT-4 / Claude to translate user intent
# into executable Python. Here we match keywords as a proof of concept.

PROMPT_ROUTINES = {
    "category": "category_region_analysis",
    "region": "category_region_analysis",
    "pivot": "pivot_tables",
    "monthly": "monthly_trends",
    "profit": "profit_analysis",
    "trend": "monthly_trends",
    "top": "top_products",
    "product": "top_products",
    "correlation": "correlation",
    "heatmap": "correlation",
    "statistics": "summary_stats",
    "summary": "summary_stats",
    "segment": "segment_analysis",
    "customer": "segment_analysis",
    "discount": "discount_analysis",
    "shipping": "shipping_analysis",
    "payment": "payment_analysis",
}


def interpret_prompt(prompt: str) -> list[str]:
    prompt_lower = prompt.lower()
    matched = set()
    for keyword, routine in PROMPT_ROUTINES.items():
        if keyword in prompt_lower:
            matched.add(routine)
    return list(matched) if matched else ["summary_stats"]


def run_analysis(df: pd.DataFrame, prompt: str, filepath: Path) -> Path:
    """Execute analysis routines based on interpreted prompt."""
    routines = interpret_prompt(prompt)
    output_path = filepath.parent / f"analysed_{filepath.name}"

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        # Always copy original data
        df.to_excel(writer, sheet_name="Original_Data", index=False)

        for routine in routines:
            try:
                if routine == "category_region_analysis":
                    _category_region(df, writer)
                elif routine == "pivot_tables":
                    _pivot_tables(df, writer)
                elif routine == "monthly_trends":
                    _monthly_trends(df, writer)
                elif routine == "profit_analysis":
                    _profit_analysis(df, writer)
                elif routine == "top_products":
                    _top_products(df, writer)
                elif routine == "correlation":
                    _correlation(df, writer)
                elif routine == "summary_stats":
                    _summary_stats(df, writer)
                elif routine == "segment_analysis":
                    _segment_analysis(df, writer)
                elif routine == "discount_analysis":
                    _discount_analysis(df, writer)
                elif routine == "shipping_analysis":
                    _shipping_analysis(df, writer)
                elif routine == "payment_analysis":
                    _payment_analysis(df, writer)
            except Exception as e:
                print(f"  ⚠️  Routine '{routine}' failed: {e}")

    return output_path


# ── Analysis Routines ──────────────────────────────────────────────────

def _category_region(df, writer):
    cr = df.groupby(["Category", "Region"]).agg(
        TotalSales=("Sales", "sum"), TotalProfit=("Profit", "sum"), OrderCount=("OrderID", "nunique")
    ).reset_index()
    cr.to_excel(writer, sheet_name="Category_x_Region", index=False)

    pivot = df.pivot_table(values="Sales", index="Region", columns="Category", aggfunc="sum", margins=True, margins_name="Total").round(2)
    pivot.to_excel(writer, sheet_name="Pivot_Category_Region")


def _pivot_tables(df, writer):
    if "Segment" in df.columns and "ShippingMode" in df.columns:
        p1 = df.pivot_table(values="Profit", index="Segment", columns="ShippingMode", aggfunc="mean", margins=True).round(2)
        p1.to_excel(writer, sheet_name="Pivot_Segment_Shipping")
    if "Country" in df.columns and "Category" in df.columns:
        p2 = df.pivot_table(values="Sales", index="Country", columns="Category", aggfunc="sum", margins=True, margins_name="Total").round(2)
        p2.to_excel(writer, sheet_name="Pivot_Country_Category")


def _monthly_trends(df, writer):
    if "OrderDate" not in df.columns:
        return
    temp = df.copy()
    temp["YearMonth"] = temp["OrderDate"].dt.to_period("M").astype(str)
    monthly = temp.groupby("YearMonth").agg(
        TotalSales=("Sales", "sum"), TotalProfit=("Profit", "sum"), OrderCount=("OrderID", "nunique")
    ).reset_index()
    monthly.to_excel(writer, sheet_name="Monthly_Trends", index=False)


def _profit_analysis(df, writer):
    cats = df.groupby("Category").agg(
        TotalSales=("Sales", "sum"), TotalProfit=("Profit", "sum"), OrderCount=("OrderID", "nunique")
    ).reset_index()
    cats["ProfitMargin"] = (cats["TotalProfit"] / cats["TotalSales"] * 100).round(1)
    cats.to_excel(writer, sheet_name="Profit_by_Category", index=False)


def _top_products(df, writer):
    if "ProductName" not in df.columns:
        return
    prods = df.groupby(["Category", "ProductName"]).agg(
        TotalSales=("Sales", "sum"), TotalProfit=("Profit", "sum"), QuantitySold=("Quantity", "sum")
    ).reset_index()
    prods["ProfitMargin"] = (prods["TotalProfit"] / prods["TotalSales"] * 100).round(1)
    top = prods.nlargest(20, "TotalSales")
    top.to_excel(writer, sheet_name="Top20_Products", index=False)


def _correlation(df, writer):
    num_cols = [c for c in ["Sales", "Profit", "Quantity", "Discount", "UnitPrice", "ShippingCost"] if c in df.columns]
    if len(num_cols) >= 2:
        corr = df[num_cols].corr().reset_index()
        corr.to_excel(writer, sheet_name="Correlation_Matrix", index=False)


def _summary_stats(df, writer):
    desc = df.describe(include="all").T.reset_index()
    desc.to_excel(writer, sheet_name="Summary_Stats", index=False)

    info = pd.DataFrame({
        "Column": df.dtypes.index,
        "DataType": df.dtypes.values,
        "NonNullCount": df.count().values,
        "NullCount": df.isnull().sum().values,
        "NullPercent": (df.isnull().sum() / len(df) * 100).round(2).values,
        "UniqueCount": [df[c].nunique() if df[c].dtype == "object" else "" for c in df.columns],
    })
    info.to_excel(writer, sheet_name="Column_Info", index=False)


def _segment_analysis(df, writer):
    if "Segment" not in df.columns:
        return
    seg = df.groupby("Segment").agg(
        TotalSales=("Sales", "sum"), TotalProfit=("Profit", "sum"), OrderCount=("OrderID", "nunique"), AvgOrderValue=("Sales", "mean")
    ).reset_index()
    seg["ProfitMargin"] = (seg["TotalProfit"] / seg["TotalSales"] * 100).round(1)
    seg.to_excel(writer, sheet_name="Segment_Analysis", index=False)


def _discount_analysis(df, writer):
    if "Discount" not in df.columns:
        return
    def bracket(d):
        if d == 0: return "0%"
        elif d <= 0.10: return "1-10%"
        elif d <= 0.20: return "11-20%"
        else: return "21-30%"
    temp = df.copy()
    temp["DiscountBracket"] = temp["Discount"].apply(bracket)
    da = temp.groupby("DiscountBracket").agg(
        OrderCount=("OrderID", "nunique"), TotalSales=("Sales", "sum"), TotalProfit=("Profit", "sum")
    ).reset_index()
    da["ProfitMargin"] = (da["TotalProfit"] / da["TotalSales"] * 100).round(1)
    da.to_excel(writer, sheet_name="Discount_Analysis", index=False)


def _shipping_analysis(df, writer):
    if "ShippingMode" not in df.columns:
        return
    sh = df.groupby("ShippingMode").agg(
        TotalSales=("Sales", "sum"), TotalProfit=("Profit", "sum"), OrderCount=("OrderID", "nunique")
    ).reset_index()
    sh.to_excel(writer, sheet_name="Shipping_Analysis", index=False)


def _payment_analysis(df, writer):
    if "PaymentMethod" not in df.columns:
        return
    pm = df.groupby("PaymentMethod").agg(
        TotalSales=("Sales", "sum"), TotalProfit=("Profit", "sum"), OrderCount=("OrderID", "nunique")
    ).reset_index()
    pm.to_excel(writer, sheet_name="Payment_Analysis", index=False)


# ── Endpoints ──────────────────────────────────────────────────────────

@app.get("/")
async def root():
    return HTMLResponse(content=HTML_PAGE, media_type="text/html")


@app.post("/analyse")
async def analyse(file: UploadFile = File(...), prompt: str = Form(...)):
    if not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(400, "Please upload an Excel file (.xlsx or .xls)")

    # Read uploaded file
    content = await file.read()
    try:
        df = pd.read_excel(io.BytesIO(content))
    except Exception as e:
        raise HTTPException(400, f"Could not read Excel file: {e}")

    if df.empty:
        raise HTTPException(400, "The uploaded Excel file is empty")

    # Save temporarily
    uid = uuid.uuid4().hex[:8]
    temp_path = TEMP_DIR / f"upload_{uid}_{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(content)

    # Run analysis
    try:
        output_path = run_analysis(df, prompt, temp_path)
    except Exception as e:
        raise HTTPException(500, f"Analysis failed: {e}")
    finally:
        temp_path.unlink(missing_ok=True)

    # Return result
    filename = output_path.name
    return FileResponse(
        path=output_path,
        filename=filename,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"X-Filename": filename},
    )


@app.get("/health")
async def health():
    return {"status": "ok", "service": "AI Vibe Coding — Excel Analysis"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)



