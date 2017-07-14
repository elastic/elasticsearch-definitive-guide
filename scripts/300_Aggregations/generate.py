#!/usr/bin/env python3

import json
import sys
import random
import datetime
import math


class Vendor:
    def __init__(self, name, market_share, max_tip, p_credit_card, p_cash, min_passengers, max_passengers):
        self.name = name
        self.market_share = market_share
        self.p_credit_card = 100 * p_credit_card
        self.p_cash = 100 * p_cash
        self.min_passengers = min_passengers
        self.max_passengers = max_passengers
        self.max_tip = max_tip
        # on average 15
        self.min_miles_per_hour = random.randint(13, 17)
        # on average 25
        self.max_miles_per_hour = random.randint(21, 29)

    def payment_type(self):
        v = random.uniform(0, 100)
        if v < self.p_credit_card:
            return "Credit card"
        elif v < self.p_credit_card + self.p_cash:
            return "Cash"
        else:
            return "No charge"

    def passengers(self):
        return min(self.max_passengers, max(self.min_passengers, round(random.lognormvariate(mu=0, sigma=1))))

    def distance(self, start, end):
        base = distances_in_miles[start][end]
        return base + 0.2 * random.randint(0, max(base, 1))

    def duration(self, dist_miles):
        return datetime.timedelta(hours=dist_miles / random.randint(self.min_miles_per_hour, self.max_miles_per_hour))

    def fare(self, trip_distance):
        # loosely based on https://www.sfmta.com/getting-around/taxi/taxi-rates
        # assume a random waiting time up to 10% of the distance
        waiting_time_units = 0.1 * random.randint(0, round(trip_distance))
        trip_units = max(0, round(trip_distance / 0.125) - 1)
        return 3.5 + 0.55 * (trip_units + waiting_time_units)

    def tip(self, fare_amount):
        return self.max_tip * random.randint(0, round(fare_amount))


vendors = [
    Vendor(name="Yellow", market_share=0.17, max_tip=0.14, p_credit_card=0.7, p_cash=0.25, min_passengers=1, max_passengers=8),
    Vendor(name="Green", market_share=0.25, max_tip=0.17, p_credit_card=0.79, p_cash=0.2, min_passengers=1, max_passengers=4),
    Vendor(name="Blue", market_share=0.13, max_tip=0.13, p_credit_card=0.8, p_cash=0.15, min_passengers=1, max_passengers=6),
    Vendor(name="Red", market_share=0.2, max_tip=0.15, p_credit_card=0.7, p_cash=0.3, min_passengers=1, max_passengers=10),
    Vendor(name="Black", market_share=0.25, max_tip=0.18, p_credit_card=0.6, p_cash=0.35, min_passengers=1, max_passengers=5),
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


def choose_vendor():
    # see https://docs.python.org/3.6/library/random.html#random.choices
    # return random.choices(vendors, cum_weights=[v.market_share for v in vendors])[0]
    return weighted_choice(vendors)


def weighted_choice(choices):
    # based on https://stackoverflow.com/a/26196078/6429186
    r = random.uniform(0.0, 1.0)
    upto = 0
    for c in choices:
        w = c.market_share
        if upto + w >= r:
            return c
        upto += w
    assert False, "Shouldn't get here"


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

    current = datetime.datetime(year=2017, month=6, day=1)
    num_records = int(sys.argv[1])
    for i in range(num_records):
        record = {}
        current = generate_timestamp(current)
        vendor = choose_vendor()
        record["vendor"] = vendor.name
        record["pickup_datetime"] = format_ts(current)
        record["passenger_count"] = vendor.passengers()

        start = random.choice(zones)
        end = random.choice(zones)
        trip_distance = vendor.distance(start, end)
        record["dropoff_datetime"] = format_ts(current + vendor.duration(trip_distance))

        record["pickup_zone"] = start
        record["dropoff_zone"] = end
        record["payment_type"] = vendor.payment_type()
        record["trip_distance"] = round_f(trip_distance)
        fare_amount = round_f(vendor.fare(trip_distance))
        tip_amount = round_f(vendor.tip(fare_amount))
        record["fare_amount"] = fare_amount
        record["tip_amount"] = tip_amount
        record["total_amount"] = round_f(fare_amount + tip_amount)

        print(json.dumps(record))


if __name__ == '__main__':
    main()
