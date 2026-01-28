from datetime import date, timedelta
from typing import Iterable, Tuple, Dict

def _week_start(d: date) -> date:
    return d - timedelta(days=d.weekday())

def compute_streaks_for_x_per_week(
        log_dates: Iterable[date],
        today: date,
        target_per_week: int,
) -> Tuple[int, int]:
    if target_per_week <= 0:
        return 0, 0
    
    counts: Dict[date, int] = {}
    for d in log_dates:
        ws = _week_start(d)
        counts[ws] = counts.get(ws, 0) + 1

    if not counts:
        return 0, 0
    
    successful = { ws for ws, c in counts.items() if c >= target_per_week }

    best = 0
    for ws in sorted(successful):
        prev_ws = ws - timedelta(days=7)
        if prev_ws in successful:
            continue
        run = 1
        nxt = ws + timedelta(days=7)
        while nxt in successful:
            run += 1
            nxt += timedelta(days=7)
        best = max(best, run)
    
    curr_ws = _week_start(today)
    start_ws = curr_ws if curr_ws in successful else (curr_ws - timedelta(days=7))

    current = 0
    ws = start_ws
    while ws in successful:
        current += 1
        ws -= timedelta(days=7)
    return current, best 

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