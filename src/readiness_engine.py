from scipy.stats import norm

def adjusted_prep_time(base_prep, kpi):
    return base_prep * (1 + kpi)

def readiness_probability(current_time, order_time, adjusted_prep):
    elapsed = (current_time - order_time).total_seconds() / 60
    mean = adjusted_prep
    std = 3
    return norm.cdf(elapsed, mean, std)
