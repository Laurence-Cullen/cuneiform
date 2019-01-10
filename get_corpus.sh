#!/usr/bin/env bash
wget https://cdli.ucla.edu/bulk_data/cdli_catalogue_1of2.csv
wget https://cdli.ucla.edu/bulk_data/cdli_catalogue_2of2.csv
wget https://cdli.ucla.edu/bulk_data/cdliatf_unblocked.atf
cat cdli_catalogue_1of2.csv cdli_catalogue_2of2.csv > cdli_catalogue.csv

if [[ ! -d "data" ]]; then
  # enter here if data doesn't exist.
  mkdir data
fi

mv cdli_catalogue.csv data/
mv cdliatf_unblocked.atf data/
rm cdli_catalogue*
