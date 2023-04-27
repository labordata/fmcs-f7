.PHONY : all
all : 
	$(MAKE) update_raw
	$(MAKE) f7.csv f7.db

f7.db : f7.csv f7_opdr.csv
	csvs-to-sqlite $^ $@

f7_opdr.csv : f7.csv link_units.csv
	csvsql -I --query 'select id as f7_id, canon_id as f_num from f7 inner join link_units on trim(lower(f7.union_name)) = link_units.union_name and trim(lower(f7.union_city)) = link_units.union_city and trim(lower(f7.union_state)) = link_units.union_state where canon_id is not null' $^ > $@

no_exact_unions.csv : f7.csv
	csvcut -c union_name,union_city,union_state $< | \
            python scripts/normalize.py | \
            csvsort | \
            uniq > $@

link_units.csv : no_exact_unions.csv
	unionlookup $< $@ -v -v

f7.csv : $(patsubst %.xlsx,%.csv,$(wildcard raw/*Notices.xlsx))
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
