def update_threshold(avg_wait_time, current_threshold):
    if avg_wait_time > 5:
        return min(current_threshold + 0.02, 0.95)
    else:
        return max(current_threshold - 0.02, 0.75)
