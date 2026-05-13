SHELL=/bin/bash -o pipefail

.PHONY : all
all : 
	$(MAKE) update_raw
	$(MAKE) f7.csv f7.db

f7.db : f7.csv
	csvs-to-sqlite $^ $@

no_exact_unions.csv : f7.csv
	csvcut -c union_name,union_city,union_state $< | \
            python scripts/normalize.py | \
            csvsort | \
            uniq > $@

link_units.csv : no_exact_unions.csv
	unionlookup $< $@ -v -v

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
