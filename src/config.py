from datetime import datetime

interest_tickers = {
    # Crude Oil
    "WTI": "WTIPUUS",
    "Brent": "BREPUUS",

    # Liquid fuels - Refiner prices for resale
    "Gasoline": "MGWHUUS",
    "Diesel": "DSWHUUS",
    "FuelOil": "D2WHUUS",

    # Liquid fuels - Retail prices including Taxes
    "GasolineRegularGrade": "MGRARUS",
    "GasolineAllGrades": "MGEIAUS",
    "OnHighwayDiesel": "DSRTUUS",
    "HeatingOil": "D2RCAUS",  # not found in legacy format.  D2RCUUS is equivalent?

    # Natural Gas
    "HenryHubSpot": "NGHHMCF", # not found in legacy format
    "RetailNaturalGas - Residential": "NGRCUUS",

    # Electricity
    "RetailElectricityResidential": "ESRCUUS",  # legacy format - in Electricity tab
}

RESOURCE_DIR = 'resources'
CSV_DIR = 'csv'


NEW_FORMAT_START_DATE = datetime.strptime("200710", "%Y%m")
START_TO_USE_XSLX = datetime.strptime("201307", "%Y%m")
URL_BASE = "https://www.eia.gov/outlooks/steo/archives/{}"
END_YEAR = 2021
