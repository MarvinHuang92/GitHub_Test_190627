from openpyxl import load_workbook

from rozipparser.model import Code


class CodeParser:
    def __init__(self, filename):
        self.__filename = filename
        self.codes = []

    def get_codes(self):
        workbook = load_workbook(filename=self.__filename, read_only=True)

        for worksheet in workbook:
            self.codes += self.__parse_worksheet(worksheet)
        return self.codes

    def __parse_worksheet(self, worksheet):
        codes = []

        next(worksheet.rows)

        # TODO: Parallelize
        for row in worksheet.rows:
            county = "Bucuresti" if self.__is_bucharest_worksheet(worksheet) else row[0].value \
                if self.__is_large_locality_worksheet(worksheet) else row[1].value
            locality = "Bucuresti" if self.__is_bucharest_worksheet(worksheet) else row[1].value \
                if self.__is_large_locality_worksheet(worksheet) else row[2].value
            sector = row[4].value if self.__is_bucharest_worksheet(worksheet) else None
            street = row[1].value if self.__is_bucharest_worksheet(worksheet) else row[3].value \
                if self.__is_large_locality_worksheet(worksheet) else None
            house_number = row[2].value if self.__is_bucharest_worksheet(worksheet) else row[4].value \
                if self.__is_large_locality_worksheet(worksheet) else None
            zip_code = row[3].value if self.__is_bucharest_worksheet(worksheet) else row[5].value \
                if self.__is_large_locality_worksheet(worksheet) else row[3].value
            street_type = row[0].value if self.__is_bucharest_worksheet(worksheet) else row[2].value \
                if self.__is_large_locality_worksheet(worksheet) else None

            code = Code(county, locality, sector, street, house_number, zip_code, street_type)
            codes.append(code)

        return codes

    @staticmethod
    def __is_bucharest_worksheet(worksheet):
        return worksheet.title == "Bucuresti"

    @staticmethod
    def __is_large_locality_worksheet(worksheet):
        return "peste" in worksheet.title

    @staticmethod
    def __is_small_locality_worksheet(worksheet):
        return "sub" in worksheet.title
