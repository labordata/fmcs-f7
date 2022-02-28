#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This code demonstrates how to use dedupe with a comma separated values
(CSV) file. All operations are performed in memory, so will run very
quickly on datasets up to ~10,000 rows.

We start with a CSV file containing our messy data. In this example,
it is listings of early childhood education centers in Chicago
compiled from several different sources.

The output will be a CSV with our clustered results.

For larger datasets, see our [mysql_example](mysql_example.html)
"""
import csv


def preProcess(column):
    """
    Do a little bit of data cleaning with the help of Unidecode and Regex.
    Things like casing, extra spaces, quotes and new lines can be ignored.
    """
    column = column.lower()
    # If data is missing, indicate that by setting the value to `None`
    if not column:
        column = None
    return column


def readData(input_file):
    """
    Read in our data from a CSV file and create a dictionary of records,
    where the key is a unique record ID and each value is dict
    """

    data_d = {}
    with open(input_file) as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            clean_row = [(k, preProcess(v)) for (k, v) in row.items()]
            data_d[i] = dict(clean_row)

    return data_d


if __name__ == '__main__':
    import argparse
    import logging
    import sys
    import os
    
    import dedupe

    # ## Logging

    # Dedupe uses Python logging to show or suppress verbose output. This
    # code block lets you change the level of loggin on the command
    # line. You don't need it if you don't want that. To enable verbose
    # logging, run `python examples/csv_example/csv_example.py -v`
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', nargs='?', type=str,
                        default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=str,
                        default=sys.stdout)
    parser.add_argument('-v', '--verbose', dest='verbose', action='count', default=0,
                        help='Increase verbosity (specify multiple times for more)'
                        )
    args = parser.parse_args()
    log_level = logging.WARNING
    if args.verbose:
        if args.verbose == 1:
            log_level = logging.INFO
        elif args.verbose >= 2:
            log_level = logging.DEBUG
    logging.basicConfig()
    logging.getLogger().setLevel(log_level)

    # ## Setup

    input_file = args.infile
    output_file = args.outfile
    settings_file = 'link_settings.pickle'
    training_file = 'link_settings.json'

    print('importing data ...')
    data_d = readData(input_file)

    # If a settings file already exists, we'll just load that and skip training
    if os.path.exists(settings_file):
        print('reading from', settings_file)
        with open(settings_file, 'rb') as f:
            deduper = dedupe.StaticDedupe(f)
    else:
        # ## Training

        # Define the fields dedupe will pay attention to
        fields = [
            {'field': 'employer', 'type': 'String', 'has missing': True},
            {'field': 'union_name', 'type': 'String', 'has missing': True},
            {'field': 'union_city', 'type': 'String', 'has missing': True},
            {'field': 'union_state', 'type': 'String', 'has missing': True},                {'field': 'affected_location_city', 'type': 'String', 'has missing': True},        
            {'field': 'affected_location_state', 'type': 'String', 'has missing': True}]

        # Create a new deduper object and pass our data model to it.
        deduper = dedupe.Dedupe(fields)

        # If we have training data saved from a previous run of dedupe,
        # look for it and load it in.
        # __Note:__ if you want to train from scratch, delete the training_file
        if os.path.exists(training_file):
            print('reading labeled examples from ', training_file)
            with open(training_file, 'rb') as f:
                deduper.prepare_training(data_d, f)
        else:
            deduper.prepare_training(data_d)

        # ## Active learning
        # Dedupe will find the next pair of records
        # it is least certain about and ask you to label them as duplicates
        # or not.
        # use 'y', 'n' and 'u' keys to flag duplicates
        # press 'f' when you are finished
        print('starting active labeling...')

        dedupe.console_label(deduper)

        # Using the examples we just labeled, train the deduper and learn
        # blocking predicates
        deduper.train()

        # When finished, save our training to disk
        with open(training_file, 'w') as tf:
            deduper.write_training(tf)

        # Save our weights and predicates to disk.  If the settings file
        # exists, we will skip all the training and learning next time we run
        # this file.
        with open(settings_file, 'wb') as sf:
            deduper.write_settings(sf)

    # ## Clustering

    # `partition` will return sets of records that dedupe
    # believes are all referring to the same entity.

    print('clustering...')
    clustered_dupes = deduper.partition(data_d, 0.5)

    print('# duplicate sets', len(clustered_dupes))

    # ## Writing Results

    # Write our original data back out to a CSV with a new column called
    # 'Cluster ID' which indicates which records refer to each other.

    cluster_membership = {}
    for cluster_id, (records, scores) in enumerate(clustered_dupes):
        for record_id, score in zip(records, scores):
            cluster_membership[record_id] = {
                "Cluster ID": cluster_id,
                "confidence_score": score
            }

    with open(output_file, 'w') as f_output, open(input_file) as f_input:

        reader = csv.DictReader(f_input)
        fieldnames = ['Cluster ID', 'confidence_score'] + reader.fieldnames

        writer = csv.DictWriter(f_output, fieldnames=fieldnames)
        writer.writeheader()

        for i, row in enumerate(reader):
            row.update(cluster_membership[i])
            writer.writerow(row)
