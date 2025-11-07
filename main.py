import argparse
from models.report import ALLOWED_REPORTS
from utils.process_files import process_files


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
        choices=ALLOWED_REPORTS.keys(),
        required=True,
        help=f'Report type. Allowed values: {", ".join(ALLOWED_REPORTS)}'
    )

    args = parser.parse_args()

    process_files(args.files, args.report)

if __name__ == "__main__":
    main()