#!/bin/bash -x

mkdir -p build/lib/guacamol_baselines/data

wget https://ndownloader.figshare.com/files/13612745 -O build/lib/guacamol_baselines/data/guacamol_v1_all.smiles

wget https://ndownloader.figshare.com/files/13612760 -O build/lib/guacamol_baselines/data/guacamol_v1_train.smiles

wget https://ndownloader.figshare.com/files/13612766 -O build/lib/guacamol_baselines/data/guacamol_v1_valid.smiles

wget https://ndownloader.figshare.com/files/13612757 -O build/lib/guacamol_baselines/data/guacamol_v1_test.smiles

