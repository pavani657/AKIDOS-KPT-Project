import pandas as pd
import numpy as np
from datetime import timedelta
import matplotlib.pyplot as plt

from src.feature_engineering import *
from src.kpi_engine import compute_kpi
from src.readiness_engine import adjusted_prep_time, readiness_probability
from src.dispatch_logic import should_dispatch

orders = pd.read_csv("../data/orders_dataset.csv",
                     parse_dates=['order_time', 'ready_time'])

wait_static = []
wait_smart = []

for i in range(200):
    order = orders.iloc[i]
    current_time = order['order_time']

    base_prep = 20

    active = compute_active_orders(orders, current_time)
    throughput = compute_throughput(orders, current_time)
    baseline = 2

    oci = compute_order_complexity(order['items_count'],
                                   order['cooking_type'])

    capacity = 50
    rush_factor = 1.2 if order['is_peak_hour'] == 1 else 1

    kpi = compute_kpi(active, capacity,
                      baseline, throughput,
                      rush_factor, oci)

    adjusted = adjusted_prep_time(base_prep, kpi)

    # Static model
    static_arrival = current_time + timedelta(minutes=base_prep)
    static_wait = max(0,
        (order['ready_time'] - static_arrival).total_seconds()/60)
    wait_static.append(static_wait)

    # Smart model
    for t in range(5, 40):
        test_time = current_time + timedelta(minutes=t)
        prob = readiness_probability(test_time,
                                      current_time,
                                      adjusted)
        if should_dispatch(prob):
            smart_arrival = test_time
            break

    smart_wait = max(0,
        (order['ready_time'] - smart_arrival).total_seconds()/60)
    wait_smart.append(smart_wait)

print("Average Static Wait:", np.mean(wait_static))
print("Average Smart Wait:", np.mean(wait_smart))

plt.plot(wait_static, label="Static")
plt.plot(wait_smart, label="AKIDOS")
plt.legend()
plt.title("Rider Wait Time Comparison")
plt.show()
