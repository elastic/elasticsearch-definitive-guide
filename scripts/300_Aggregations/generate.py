#!/usr/bin/env python3

import json
import sys
import random

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


def main():
    if len(sys.argv) != 2:
        print("usage: %s number_of_records_to_generate" % sys.argv[0])
        exit(1)

    num_records = int(sys.argv[1])
    for i in range(num_records):
        record = {}
        record["vendor"] = vendor()
        # TODO: Find a simple but somewhat realistic model for daily / weekly patterns
        # record["pickup_datetime"] = pickup_datetime
        # record["dropoff_datetime"] = dropoff_datetime
        record["passenger_count"] = passengers()

        start = random.choice(zones)
        end = random.choice(zones)
        trip_distance = distance(start, end)

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
