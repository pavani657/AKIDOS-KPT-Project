def compute_kpi(active_orders, capacity,
                baseline_throughput, current_throughput,
                rush_factor, oci):

    if current_throughput == 0:
        current_throughput = 0.1

    load_ratio = active_orders / capacity
    throughput_ratio = baseline_throughput / current_throughput

    kpi = load_ratio * throughput_ratio * rush_factor * oci

    return min(kpi, 1)
