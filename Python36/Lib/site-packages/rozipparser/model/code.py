class Code:
    def __init__(self, county=None, locality=None, sector=None, street=None, house_number=None, zip_code=None,
                 street_type=None):
        self.county = county
        self.locality = locality
        self.sector = sector
        self.street = street
        self.house_number = house_number
        self.zip = zip_code
        self.street_type = street_type

    def __str__(self):
        return "{},{},{},{},{},{},{}".format(self.county, self.locality, self.sector, self.street,
                                             self.house_number, self.zip, self.street_type)

    def to_list(self):
        return [self.county,
                self.locality,
                self.sector,
                self.street,
                self.house_number,
                self.zip,
                self.street_type]
