.PHONY : all
all : 
	$(MAKE) update_raw
	$(MAKE) f7.csv f7.db

f7.db : f7.csv
	sqlite3 $@ -csv '.import $< f7'

f7.csv : $(patsubst %.xlsx,%.csv,$(wildcard raw/*.xlsx))
	python scripts/to_csv.py $^ | csvsort | uniq | csvcut -x  > $@

%.csv : %.xlsx
	in2csv $< | sed '/^Notice Date/,$$!d' > $@

.PHONY : update_raw
update_raw :
	curl https://www.fmcs.gov/resources/documents-and-data/#tab-d3d7f5344cef9bab4d3 | grep Notices.xlsx | sed -n 's/.*href="\([^"]*\).*/\1/p' | wget -nd -i - -P raw -nc
