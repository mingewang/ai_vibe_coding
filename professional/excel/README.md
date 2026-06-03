# AI Vibe Coding — Excel Data Analysis

A complete demonstration of how AI-assisted coding ("vibe coding") transforms Excel data analysis. Describe what you want in plain English — AI generates the Python code, insights flow back into Excel automatically.

## Contents

| File | Description |
|------|-------------|
| `generate_sales_data.py` | Generates a realistic 5,000-row sales Excel workbook (7 sheets) |
| `ai_vibe_excel_tutorial.ipynb` | Jupyter notebook with 10 AI prompts + full analysis |
| `sales_data.xlsx` | Sample output (generated) |
| `requirements.txt` | Python dependencies |
| `service/app.py` | FastAPI web service for the upload-analyse-download flow |
| `service/requirements.txt` | Service dependencies |

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Generate sample sales data
python generate_sales_data.py

# 3. Launch the Jupyter notebook tutorial
jupyter notebook ai_vibe_excel_tutorial.ipynb
```

Run all cells in the notebook to see AI-generated code analyse the data, produce charts and pivot tables, and write results back to `sales_data_analyzed.xlsx` (18 sheets).

## The AI Vibe Coding Flow

```
Your Prompt (English)  →  AI Generates Python  →  Your Data  →  Enriched Excel
```

**Example prompts to try** (copy these into ChatGPT / Claude / Gemini):

1. *"Load the Orders sheet, show me basic statistics and check for missing values."*
2. *"Plot monthly sales and profit trends on a dual-axis chart."*
3. *"Create a grouped bar chart of sales by Category and Region."*
4. *"Build a pivot table: Region as rows, Category as columns, sum of Sales as values."*
5. *"Analyse discount impact — group discounts into brackets and show profit margin per bracket."*
6. *"Create a correlation heatmap of Sales, Profit, Quantity, Discount."*
7. *"Write all analysis results to new sheets in the Excel file."*

## Web Service Demo

The FastAPI service provides an upload-analyse-download experience:

```bash
cd service
pip install -r requirements.txt
uvicorn app:app --reload
# Open http://localhost:8000
```

Upload any Excel file, type your question in natural language, and download the enriched workbook. The service demonstrates the architecture; in production the AI prompt→code translation would use GPT-4/Claude.

## Architecture

```
                         ┌──────────────────────┐
                         │   User Prompt (NLP)   │
                         └──────────┬───────────┘
                                    │
                         ┌──────────▼───────────┐
                         │  AI Prompt Interpreter │
                         │  (Keyword matching /   │
                         │   LLM in production)   │
                         └──────────┬───────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
            ┌──────────┐   ┌──────────────┐   ┌──────────┐
            │ pandas   │   │  numpy       │   │ seaborn  │
            │ (tables) │   │ (statistics) │   │ (charts) │
            └────┬─────┘   └──────┬───────┘   └────┬─────┘
                 │               │                │
                 └───────────────┼────────────────┘
                                 ▼
                    ┌──────────────────────┐
                    │  openpyxl writes      │
                    │  results to new sheets│
                    └──────────────────────┘
                                 │
                                 ▼
                    ┌──────────────────────┐
                    │  Enriched Excel file  │
                    │  (original + insights)│
                    └──────────────────────┘
```

## Why This Matters

- **Speed**: Go from question to insight in seconds, not hours
- **Accessibility**: No need to memorise pandas/numpy syntax
- **Iteration**: Change one word in your prompt to explore a different angle
- **Integration**: Results land right back in Excel — your team's existing workflow
