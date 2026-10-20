import os


def format_report(results):
    # build a clean, aligned text report from the results dictionary
    lines = []
    divider = "=" * 55
    sub_divider = "-" * 55

    lines.append(divider)
    lines.append("              SALES DATA SUMMARY REPORT")
    lines.append(divider)
    lines.append("")

    # overview section
    lines.append("DATASET OVERVIEW")
    lines.append(sub_divider)
    lines.append(f"{'Total rows read':<28}: {results['total_rows']}")
    lines.append(f"{'Valid records processed':<28}: {results['valid_rows']}")
    lines.append(f"{'Skipped / invalid rows':<28}: {results['skipped_rows']}")
    lines.append("")

    # financial & sales metrics
    lines.append("SALES & REVENUE METRICS")
    lines.append(sub_divider)
    lines.append(f"{'Total revenue':<28}: ${results['total_revenue']:,.2f}")
    lines.append(f"{'Total units sold':<28}: {results['total_units_sold']:,}")
    lines.append(f"{'Average salary':<28}: ${results['average_salary']:,.2f}")

    top_prod = results.get("top_selling_product", "N/A")
    top_units = results.get("top_product_units", 0)
    lines.append(f"{'Top-selling product':<28}: {top_prod} ({top_units} units)")
    lines.append("")

    # highest & lowest performers
    lines.append("HIGHLIGHTS (HIGHEST & LOWEST REVENUE)")
    lines.append(sub_divider)
    high = results.get("highest_revenue_row")
    if high:
        high_str = f"{high['name']} ({high['product']}) - ${high['revenue']:,.2f}"
    else:
        high_str = "None"
    lines.append(f"{'Highest revenue row':<28}: {high_str}")

    low = results.get("lowest_revenue_row")
    if low:
        low_str = f"{low['name']} ({low['product']}) - ${low['revenue']:,.2f}"
    else:
        low_str = "None"
    lines.append(f"{'Lowest revenue row':<28}: {low_str}")
    lines.append("")

    # department counts
    lines.append("RECORDS PER DEPARTMENT")
    lines.append(sub_divider)
    dept_counts = results.get("department_counts", {})
    if dept_counts:
        for dept, count in sorted(dept_counts.items(), key=lambda x: x[1], reverse=True):
            lines.append(f"{dept:<28}: {count}")
    else:
        lines.append("No department records found.")
    lines.append("")

    # region counts
    lines.append("RECORDS PER REGION")
    lines.append(sub_divider)
    region_counts = results.get("region_counts", {})
    if region_counts:
        for region, count in sorted(region_counts.items(), key=lambda x: x[1], reverse=True):
            lines.append(f"{region:<28}: {count}")
    else:
        lines.append("No region records found.")
    lines.append("")

    # data quality and skipped issues
    lines.append("DATA QUALITY ISSUES")
    lines.append(sub_divider)
    field_issues = results.get("field_issues", {})
    if field_issues:
        lines.append(f"{'Total rows with issues':<28}: {results['skipped_rows']}")
        for field, count in field_issues.items():
            lines.append(f"  - Invalid/missing {field:<12}: {count} row(s)")
    else:
        lines.append("All rows were clean with no issues.")

    lines.append(divider)
    return "\n".join(lines)


def generate_report(results, output_path=None):
    # check for error message from processing
    if "error" in results:
        error_msg = f"[ERROR] Could not generate report: {results['error']}"
        print(error_msg)
        return

    # format report
    report_text = format_report(results)

    # print to console
    print(report_text)

    # write to output file if path is given
    if output_path:
        out_dir = os.path.dirname(output_path)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)

        with open(output_path, mode="w", encoding="utf-8") as f:
            f.write(report_text + "\n")
