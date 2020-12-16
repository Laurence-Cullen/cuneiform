#!/usr/bin/env bash
wget https://cdli.ucla.edu/bulk_data/cdli_catalogue_1of2.csv
wget https://cdli.ucla.edu/bulk_data/cdli_catalogue_2of2.csv
wget https://cdli.ucla.edu/bulk_data/cdliatf_unblocked.atf
cat cdli_catalogue_1of2.csv cdli_catalogue_2of2.csv > cdli_catalogue.csv

DATA_DIRECTORY=../CDLI_data/

mv cdli_catalogue.csv ${DATA_DIRECTORY}
mv cdliatf_unblocked.atf ${DATA_DIRECTORY}
rm cdli*
