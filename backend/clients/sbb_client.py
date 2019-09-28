class SBBClient:

    def get_cheapest_by_location(self, location_from, location_to, from_date, to_date):
        pass


class SBBParam:
    def __init__(self, location_from, location_to, from_date, to_date):
        self.location_from = location_from
        self.location_to = location_to
        self.from_date = from_date
        self.to_date = to_date
