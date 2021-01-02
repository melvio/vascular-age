#!/usr/bin/env python3.8

_DAYS_IN_YEAR = 365.25


def years_to_days(years: float) -> int:
    """Return the average amount of days in a year as int"""
    return round(years * _DAYS_IN_YEAR)
