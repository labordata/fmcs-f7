.PHONY : all
all : 
	$(MAKE) update_raw
	$(MAKE) f7.csv f7.db

f7.db : f7.csv link.csv
	csvs-to-sqlite $^ $@

no_exact.csv : f7.csv
	csvcut -c employer,union_name,union_city,union_state,affected_location_city,affected_location_state $< | csvsort | uniq > $@

link.csv : no_exact.csv
	python scripts/link_units.py $< $@ -v -v

f7.csv : $(patsubst %.xlsx,%.csv,$(wildcard raw/*.xlsx))
	python scripts/to_csv.py $^ | \
            csvsort | \
            uniq | \
            csvcut -x -l | \
            sed '1s/line_number/id/' > $@

%.csv : %.xlsx
	in2csv $< | sed '/^Notice Date/,$$!d' > $@

.PHONY : update_raw
update_raw :
	curl -k https://www.fmcs.gov/resources/documents-and-data/#tab-d3d7f5344cef9bab4d3 | grep Notices.xlsx | sed -n 's/.*href="\([^"]*\).*/\1/p' | wget --no-check-certificate -nd -i - -P raw -nc
