#!/usr/bin/env bash

# TODO fix up and generalise, maybe wrap in Python?

ENCODING_MODEL=sp_encodings/omni.model
CORPUS=omni.txt

spm_encode --model=${ENCODING_MODEL} --output_format=piece monolingual_corpuses/${CORPUS} > tokenised_corpuses/${CORPUS}