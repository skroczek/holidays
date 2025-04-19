from datetime import date, timedelta
import argparse
from gettext import gettext as tr
from holidays.constants import CATHOLIC, PUBLIC, UNOFFICIAL
from icalendar import Calendar, Event
import uuid
from datetime import datetime
from holidays.countries.germany import Germany


class GermanyWithAugsburg(Germany):
    supported_categories = (CATHOLIC, PUBLIC, UNOFFICIAL)

    def _populate_subdiv_by_unofficial_holidays(self):
            self._add_holiday_feb_14(tr("Valentinstag"))
            self._add_holiday_oct_31(tr("Halloween"))
            self._add_holiday_dec_6(tr("Nikolaus"))

            # Muttertag: Zweiter Sonntag im Mai
            self._add_holiday_2nd_sun_of_may(tr("Muttertag"))

            # Bewegliche Feiertage auf Basis von Ostern
            self._add_holy_thursday(tr("Gründonnerstag"))
            self._add_palm_sunday(tr("Palmsonntag"))
            self._add_ash_monday(tr("Rosenmontag"))
            self._add_carnival_tuesday(tr("Faschingsdienstag"))
            self._add_ash_wednesday(tr("Aschermittwoch"))


def generate_calendar(start_year: int, end_year: int, region: str, output_file: str, categories: list) -> None:
    state = region

    calendar = Calendar()
    calendar.add('prodid', 'icalendar-python')
    calendar.add('version', '2.0')
    calendar.add('calscale', 'GREGORIAN')
    calendar.add('X-WR-CALNAME', 'Deutsche Feiertage')
    calendar.add('X-APPLE-LANGUAGE', 'de')
    calendar.add('X-APPLE-REGION', 'DE')

    subdiv, custom_subdiv = (state.split("_", 1) + [None])[:2]
    for year in range(start_year, end_year + 1):
        state_holidays = GermanyWithAugsburg(
            years=year,
            subdiv=subdiv,
            categories=categories
        )
        for day, name in sorted(state_holidays.items()):
            event = Event()
            event.add('dtstamp', datetime(1976, 4, 1).date())
            event.add('uid', f"{uuid.uuid4()}")
            event.add('dtstart', day)
            event.add('class', 'PUBLIC')
            event.add('summary', name)
            event['SUMMARY'].params['LANGUAGE'] = 'de'
            event.add('transp', 'TRANSPARENT')
            event.add('categories', 'Feiertag')
            event.add('X-APPLE-UNIVERSAL-ID', str(uuid.uuid4()))
            calendar.add_component(event)

    with open(output_file, "wb") as f:
        f.write(calendar.to_ical())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate German public holidays as iCal file.")
    parser.add_argument("--from-year", type=int, help="Start year")
    parser.add_argument("--to-year", type=int, help="End year")
    parser.add_argument("--years-range", nargs=2, type=int, metavar=('BEFORE', 'AFTER'),
                        help="Relative range in years from current year, e.g., -3 5")
    parser.add_argument("--region", type=str, default="DE", help="Region or subdivision (e.g. DE, BY)")
    parser.add_argument("--output", type=str, default="feiertage.ics", help="Output file name")
    parser.add_argument("--with-unofficial", action="store_true", help="With unofficial holidays")
    parser.add_argument("--with-public", action="store_true", help="With public holidays")
    parser.add_argument("--with-catholic", action="store_true", help="With catholic holidays")
    args = parser.parse_args()

    today_year = date.today().year

    if args.years_range:
        before, after = args.years_range
        start_year = today_year + before
        end_year = today_year + after
    else:
        start_year = args.from_year or today_year
        end_year = args.to_year or today_year

    categories = []
    if args.with_unofficial:
        categories.append(UNOFFICIAL)
    if args.with_public:
        categories.append(PUBLIC)
    if args.with_catholic:
        categories.append(CATHOLIC)

    generate_calendar(start_year, end_year, args.region, args.output, categories)
