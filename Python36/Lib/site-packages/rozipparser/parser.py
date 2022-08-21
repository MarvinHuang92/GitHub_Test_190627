import argparse
import csv

from rozipparser.codeparser import CodeParser

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Import Romanian postal codes from official xls files")
    parser.add_argument("input", metavar="input", type=str, help="path to xls file")
    parser.add_argument("--csv", dest="csv_filename", type=str, help="path to output csv file")

    args = parser.parse_args()

    parser = CodeParser(args.input)
    codes = parser.get_codes()

    if "csv_filename" in args:
        with open(args.csv_filename, "w", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["county", "locality", "sector", "street", "house_number", "zip_code", "street_type"])
            writer.writerows((x.to_list() for x in codes))
