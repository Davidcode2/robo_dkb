from datetime import datetime
import calendar

class CalendarService:
    startDate = str
    date_range = {}

    def __init__(self, month=None, year=None):
        self.startDate = self.getStartDate(month, year);

    def getYearRange(self, year):
        startDate = self.getStartDate(month=1, year=year)
        endDate = self.getEndOfYear(startDate)
        return {
            "date_from": startDate.strftime("%d.%m.%Y"),
            "date_to": endDate.strftime("%d.%m.%Y"),
        }

    def getEndOfYear(self, startDate):
        return startDate.replace(year=startDate.year, month=12, day=31)

    def getDateRange(self, month=None, year=None):
        startDate = self.getStartDate(month, year)
        endDate = self.getEndDate(startDate)
        self.date_range = {
            "date_from": startDate.strftime("%d.%m.%Y"),
            "date_to": endDate.strftime("%d.%m.%Y"),
        }
        return self.date_range

    def printDateRange(self):
        print(
            "Date range: "
            + str(self.date_range.get("date_from"))
            + " - "
            + str(self.date_range.get("date_to"))
        )

    def getStartDate(self, month=None, year=None):
        today = datetime.today()
        if month is None:
            return today.replace(day=1).date()
        if year is None:
            year = today.year
        if not 1 <= month <= 12:
            raise ValueError("Month must be an integer between 1 and 12.")
        # Return the first day of the specified month
        return today.replace(year=year, month=month, day=1).date()

    def getEndDate(self, startDate):
        _, lastDayOfMonth = calendar.monthrange(startDate.year, startDate.month)
        return startDate.replace(day=lastDayOfMonth)
