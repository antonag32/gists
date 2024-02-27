"""Convert a CSV file to Odoo statements which can be run in a scheduled action to update the given records"""
import argparse
import csv
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    args = parser.parse_args()

    csv_file = Path(args.file).expanduser().absolute()
    table_name = Path(args.file).stem.replace(".", "_")
    with open(csv_file, "r", encoding="utf-8") as csv_fd:
        reader = csv.reader(csv_fd)
        columns = next(reader)[1:]
        for row in reader:
            for field, val in zip(columns, row[1:]):
                sql_sentence = f"UPDATE {table_name} SET backup_{field} = '{val}' WHERE id = {row[0]}"
                odoo_command = f'env.cr.execute("{sql_sentence}")'
                print(odoo_command)


if __name__ == "__main__":
    main()
