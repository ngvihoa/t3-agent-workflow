#!/usr/bin/env python3
"""Timezone-aware maintenance planning; never registers a real schedule."""
import argparse
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path

from workflow import load_config, time_value, tz


def aware(value):
    if value.tzinfo is None:
        raise ValueError("Timestamp must include an explicit timezone")
    return value.astimezone(timezone.utc)


def in_window(policy, now):
    local = aware(now).astimezone(tz(policy["timezone"]))
    minute = local.hour * 60 + local.minute
    return policy["outside_hours"] or (local.weekday() in policy["weekdays"] and time_value(policy["start"]) <= minute < time_value(policy["end"]))


def next_run(policy, now):
    now = aware(now)
    if not policy["enabled"]:
        return None
    if policy["outside_hours"]:
        return (now + timedelta(minutes=policy["interval_minutes"])).isoformat()
    candidate = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
    # Iterate UTC minutes so DST gaps/folds cannot produce imaginary local times.
    for _ in range(8 * 24 * 60):
        local = candidate.astimezone(tz(policy["timezone"]))
        minute = local.hour * 60 + local.minute
        if in_window(policy, candidate) and (minute - time_value(policy["start"])) % policy["interval_minutes"] == 0:
            return candidate.isoformat()
        candidate += timedelta(minutes=1)
    raise ValueError("No reconciliation slot within eight days; inspect schedule policy")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo", type=Path, default=Path.cwd())
    p.add_argument("--now", help="ISO timestamp with offset; defaults to current UTC")
    a = p.parse_args()
    now = datetime.fromisoformat(a.now) if a.now else datetime.now(timezone.utc)
    policy = load_config(a.repo)["maintenance"]
    print(json.dumps({"enabled": policy["enabled"], "allowed_now": policy["enabled"] and in_window(policy, now), "next_run_at": next_run(policy, now), "note": "Planning only; use supported T3 tools to register and record the actual returned handle/next run."}, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError) as exc:
        raise SystemExit(str(exc))

