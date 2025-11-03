import argparse
import csv
import os
from tabulate import tabulate

ALLOWED_REPORTS = ["average-rating", "average-price-in-brand"]

def calculate_average_values(rows, report_claim):
    """Calculates the average rating of a given row."""
    brand_data = {}
    for row in rows:
        try:
            brand = row.get("brand")
            rating = float(row.get("rating"))
            price = float(row.get("price"))
            if brand and rating and price:
                if report_claim == ALLOWED_REPORTS[0]:
                    if brand not in brand_data:
                        brand_data[brand] = []
                    brand_data[brand].append(rating)
                elif report_claim == ALLOWED_REPORTS[1]:
                    if brand not in brand_data:
                        brand_data[brand] = []
                    brand_data[brand].append(price)
            else:
                continue
        except ValueError:
            continue

    result_dict = {}
    for brand, average_res in brand_data.items():
        if average_res:
            avg = sum(average_res) / len(average_res)
            result_dict[brand] = round(avg, 1)

    return dict(sorted(result_dict.items(), key=lambda item: item[1], reverse=True))


def process_files(file_paths, report_type):
    """Download files data and generate a report."""
    all_rows = []

    # 1. All files data downloading
    for file_path in file_paths:
        try:
            with open(f"data/{file_path}", newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    all_rows.append(row)
        except FileNotFoundError:
            print(f"Error: There is no file on path: {file_path}")
            return
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return

    # 2. Report generation
    report_data = None
    header = None

    if report_type == "average-rating":
        report_data = calculate_average_values(all_rows, "average-rating")
        header = ["Brand", "Average rating"]
    elif report_type == "average-price-in-brand":
        report_data = calculate_average_values(all_rows, "average-price-in-brand")
        header = ["Brand", "Average price in brand"]
    else:
        print(f"Error: Unexpected report type: {report_type}")
        return

    if report_data:
        table_data = [[brand, value] for brand, value in report_data.items()]
        print(f"\n--- Report: {report_type} ---")
        print(tabulate(table_data, headers=header, tablefmt="fancy_grid"))
    else:
        print("No data for this report.")

def main():
    """Main handler func."""
    parser = argparse.ArgumentParser(
        description="Script to analyze data from CSV files."
    )

    parser.add_argument(
        '--files',
        nargs='+',
        required=True,
        help='file list(for example: products1.csv products2.csv)'
    )

    parser.add_argument(
        '--report',
        choices=ALLOWED_REPORTS,
        required=True,
        help=f'Report type. Allowed values: {", ".join(ALLOWED_REPORTS)}'
    )

    args = parser.parse_args()

    process_files(args.files, args.report)

if __name__ == "__main__":
    main()