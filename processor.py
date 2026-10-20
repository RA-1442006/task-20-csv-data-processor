import csv
import os


def to_number(value, num_type=float):
    # helper to safely turn text into numbers, returns None if it fails
    if value is None:
        return None
    cleaned = value.strip()
    if not cleaned:
        return None
    try:
        num = num_type(cleaned)
        # in our dataset, negative units, prices, or salaries are invalid
        if num < 0:
            return None
        return num
    except (ValueError, TypeError):
        return None


def process_sales_data(filepath):
    # check if file exists before trying to open it
    if not os.path.exists(filepath):
        return {"error": f"File not found at '{filepath}'"}

    total_rows = 0
    valid_rows = 0
    skipped_rows = 0

    total_revenue = 0.0
    total_units_sold = 0
    total_salary = 0.0
    salary_count = 0

    highest_revenue_row = None
    lowest_revenue_row = None

    product_sales = {}
    dept_counts = {}
    region_counts = {}
    field_issues = {}

    try:
        with open(filepath, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            # check if file is empty or missing headers
            if not reader.fieldnames:
                return {"error": "The CSV file is empty or missing a header row."}

            for row in reader:
                total_rows += 1
                row_has_error = False

                # validate numeric fields
                units = to_number(row.get("units_sold"), int)
                if units is None:
                    row_has_error = True
                    field_issues["units_sold"] = field_issues.get("units_sold", 0) + 1

                price = to_number(row.get("unit_price"), float)
                if price is None:
                    row_has_error = True
                    field_issues["unit_price"] = field_issues.get("unit_price", 0) + 1

                salary = to_number(row.get("salary"), float)
                if salary is None:
                    row_has_error = True
                    field_issues["salary"] = field_issues.get("salary", 0) + 1

                # if any number was bad or missing, skip this row
                if row_has_error:
                    skipped_rows += 1
                    continue

                valid_rows += 1

                # calculations for revenue and units
                revenue = units * price
                total_revenue += revenue
                total_units_sold += units

                # track salary for average
                total_salary += salary
                salary_count += 1

                # clean record summary for high/low comparison
                record = {
                    "id": row.get("id", "").strip(),
                    "name": row.get("name", "").strip(),
                    "department": row.get("department", "").strip(),
                    "region": row.get("region", "").strip(),
                    "product": row.get("product", "").strip(),
                    "units_sold": units,
                    "unit_price": price,
                    "revenue": revenue,
                    "salary": salary,
                }

                # check highest and lowest revenue
                if highest_revenue_row is None or revenue > highest_revenue_row["revenue"]:
                    highest_revenue_row = record

                if lowest_revenue_row is None or revenue < lowest_revenue_row["revenue"]:
                    lowest_revenue_row = record

                # track units per product to find top seller
                prod = record["product"]
                product_sales[prod] = product_sales.get(prod, 0) + units

                # count records per department and region
                dept = record["department"]
                dept_counts[dept] = dept_counts.get(dept, 0) + 1

                reg = record["region"]
                region_counts[reg] = region_counts.get(reg, 0) + 1

    except Exception as e:
        return {"error": f"Failed to read CSV: {e}"}

    if total_rows == 0:
        return {"error": "The CSV file contains no data rows."}

    # calculate average salary
    avg_salary = (total_salary / salary_count) if salary_count > 0 else 0.0

    # find top selling product
    top_product = None
    top_product_units = 0
    if product_sales:
        top_product = max(product_sales, key=product_sales.get)
        top_product_units = product_sales[top_product]

    return {
        "total_rows": total_rows,
        "valid_rows": valid_rows,
        "skipped_rows": skipped_rows,
        "field_issues": field_issues,
        "total_revenue": total_revenue,
        "total_units_sold": total_units_sold,
        "average_salary": avg_salary,
        "highest_revenue_row": highest_revenue_row,
        "lowest_revenue_row": lowest_revenue_row,
        "top_selling_product": top_product,
        "top_product_units": top_product_units,
        "product_sales": product_sales,
        "department_counts": dept_counts,
        "region_counts": region_counts,
    }
