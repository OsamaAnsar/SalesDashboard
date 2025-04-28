from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS
from datetime import datetime, timedelta
import random

app = Flask(__name__)
CORS(app)

# ------------------------ Config ------------------------
SALES_LEDGER = 'Sales Ledger.xlsx'  # Your sales ledger file path
company_name = "Fangtooth Technologies Inc."
currency = "CAD"
denomination = "$"
current_date_input = "2023-12-31"
fiscal_year_input = "2023-03-31"

# ------------------------ Dates ------------------------
current_date = pd.to_datetime(current_date_input)
fiscal_year_end = pd.to_datetime(fiscal_year_input)
fiscal_month = fiscal_year_end.month
fiscal_day = fiscal_year_end.day

# ------------------------ Load Data ------------------------
data = pd.read_excel(SALES_LEDGER)
data['Date'] = pd.to_datetime(data['Date'])
data_all = data.copy()

# ------------------------ Utilities ------------------------
def get_fiscal_year(date):
    fiscal_end = datetime(date.year, fiscal_month, fiscal_day)
    return date.year if date <= fiscal_end else date.year + 1

def fiscal_year_label(date):
    return f"F{get_fiscal_year(date)}"

# ------------------------ Preprocessing ------------------------
data_all['Fiscal Year'] = data_all['Date'].apply(fiscal_year_label)
data_all['Month'] = data_all['Date'].dt.to_period('M').dt.to_timestamp()

full_fiscal_years = data_all.groupby('Fiscal Year')['Month'].nunique() == 12
fiscal_years = full_fiscal_years[full_fiscal_years].index.tolist()
data_full = data_all[data_all['Fiscal Year'].isin(fiscal_years)]
fiscal_periods = sorted(fiscal_years)

# ------------------------ Filter Lists ------------------------
def clean_column(col):
    return sorted(
        data_all[col]
        .dropna()
        .astype(str)
        .str.strip()
        .unique()
        .tolist()
    )

available_filters = {
    "currencies": clean_column("Original Currency (CAD)"),
    "customers": clean_column("Customer"),
    "locations": clean_column("Location"),
    "companies": clean_column("Company"),
}

# ------------------------ Aggregation ------------------------
products = data_all['Account Name'].dropna().unique().tolist()

def aggregate_monthly(df, period_name):
    if df.empty:
        return {}

    df['Month'] = df['Date'].dt.to_period('M').dt.to_timestamp()
    grouped = df.groupby(['Month', 'Account Name'])

    month_product_data = {}

    for (month, product), group in grouped:
        if month not in month_product_data:
            month_product_data[month] = {}
        month_product_data[month][product] = [
            {
                "Amount": float(row["Amount"]),
                "Customer": row["Customer"],
                "Location": row["Location"],
                "Currency": row["Original Currency (CAD)"]
            }
            for _, row in group.iterrows()
        ]

    # Now sort months properly
    ordered_months = dict(sorted(month_product_data.items()))
    # Build final structure
    final_result = {period_name: {}}
    for month, products in ordered_months.items():
        month_label = month.strftime("%B %Y")  # Convert only now
        final_result[period_name][month_label] = products

    return final_result

# ------------------------ Period Definitions ------------------------
ltm_start = current_date - pd.DateOffset(years=1)
ltm_data = data_all.loc[(data_all['Date'] >= ltm_start) & (data_all['Date'] <= current_date)].copy()

current_fiscal_start = datetime(get_fiscal_year(current_date) - 1, fiscal_month, fiscal_day) + timedelta(days=1)
ytd_data = data_all.loc[(data_all['Date'] >= current_fiscal_start) & (data_all['Date'] <= current_date)].copy()

# ------------------------ API Route ------------------------
@app.route('/api/sales-data', methods=['GET'])
def get_sales_data():
    period = request.args.get('period', 'YTD')
    filter_currency = request.args.get('currency', 'CAD')
    filter_customer = request.args.get('customer')
    filter_location = request.args.get('location')
    filter_company = request.args.get('company')
    start_date = request.args.get('startDate')
    end_date = request.args.get('endDate')

    filtered_data = data_all.copy()

    # Apply standard filters
    if filter_currency:
        filtered_data = filtered_data[filtered_data['Original Currency (CAD)'] == filter_currency]

    if filter_customer:
        filtered_data = filtered_data[filtered_data['Customer'].str.contains(filter_customer, case=False, na=False)]

    if filter_location:
        filter_location = filter_location.strip().lower()
        filtered_data = filtered_data[filtered_data['Location'].str.contains(filter_location, case=False, na=False)]

    if filter_company:
        filtered_data = filtered_data[filtered_data['Company'].str.contains(filter_company, case=False, na=False)]

    # Apply date range filter
    if start_date:
        try:
            start_date_parsed = pd.to_datetime(start_date)
            filtered_data = filtered_data[filtered_data['Date'] >= start_date_parsed]
        except Exception as e:
            return jsonify({"error": f"Invalid startDate format: {str(e)}"}), 400

    if end_date:
        try:
            end_date_parsed = pd.to_datetime(end_date)
            filtered_data = filtered_data[filtered_data['Date'] <= end_date_parsed]
        except Exception as e:
            return jsonify({"error": f"Invalid endDate format: {str(e)}"}), 400

    # Period Aggregation
    period_data = {}

    if period == 'YTD':
        current_fiscal_start = datetime(get_fiscal_year(current_date) - 1, fiscal_month, fiscal_day) + timedelta(days=1)
        ytd_filtered = filtered_data[(filtered_data['Date'] >= current_fiscal_start) & (filtered_data['Date'] <= current_date)]
        period_data = aggregate_monthly(ytd_filtered, f"YTD F{get_fiscal_year(current_date)}")

    elif period.startswith('F'):
        fy = period
        fy_filtered = filtered_data[filtered_data['Fiscal Year'] == fy]
        period_data = aggregate_monthly(fy_filtered, fy)

    elif period.startswith('LTM'):
        ltm_start = current_date - pd.DateOffset(years=1)
        ltm_filtered = filtered_data[(filtered_data['Date'] >= ltm_start) & (filtered_data['Date'] <= current_date)]
        period_data = aggregate_monthly(ltm_filtered, f"LTM {current_date.strftime('%b %Y')}")

    else:
        return jsonify({"error": "Invalid period type"}), 400

    result = {
        "company_name": filter_company if filter_company else data_all['Company'].iloc[0],
        "currency": filter_currency,
        "denomination": denomination,
        "chart_title": "Monthly Sales by Product",
        "default_colors": {
            "primary": "#104861",
            "secondary": "#DDDDDD",
            "tertiary": "#83CCEB"
        },
        "product_colors": {
            product: f"#{random.randint(0, 0xFFFFFF):06x}" for product in products
        },
        "meta": {
            "customers": available_filters["customers"],
            "currencies": available_filters["currencies"],
            "locations": available_filters["locations"],
            "companies": available_filters["companies"],
        },
        "periods": period_data
    }

    return jsonify(result)

# ------------------------ Run App ------------------------
if __name__ == '__main__':
    app.run(debug=True)
