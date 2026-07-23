"""Generate per-task regression codebooks: 1-D weighted k-means in z-space.

Run with a python that has relbench (e.g. ~/miniconda3/bin/python).
Codebook = empirical Lloyd-Max quantizer of the task's TRAIN-split targets,
computed in the same z-space the sampler feeds the model (train mean/std,
ddof=1, matching rustler/src/pre.rs). No test labels are touched; no model
parameters depend on the eval database — zero-shot is preserved (same data
source as the pipeline's standardization statistics).

Output: experiments/exp2_rowgraph/codebooks_k64.json
"""
import json
import sys
from pathlib import Path

import numpy as np
from relbench.tasks import get_task

K = 64
REG_TASKS = [
    ('rel-amazon', 'item-ltv'),
    ('rel-amazon', 'user-ltv'),
    ('rel-avito', 'ad-ctr'),
    ('rel-event', 'user-attendance'),
    ('rel-f1', 'driver-position'),
    ('rel-hm', 'item-sales'),
    ('rel-stack', 'post-votes'),
    ('rel-trial', 'site-success'),
    ('rel-trial', 'study-adverse'),
]


def kmeans1d_w(u, w, k, iters=500):
    """Weighted 1-D Lloyd. Mass-aware init: heavy point masses get their own
    center from the start; the rest spread over the support by rank."""
    if len(u) <= k:
        return u.copy()
    top = u[np.argsort(-w)[: k // 4]]
    fill = u[np.linspace(0, len(u) - 1, k - len(top)).astype(int)]
    c = np.unique(np.concatenate([top, fill]))
    while len(c) < k:  # dedup shrank the init: split the widest gap
        gaps = np.diff(c)
        i = int(np.argmax(gaps))
        c = np.sort(np.append(c, (c[i] + c[i + 1]) / 2))
    for _ in range(iters):
        mid = (c[:-1] + c[1:]) / 2
        idx = np.searchsorted(mid, u)
        s = np.bincount(idx, weights=w * u, minlength=len(c))
        n = np.bincount(idx, weights=w, minlength=len(c))
        ne = n > 0
        newc = np.unique(s[ne] / n[ne])
        if len(newc) == len(c) and np.allclose(newc, c, atol=1e-12):
            break
        c = newc
    return c


out = {}
for db, tb in REG_TASKS:
    t = get_task(db, tb, download=True)
    col = t.target_col
    v = t.get_table('train', mask_input_cols=False).df[col].values.astype(float)
    v = v[np.isfinite(v)]
    mean, std = float(v.mean()), float(v.std(ddof=1))
    if std == 0:
        std = 1.0
    z = (v - mean) / std
    u, w = np.unique(z, return_counts=True)
    cb = kmeans1d_w(u, w.astype(float), K)
    # quantization SSE in z-space (clamping only; two-hot interpolates in-range)
    zc = np.clip(z, cb.min(), cb.max())
    sse = float(((z - zc) ** 2).sum())
    out[f'{db}/{tb}'] = dict(
        target=col, mean=mean, std=std, K_eff=len(cb),
        centers=[float(x) for x in cb],
    )
    print(f'{db}/{tb:20s} target={col:24s} n={len(v):>9,} K_eff={len(cb):>3} '
          f'range=[{cb.min():.3f},{cb.max():.3f}] train-clamp SSE={sse:.4f}',
          flush=True)

path = Path(__file__).resolve().parent / 'codebooks_k64.json'
path.write_text(json.dumps(out, indent=1))
print(f'\nwrote {path}')
