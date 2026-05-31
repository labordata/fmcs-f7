SHELL=/bin/bash -o pipefail

.PHONY : all
all :
	$(MAKE) update_raw
	$(MAKE) f7.csv f7.db
	$(MAKE) check

# Guard against a year silently dropping out of the build (see issue #16).
.PHONY : check
check : f7.db
	python scripts/check_coverage.py f7.db

f7.db : f7.csv
	csvs-to-sqlite $^ $@

f7.csv : $(patsubst %.xlsx,%.csv,$(wildcard raw/*Notices*.xlsx)) $(patsubst %.xls,%.csv,$(wildcard raw/*Notices*.xls))
	python scripts/to_csv.py $^ | \
            csvsort | \
            uniq > $@

%.csv : %.xlsx
	(in2csv $< || in2csv $< -K 5) | sed '/^Notice Date/,$$!d' > $@

%.csv : %.xls
	in2csv $< | sed '/^Notice Date/,$$!d' > $@


.PHONY : update_raw
update_raw :
	curl -k https://www.fmcs.gov/resources/documents-and-data/#tab-d3d7f5344cef9bab4d3 | grep Notices.xlsx | sed -n 's/.*href="\([^"]*\).*/\1/p' | wget --no-check-certificate -nd -i - -P raw -nc
