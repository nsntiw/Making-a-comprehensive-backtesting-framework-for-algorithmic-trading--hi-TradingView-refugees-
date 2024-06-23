import pandas as pd
import numpy as np

def montecarlo(trades, times):
    results = []
    for _ in range(times):
        rng_array = np.random.randint(0, len(trades['Return']), len(trades['Return']))
        results.append(trades['Return'].values[rng_array])
    return results