import csv
import sys

import xlrd


def fix_excel_dates(date_str):
    if date_str.endswith(".0"):
        return xlrd.xldate_as_datetime(float(date_str), 0).date()
    else:
        return date_str


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
            row["notice_date"] = fix_excel_dates(row["notice_date"])
            if "initiated_date" in row:
                row["initiated_date"] = fix_excel_dates(row["initiated_date"])

            writer.writerow(row)
