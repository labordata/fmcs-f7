import csv
import re
import sys

import xlrd

TIME_ONLY = re.compile(r"^\d{1,2}:\d{2}(:\d{2})?$")
EXCEL_EPOCH_SENTINELS = {"1899-12-29", "1899-12-30", "1899-12-31"}


def fix_excel_dates(date_str):
    if not date_str:
        return ""
    if TIME_ONLY.match(date_str):
        return ""
    if date_str in EXCEL_EPOCH_SENTINELS:
        return ""
    if date_str.endswith(".0"):
        try:
            converted = xlrd.xldate_as_datetime(float(date_str), 0).date()
        except (ValueError, xlrd.xldate.XLDateError):
            return ""
        iso = converted.isoformat()
        if iso in EXCEL_EPOCH_SENTINELS:
            return ""
        return iso
    return date_str


def strip_trailing_zero(value):
    if value.endswith(".0"):
        return value[:-2]
    return value


def fix_zip(value):
    value = strip_trailing_zero(value.strip("-"))
    if value.isdigit():
        if len(value) == 4:
            value = "0" + value
        elif len(value) == 8:
            value = "0" + value
        if len(value) == 9:
            return value[:5] + "-" + value[5:]
    return value


def fix_phone(value):
    value = strip_trailing_zero(value)
    if value.isdigit() and len(value) == 10:
        return "(%s) %s-%s" % (value[:3], value[3:6], value[6:])
    return value


ZIP_FIELDS = (
    "employer_zip",
    "union_zip",
    "affected_location_zip",
    "location_negotiation_zip",
)
PHONE_FIELDS = ("employer_representative_phone", "union_representative_phone")
INT_FIELDS = ("naics", "bargaining_unit_size", "establishment_size")


HEADER = (
    "notice_date",
    "initiated_date",
    "employer",
    "employer_street",
    "employer_city",
    "employer_state",
    "employer_zip",
    "employer_representative",
    "employer_representative_phone",
    "employer_representative_title",
    "employer_representative_email",
    "union_name",
    "union_street",
    "union_city",
    "union_state",
    "union_zip",
    "union_representative",
    "union_representative_phone",
    "union_representative_title",
    "union_representative_email",
    "affected_location_city",
    "affected_location_state",
    "affected_location_zip",
    "expiration_date",
    "naics",
    "industry",
    "bargaining_unit_size",
    "establishment_size",
    "notice_submitted_by",
    "category",
    "healthcare_related",
    "location_negotiation_city",
    "location_negotiation_state",
    "location_negotiation_zip",
)

HEADER_LOOKUP = {
    "e-street": "employer_street",
    "e-city": "employer_city",
    "e-state": "employer_state",
    "e-zip": "employer_zip",
    "employer_rep": "employer_representative",
    "e-representative": "employer_representative",
    "e-rep_phone": "employer_representative_phone",
    "employer_rep_phone": "employer_representative_phone",
    "e-rep_title": "employer_representative_title",
    "employer_rep_title": "employer_representative_title",
    "employer_rep_email": "employer_representative_email",
    "union_name_&_local_number": "union_name",
    "u-street": "union_street",
    "u-city": "union_city",
    "u-state": "union_state",
    "u-zip": "union_zip",
    "u-representative": "union_representative",
    "union_rep": "union_representative",
    "u-rep_title": "union_representative_title",
    "union_rep_title": "union_representative_title",
    "u-rep_phone": "union_representative_phone",
    "union_rep_phone": "union_representative_phone",
    "union_rep_email": "union_representative_email",
    "a-city": "affected_location_city",
    "a-state": "affected_location_state",
    "a-zip": "affected_location_zip",
    "notice_sumbitted_by": "notice_submitted_by",
}

header_set = set(HEADER)
header_set.update({"", "e-street_2", "u-street_2"})
writer = csv.DictWriter(sys.stdout, fieldnames=HEADER, extrasaction="ignore")
writer.writeheader()


for filename in sys.argv[1:]:
    with open(filename) as f:
        reader = csv.DictReader(f)
        slugged_fields = (
            field.lower().replace(" ", "_").replace("\n", "_")
            for field in reader.fieldnames
        )
        try:
            normalized_fields = [
                field if field in header_set else HEADER_LOOKUP[field]
                for field in slugged_fields
            ]
        except KeyError:
            print(filename, file=sys.stderr)
            raise
        assert set(normalized_fields) - header_set == set(), print(
            set(normalized_fields) - header_set
        )
        reader.fieldnames = normalized_fields
        for row in reader:
            if "e-street_2" in row:
                row["employer_street"] += "\n" + row.pop("e-street_2")
            if "u-street_2" in row:
                row["union_street"] += "\n" + row.pop("u-street_2")
            for col in list(row):
                if row[col]:
                    row[col] = row[col].strip().strip("_")
            row["notice_date"] = fix_excel_dates(row["notice_date"])
            if "initiated_date" in row:
                row["initiated_date"] = fix_excel_dates(row["initiated_date"])
            if "expiration_date" in row:
                row["expiration_date"] = fix_excel_dates(row["expiration_date"])
            for col in ZIP_FIELDS:
                if col in row:
                    row[col] = fix_zip(row[col])
            for col in PHONE_FIELDS:
                if col in row:
                    row[col] = fix_phone(row[col])
            for col in INT_FIELDS:
                if col in row:
                    row[col] = strip_trailing_zero(row[col])

            writer.writerow(row)
