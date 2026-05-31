"""Fail the build if any year is silently missing from f7.db.

The published database is assembled from spreadsheets in raw/. Some annual
files (e.g. FY-2015, FY-2016) are no longer served by fmcs.gov, so they only
make it into the build if they are committed to the repo. When such a file is
missing, the affected year drops to zero rows and the gap is easy to miss --
see https://github.com/labordata/fmcs-f7/issues/16.

This guard asserts that every calendar year in a continuously-covered window
has a plausible number of notices, and exits non-zero (failing `make`) if not.
"""

import datetime
import sqlite3
import sys

DB = sys.argv[1] if len(sys.argv) > 1 else "f7.db"

# Continuous monthly/annual coverage begins in 2005 (NAICS era). Earlier years
# exist but are sparser and filed as a few historical spreadsheets, so we only
# enforce the floor from 2005 up to (but not including) the current year, which
# is always partial.
FIRST_ENFORCED_YEAR = 2005
LAST_ENFORCED_YEAR = datetime.date.today().year - 1

# Smallest yearly volume we have ever seen is ~14k; anything under this floor
# means a source file failed to load rather than a real dip in bargaining.
MIN_NOTICES_PER_YEAR = 5000


def main():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    deficient = []
    for year in range(FIRST_ENFORCED_YEAR, LAST_ENFORCED_YEAR + 1):
        (count,) = cur.execute(
            "select count(*) from f7 where notice_date like ?", (f"{year}%",)
        ).fetchone()
        if count < MIN_NOTICES_PER_YEAR:
            deficient.append((year, count))

    if deficient:
        print(
            f"COVERAGE CHECK FAILED for {DB}: "
            f"each year {FIRST_ENFORCED_YEAR}-{LAST_ENFORCED_YEAR} should have "
            f">= {MIN_NOTICES_PER_YEAR} notices.",
            file=sys.stderr,
        )
        for year, count in deficient:
            print(f"  {year}: {count} notices", file=sys.stderr)
        print(
            "A source spreadsheet for the year(s) above is probably missing "
            "from raw/ (and uncommitted). See issue #16.",
            file=sys.stderr,
        )
        sys.exit(1)

    print(
        f"coverage ok: {FIRST_ENFORCED_YEAR}-{LAST_ENFORCED_YEAR} "
        f"all >= {MIN_NOTICES_PER_YEAR} notices"
    )


if __name__ == "__main__":
    main()
