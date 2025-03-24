#!/usr/bin/env python

import os
import numpy as np
import pandas as pd
import pickle
import sys

kmer_size = 5
# in_dir = sys.argv[1]
in_dir = "."
#out_dir = sys.argv[2]
out_dir = "../../003.pickled.5mer.features/barcode02"
if not os.path.exists(out_dir):
    os.makedirs(out_dir, exist_ok=True)

## load data
for filename in os.listdir(in_dir):
    full_path = os.path.join(in_dir, filename)
    x = pd.read_csv(full_path, sep = "\t", header=0,
                names = ["mean", "std", "length", "base"])
    x_base_enc = pd.get_dummies(x, columns=['base'], dtype=int)
    x_arr = x_base_enc.to_numpy()
    # Split into sub-arrays (e.g., split into two sub-arrays along axis 0)
    x_arr_split = np.split(x_arr, indices_or_sections = x_arr.shape[0]/kmer_size, axis = 0)
    # Reshape into a 3D array
    x_arr = np.stack(x_arr_split, axis=0)
    with open(os.path.join(out_dir, ''.join([filename, '.pkl'])), 'wb') as file:
        pickle.dump(x_arr, file)