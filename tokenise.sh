#!/usr/bin/env bash

# TODO fix up and generalise, maybe wrap in Python?
spm_encode --model=sp_encodings/omni.model --output_format=piece monolingual_corpuses/sumerian.txt > tokenised_corpuses/sumerian.txt