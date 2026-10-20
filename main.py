import os
from processor import process_sales_data
from report import generate_report


def main():
    # find paths relative to this script so it works from any directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, "data", "sales_data.csv")
    output_path = os.path.join(base_dir, "output", "summary_report.txt")

    # step 1: process data (no printing inside processor)
    results = process_sales_data(data_path)

    # step 2: display and save the formatted summary report
    generate_report(results, output_path)


if __name__ == "__main__":
    main()
