import builtins
from unittest.mock import patch, mock_open


from models.product import Product
from models.report import AverageReport
from utils.process_files import process_files

MOCK_CSV_DATA_1 = (
    "brand,name,rating,price\n"
    "BrandA,Item1,4.5,100\n"
    "BrandB,Item2,3.0,200\n"
    "BrandA,Item3,5.0,150\n"
)

MOCK_CSV_DATA_2 = (
    "brand,name,rating,price\n"
    "BrandB,Item4,4.0,250\n"
    "BrandC,Item5,2.0,50\n"
    "BrandC,Item6,3.0,50\n"
)

TEST_DATA = [
    {"brand": 'smart', "price": '160', "model": 'x1', "rating": '5.2'}, # rating (5.2 + 3.2 + 5.0) / 3 = 4,46
    {"brand": 'simple', "price": '100', "model": 'e2', "rating": '1.3'}, # rating (1.3 + 2.3 + 0.3) / 3 = 1,3
    {"brand": 'medium', "price": '140', "model": 'q2', "rating": '3.4'}, # rating (3.4 + 3.3) / 2 = 3.35
    {"brand": 'smart', "price": '168', "model": 'x2', "rating": '3.2'}, # price (160 + 168 + 122) / 3 = 150
    {"brand": 'simple', "price": '101', "model": 'e3', "rating": '2.3'}, # price (101 + 100 + 102) / 3 = 101
    {"brand": 'medium', "price": '150', "model": 'q3', "rating": '3.3'}, # price (140 + 150) / 2 = 145
    {"brand": 'smart', "price": '122', "model": 'x3', "rating": '5.0'},
    {"brand": 'simple', "price": '102', "model": 'e3', "rating": '0.3'},
    ]


MOCK_ROWS = [
    {'brand': 'BrandA', 'name': 'Item1', 'rating': '4.5', 'price': '100'},
    {'brand': 'BrandB', 'name': 'Item2', 'rating': '3.0', 'price': '200'},
    {'brand': 'BrandA', 'name': 'Item3', 'rating': '5.0', 'price': '150'},
    {'brand': 'BrandB', 'name': 'Item4', 'rating': '4.0', 'price': '250'},
    {'brand': 'BrandC', 'name': 'Item5', 'rating': '2.0', 'price': '50'},
    {'brand': 'BrandC', 'name': 'Item6', 'rating': '3.0', 'price': '50'},
]

def prod_creation(data):
    products = [Product.from_dict(row) for row in data]
    return products

def test_calculate_average_rating():
    expected = {'smart': 4.5, 'medium': 3.3, 'simple': 1.3}
    avg_report = AverageReport("average-rating")
    average_values = avg_report.calculate_average_values(prod_creation(TEST_DATA))
    assert average_values == expected

def test_calculate_average_price():
    expected = {'smart': 150, 'medium': 145, 'simple': 101}
    avg_report = AverageReport("average-price-in-brand")
    average_values = avg_report.calculate_average_values(prod_creation(TEST_DATA))
    assert average_values == expected

def test_calculate_with_missing_or_invalid_data():
    invalid_rows = [
        {'brand': 'Valid', 'rating': '4.0', 'price': '10'},
        {'brand': 'InvalidRating', 'rating': 'N/A', 'price': '20'}, # Пропуск
        {'brand': 'InvalidPrice', 'rating': '3.0', 'price': 'free'}, # Пропуск цены
        {'name': 'NoBrand', 'rating': '5.0', 'price': '50'}, # Пропуск бренда
    ]
    avg_report = AverageReport("average-rating")
    avg_report2 = AverageReport("average-price-in-brand")

    assert avg_report.calculate_average_values(prod_creation(invalid_rows)) == {'Valid': 4.0}
    assert avg_report2.calculate_average_values(prod_creation(invalid_rows)) == {'Valid': 10.0}

## File reading tests

MOCK_FILE_CONTENT = {
    'data/products1.csv': MOCK_CSV_DATA_1,
    'products2.csv': MOCK_CSV_DATA_2,
}

@patch('builtins.open', new_callable=mock_open)
@patch('builtins.print')
@patch('utils.process_files.tabulate', return_value="MOCKED_TABLE_OUTPUT")
def test_process_files_one_file(mock_tabulate, mock_print, mock_file):
    """One file handle and report generation."""
    mock_file.side_effect = lambda f, *args, **kwargs: mock_open(read_data=MOCK_CSV_DATA_1).return_value
    process_files(['products1.csv'], 'average-rating')
    mock_file.assert_called_once_with('data/products1.csv', newline='', encoding='utf-8')
    mock_tabulate.assert_called_once()
    mock_print.assert_any_call("MOCKED_TABLE_OUTPUT")


@patch('builtins.open', side_effect=FileNotFoundError)
@patch('builtins.print')
def test_process_files_not_found(mock_print, mock_file):
    """Error FileNotFoundError handler."""
    process_files(['nonexistent.csv'], 'average-rating')
    mock_print.assert_called_with('Error: There is no file on path: nonexistent.csv')