import time
import pycountry

ONE_MINUTE = 60
ONE_HOUR = 60 * ONE_MINUTE
ONE_DAY = 24 * ONE_HOUR

countries = [country.alpha_2 for country in pycountry.countries]
languages = [lang.alpha_2 for lang in pycountry.languages if hasattr(lang, 'alpha_2')]


def now():
    return int(time.time() * 1000)


def validate_country(code):
    return code in countries


def validate_language(code):
    return code in languages
