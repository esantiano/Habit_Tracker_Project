from datetime import date, timedelta
from typing import Iterable, Tuple

def compute_streaks_for_daily(log_dates: Iterable[date], today: date) -> Tuple[int,int]:
    
    unique_dates = sorted(set(log_dates))
    if not unique_dates:
        return 0,0
    
    best_streak = 1
    current_run = 1

    for i in range(1, len(unique_dates)):
        if unique_dates[i] == unique_dates[i-1] + timedelta(days=1):
            current_run += 1
        else:
            best_streak = max(best_streak, current_run)
            current_run = 1
        
    best_streak = max(best_streak, current_run)

    current_streak = 0
    day = today
    date_set = set(unique_dates)

    while day in date_set:
        current_streak += 1
        day = day - timedelta(days=1)
    
    return current_streak, best_streak