"""RowGraphNet: row-level relational GNN backbone.

model.py  - the network (cell encoding -> row pooling -> typed message
            passing (+optional ULTRA-style relation graph) -> candidate-value
            readout; supports per-task adaptive regression codebooks)
train.py  - from-scratch leave-db-out training/eval entry
gen_codebooks.py / codebooks_k64.json - per-task regression codebooks
            (1-D k-means of TRAIN targets in z-space, K<=64)
"""
from rowgraph.model import RowGraphNet  # noqa: F401
