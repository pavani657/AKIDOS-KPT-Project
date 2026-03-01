import pandas as pd
import numpy as np

def compute_active_orders(df, current_time):
    active = df[(df['order_time'] <= current_time) &
                (df['ready_time'] > current_time)]
    return len(active)

def compute_throughput(df, current_time, window=15):
    window_start = current_time - pd.Timedelta(minutes=window)
    completed = df[(df['ready_time'] >= window_start) &
                   (df['ready_time'] <= current_time)]
    return len(completed) / window

def compute_order_complexity(items_count, cooking_type):
    cooking_weights = {
        "fried": 1.2,
        "baked": 1.5,
        "grilled": 1.3,
        "simple": 0.8
    }
    return 0.4 * items_count + 0.6 * cooking_weights.get(cooking_type, 1)

def compute_merchant_reliability(wait_times):
    if len(wait_times) == 0:
        return 1
    variance = np.var(wait_times)
    return 1 / (1 + variance)
