import csv

from tabulate import tabulate

from models.product import Product
from models.report import AverageReport


def process_files(file_paths, report_type):
    """Download files data and generate a report."""
    all_rows = []

    # 1. All files data downloading
    for file_path in file_paths:
        try:
            with open(f"data/{file_path}", newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    try:
                        all_rows.append(Product.from_dict(row))
                    except ValueError:
                        continue
        except FileNotFoundError:
            print(f"Error: There is no file on path: {file_path}")
            return
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return

    # 2. Report generation
    table_data = None
    report_data = None
    avg_report = AverageReport(report_type)
    header = ["Brand", report_type.capitalize().replace('-', ' ')]
    report_data = avg_report.calculate_average_values(all_rows)
    if report_data:
        table_data = [[brand, value] for brand, value in report_data.items()]
        print(f"\n--- Report: {header[1]} ---")
        print(tabulate(table_data, headers=header, tablefmt="fancy_grid"))
    else:
        print("No data for this report.")
