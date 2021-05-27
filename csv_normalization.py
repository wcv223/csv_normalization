"""
Program Name - csv_normalization
Python version - python3 9.5
Author - William Cody Villarreal
Date - 05/25/2021
Purpose - Normalize CSV File with the fields timestamp, address, zip, full name, foo duration, bar duration, total
          duration, and notes. Headers are expected for row one. The file should use a UTF-8 character set.
Revisions - 05/25/2021 Cody Villarreal Started coding
"""


import sys
import csv
import os
from zoneinfo import ZoneInfo
from datetime import datetime, timedelta


class CsvNormalization:
    """
    Input CSV file and normalize fields Timestamp, Address, Zip, Full Name, Foo Duration, Bar Duration, Total Duration,
    and notes.
    """
    def __init__(self):
        self.csv_file_list = []
        self.csv_normalized_list = []
        self.foo_seconds = 0
        self.bar_seconds = 0

    def audit_input_file_type(self):
        """
        Checks to see if the input file is a csv
        """
        filename = sys.argv[1]
        name, extension = os.path.splitext(filename)
        if extension == '.csv':
            return True

    def audit_output_file_type(self):
        """
        Checks to see if the input file is a csv
        """
        filename = sys.argv[2]
        name, extension = os.path.splitext(filename)
        if extension == '.csv':
            return True

    def open_csv(self):
        """
        Opens CSV file and ignores non utf-8 characters and creates a list of lists with csv rows.
        """
        filename = sys.argv[1]

        with open(filename, mode='r', newline='', encoding='utf-8', errors='ignore') as file:
            csv_file = csv.reader(file)
            self.csv_file_list = list(csv_file)

    def determine_csv_length(self):
        """
        return the number of rows in the csv file.
        """
        return len(self.csv_file_list)

    def process_header(self):
        """
        Move header to hold list.
        """
        self.csv_normalized_list.append(self.csv_file_list[0])

    def add_new_row_to_normalized_list(self):
        """
        append new blank list to hold list.
        """
        self.csv_normalized_list.append([])

    def convert_pdt_to_est(self, row):
        """
        converts timestamp from pdt/pst to est and appends normalized timestamp to the hold list.
        :param row: int - the row currently being worked on
        """
        timestamp_strip = datetime.strptime(self.csv_file_list[row][0], "%m/%d/%y %I:%M:%S %p")
        timestamp_with_timezone = timestamp_strip.replace(tzinfo=ZoneInfo("America/Los_Angeles"))
        timestamp_est = timestamp_with_timezone.astimezone(ZoneInfo('US/Eastern'))
        self.csv_normalized_list[row].append(timestamp_est)

    def move_address_to_normalized_list(self, row):
        """
        No changes made to address. The address is appended to the hold list.
        :param row: int - the row currently being worked on
        """
        self.csv_normalized_list[row].append(self.csv_file_list[row][1])

    def audit_zip(self, row):
        """
        Check to see if zip is a number.
        :param row: int - the row currently being worked on
        """
        return self.csv_file_list[row][2].isnumeric()

    def normalize_five_digit_zip(self, row):
        """
        All zips should be five digits long and padded with zeros if shorter. Appends normalized zip to the hold list.
        :param row: int - the row currently being worked on
        """
        zip_normalized = self.csv_file_list[row][2].zfill(5)
        self.csv_normalized_list[row].append(zip_normalized)

    def normalize_uppercase_name(self, row):
        """
        Make full name all uppercase. Appends normalized full name to the hold list.
        :param row: int - the row currently being worked on
        """
        uppercase_name = self.csv_file_list[row][3].upper()
        self.csv_normalized_list[row].append(uppercase_name)

    def foo_duration_to_seconds(self, row):
        """
        Change time (hour, minute, second, millisecond) to seconds. Appends normalized foo duration to the hold list.
        :param row: int - the row currently being worked on
        """
        time_sans_period = self.csv_file_list[row][4].replace('.', ':')
        h, m, s, ms = time_sans_period.split(':')
        foo_duration_seconds = timedelta(hours=int(h), minutes=int(m), seconds=int(s),
                                         milliseconds=int(ms)).total_seconds()

        self.csv_normalized_list[row].append(foo_duration_seconds)
        self.foo_seconds = foo_duration_seconds

    def bar_duration_to_seconds(self, row):
        """
        Change time (hour, minute, second, millisecond) to seconds. Appends normalized bar duration to the hold list.
        :param row: int - the row currently being worked on
        """
        time_sans_period = self.csv_file_list[row][5].replace('.', ':')
        h, m, s, ms = time_sans_period.split(':')
        bar_duration_seconds = timedelta(hours=int(h), minutes=int(m), seconds=int(s),
                                         milliseconds=int(ms)).total_seconds()

        self.csv_normalized_list[row].append(bar_duration_seconds)
        self.bar_seconds = bar_duration_seconds

    def total_duration(self, row):
        """
        Add bar and foo duration together to get duration. Appends normalized total duration to the hold list.
        Total duration from csv is ignored since it is filled with garbage data.
        :param row: int - the row currently being worked on
        """
        total_duration_seconds = self.foo_seconds + self.bar_seconds
        self.csv_normalized_list[row].append(total_duration_seconds)

    def move_notes_to_normalized_list(self, row):
        """
        No changes made to notes. The notes are appended to the hold list.
        :param row: int - the row currently being worked on
        """
        self.csv_normalized_list[row].append(self.csv_file_list[row][7])

    def write_new_csv(self):
        """
        Using the hold list of list filled with the normalized data write to a new csv file
        """
        filename = sys.argv[2]
        with open(filename, 'w', newline='', encoding='utf-8') as new_csv_file:
            csv_normalized = csv.writer(new_csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            for row in self.csv_normalized_list:
                csv_normalized.writerow(row)

    def drop_rows(self, rows):
        """
        if an error occurs the entire row is dropped and the user is notified
        :param rows: int - the row currently being worked on
        """
        for row in rows:
            self.csv_normalized_list.pop(row[0])
            display_row = row[0] + 1
            print(f"Row {display_row} was dropped. Was not able to normalize {row[1]}.")


def main():
    rows_to_drop = []

    csv_normalizer = CsvNormalization()

    if not csv_normalizer.audit_input_file_type():
        print("Input file needs to be a csv.")
        quit()

    if not csv_normalizer.audit_output_file_type():
        print("Output file needs to be a csv.")
        quit()

    try:
        csv_normalizer.open_csv()
    except:
        print("Not able to open file.")
        quit()

    csv_length = csv_normalizer.determine_csv_length()
    if csv_length <= 0:
        print("CSV file being read is empty. Program ended early. ")
        quit()

    csv_normalizer.process_header()

    for row_number in range(1, csv_length):

        csv_normalizer.add_new_row_to_normalized_list()

        try:
            csv_normalizer.convert_pdt_to_est(row_number)
        except ValueError:
            rows_to_drop.insert(0, [row_number, "Timestamp"])
            continue

        try:
            csv_normalizer.move_address_to_normalized_list(row_number)
        except:
            # Should not error, but if method is updated except condition should be reviewed
            rows_to_drop.insert(0, [row_number, "Address"])
            continue

        if not csv_normalizer.audit_zip(row_number):
            rows_to_drop.insert(0, [row_number, "Zip Code"])
            continue

        try:
            csv_normalizer.normalize_five_digit_zip(row_number)
        except:
            # Should not error, but if method is updated except condition should be reviewed
            rows_to_drop.insert(0, [row_number, "Zip Code"])
            continue

        try:
            csv_normalizer.normalize_uppercase_name(row_number)
        except:
            # Should not error, but if method is updated except condition should be reviewed
            rows_to_drop.insert(0, [row_number, "Full Name"])
            continue

        try:
            csv_normalizer.foo_duration_to_seconds(row_number)
        except ValueError:
            rows_to_drop.insert(0, [row_number, "Foo Duration"])
            continue

        try:
            csv_normalizer.bar_duration_to_seconds(row_number)
        except ValueError:
            rows_to_drop.insert(0, [row_number, "Bar Duration"])
            continue

        try:
            csv_normalizer.total_duration(row_number)
        except:
            # Should not error, but if method is updated except condition should be reviewed
            rows_to_drop.insert(0, [row_number, "Total Duration"])
            continue

        try:
            csv_normalizer.move_notes_to_normalized_list(row_number)
        except:
            # Should not error, but if method is updated except condition should be reviewed
            rows_to_drop.insert(0, [row_number, "Notes"])
            continue

    if rows_to_drop:
        csv_normalizer.drop_rows(rows_to_drop)

    csv_normalizer.write_new_csv()
    print("Normalization completed")


if __name__ == "__main__":
    main()
