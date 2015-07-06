#!/usr/bin/python

import logging
import argparse
import sys
import csv
from collections import defaultdict
from itertools import groupby

parser = argparse.ArgumentParser('aggr')

parser.add_argument('-p', '--pattern', required=True)
parser.add_argument('-i', '--infile')
parser.add_argument('-o', '--outfile')
parser.add_argument('-d', '--field-delimiter')
parser.add_argument('-v', '--verbose', action='store_true')

parser.set_defaults(field_delimiter=',')
parser.set_defaults(verbose=False)

args = parser.parse_args()

PATTERN_OPTIONS = ('key', 'sum', 'max', 'min', 'len', 'any')

FUNCTION_MAP = {
        'sum' : sum,
        'max' : max,
        'min' : min,
        'len' : len,
        'any' : any
        }


def parse_pattern():
    pattern = args.pattern.split(args.field_delimiter)
    for p in pattern:
        assert p in PATTERN_OPTIONS
    return pattern


def get_keyfunc():
    def keyfunc(record):
        return tuple(f 
                     for f, option in zip(record, parse_pattern())
                     if option == 'key')
    return keyfunc


def infer_type(field):
    try:
        return int(field)
    except ValueError as ex:
        pass
    try:
        return float(field)
    except ValueError as ex:
        pass
    return field


def parse_record(raw_record):
    return [infer_type(f.strip()) for f in raw_record.split(args.field_delimiter)]


def get_records():
    if args.infile:
        with open(args.infile, 'r') as infile:
            return infile.readlines()
    else:
        return sys.stdin


def aggregate_group(records):
    records = list(records)
    logging.debug(records)
    for n, _ in enumerate(records[0]):
        if parse_pattern()[n] == 'key':
            continue
        else:
            func = FUNCTION_MAP[parse_pattern()[n]]
            column = [record[n] for record in records]
            logging.debug(column)
            yield func(column)


def output(results):
    if args.outfile:
        with open(args.outfile, 'w') as of:
            writer = csv.writer(of, delimiter=args.field_delimiter)
            for row in results:
                writer.writerow(row)
    else:
        writer = csv.writer(sys.stdout, delimiter=args.field_delimiter)
        for row in results:
            writer.writerow(row)


def aggr():
    keyfunc = get_keyfunc()
    records = map(parse_record, get_records())
    records = sorted(records, key=keyfunc)
    results = (k + tuple(aggregate_group(g))
               for k, g in groupby(records, keyfunc))
    output(results)


if __name__ == '__main__':
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    aggr()
