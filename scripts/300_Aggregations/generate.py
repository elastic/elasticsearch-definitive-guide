#!/usr/bin/env python3

import json
import sys
import random
import datetime
import math

vendors = [
    "Yellow",
    "Green",
    "Blue",
    "Red",
    "Black"
]

all_zones = [
    "Castro District",
    "Chinatown",
    "Cole Valley",
    "Financial District",
    "Fisherman's Wharf",
    "Haight-Ashbury",
    "Hayes Valley",
    "Japantown",
    "Lower Haight",
    "Marina",
    "Mission District",
    "Nob Hill",
    "Noe Valley",
    "North Beach",
    "Pacific Heights",
    "Panhandle",
    "Potrero Hill",
    "Presidio",
    "Richmond",
    "Russian Hill",
    "Sea Cliff",
    "Sixth Street",
    "SOMA",
    "Sunset",
    "Tenderloin",
    "Union Square",
    "Upper Market"
]

zones = [
    "Chinatown",
    "Financial District",
    "Haight-Ashbury",
    "Presidio",
    "Sunset"
]

minutes_per_mile = 5

distances_in_miles = {
    "Chinatown": {
        "Chinatown": 0,
        "Financial District": 1,
        "Haight-Ashbury": 4,
        "Presidio": 4,
        "Sunset": 9
    },
    "Financial District": {
        "Chinatown": 1,
        "Financial District": 0,
        "Haight-Ashbury": 4,
        "Presidio": 4,
        "Sunset": 7
    },
    "Haight-Ashbury": {
        "Chinatown": 4,
        "Financial District": 4,
        "Haight-Ashbury": 0,
        "Presidio": 3,
        "Sunset": 4
    },
    "Presidio": {
        "Chinatown": 4,
        "Financial District": 4,
        "Haight-Ashbury": 3,
        "Presidio": 0,
        "Sunset": 5
    },
    "Sunset": {
        "Chinatown": 9,
        "Financial District": 7,
        "Haight-Ashbury": 4,
        "Presidio": 5,
        "Sunset": 0
    }
}


def payment_type():
    v = random.uniform(0, 10)
    if v < 7:
        return "Credit card"
    elif v < 9.5:
        return "Cash"
    else:
        return "No charge"


def vendor():
    return random.choice(vendors)


def passengers():
    return min(6, max(1, round(random.lognormvariate(mu=0, sigma=1))))


def distance(start, end):
    base = distances_in_miles[start][end]
    return base + 0.2 * random.randint(0, max(base, 1))


def duration(dist_miles):
    # 15 - 25 miles per hour on average
    return datetime.timedelta(hours=dist_miles / random.randint(15, 25))


def fare(trip_distance):
    # loosely based on https://www.sfmta.com/getting-around/taxi/taxi-rates
    # assume a random waiting time up to 10% of the distance
    waiting_time_factor = 0.55 * 0.1 * random.randint(0, round(trip_distance))
    units = max(0, round(trip_distance / 0.125) - 1)
    return 3.5 + units * 0.55


def tip(fare_amount):
    # up to 20% tip
    return 0.2 * random.randint(0, round(fare_amount))


def round_f(v):
    return float("{0:.2f}".format(v))


def generate_timestamp(current):
    h = current.hour
    week_day = current.isoweekday()

    hours_per_day = 24

    peak_hour = 12
    max_difference_hours = hours_per_day - peak_hour

    if week_day < 6:
        max_rides_per_hour = 1000
        min_rides_per_hour = 100
    elif week_day == 6:
        max_rides_per_hour = 800
        min_rides_per_hour = 200
    else:
        max_rides_per_hour = 600
        min_rides_per_hour = 50

    diff_from_peak_hour = peak_hour - h if h <= peak_hour else h - peak_hour
    # vary the targeted rides per hour between [min_rides_per_hour; max_rides_per_hour] depending on difference to peak hour according to
    # a sine function to smooth it a bit.
    traffic_scale_factor = math.sin(0.5 * math.pi * (max_difference_hours - diff_from_peak_hour) / max_difference_hours)
    target_rides_this_hour = min_rides_per_hour + (max_rides_per_hour - min_rides_per_hour) * traffic_scale_factor

    increment = random.expovariate(target_rides_this_hour) * 3600
    return current + datetime.timedelta(seconds=increment)


def format_ts(ts):
    return ts.strftime("%Y-%m-%d %H:%M:%S")


def main():
    if len(sys.argv) != 2:
        print("usage: %s number_of_records_to_generate" % sys.argv[0])
        exit(1)

    current = datetime.datetime(year=2017, month=4, day=1)
    num_records = int(sys.argv[1])
    for i in range(num_records):
        record = {}
        current = generate_timestamp(current)
        record["vendor"] = vendor()
        record["pickup_datetime"] = format_ts(current)
        record["passenger_count"] = passengers()

        start = random.choice(zones)
        end = random.choice(zones)
        trip_distance = distance(start, end)
        record["dropoff_datetime"] = format_ts(current + duration(trip_distance))

        record["pickup_zone"] = start
        record["dropoff_zone"] = end
        record["payment_type"] = payment_type()
        record["trip_distance"] = round_f(trip_distance)
        fare_amount = round_f(fare(trip_distance))
        tip_amount = round_f(tip(fare_amount))
        record["fare_amount"] = fare_amount
        record["tip_amount"] = tip_amount
        record["total_amount"] = round_f(fare_amount + tip_amount)

        print(json.dumps(record))


if __name__ == '__main__':
    main()
