"""RowGraphNet: row-level relational GNN backbone.

model.py  - the network (cell encoding -> row pooling -> typed message
            passing (+optional ULTRA-style relation graph) -> candidate-value
            classification readout; fixed numeric bins retain their training loss)
train.py  - from-scratch mixed-task leave-db-out training, classification evaluation
"""
from rowgraph.model import RowGraphNet  # noqa: F401
