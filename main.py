# -*- coding: utf-8 -*-
import pandas as pd
from jours_feries_france.compute import JoursFeries
from datetime import date


def bank_holiday_name(data, date):
    return [k for k, v in data[date.year].items() if v == date][0]


def to_csv(df, filename):
    df.to_csv(filename, index=False, encoding='utf-8')

START, END = date(1950, 1, 1), date(2050, 12, 31)

modes = [
    ({'include_alsace': False}, ''),
    ({'include_alsace': True}, '_alsace_moselle')
]

for mode in modes:
    args, suffix = mode
    bank_holidays = {}

    for year in range(START.year, END.year+1):
        bank_holidays[year] = JoursFeries.for_year(year, **args)

    data = []
    dates = map(lambda d: d.to_pydatetime().date(), pd.date_range(START, END))
    for the_date in dates:
        est_jour_ferie = the_date in bank_holidays[the_date.year].values()
        nom_jour_ferie = None
        if est_jour_ferie:
            nom_jour_ferie = bank_holiday_name(bank_holidays, the_date)

        data.append({
            'date': the_date.strftime('%Y-%m-%d'),
            'est_jour_ferie': est_jour_ferie,
            'nom_jour_ferie': nom_jour_ferie
        })

    df = pd.DataFrame(data)
    to_csv(df, 'jours_feries' + suffix + '.csv')
    to_csv(df[df.est_jour_ferie], 'jours_feries_seuls' + suffix + '.csv')
