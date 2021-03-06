# aggr

An aggregation pipe.

    $ cat data.txt
    Eggs,12
    Chips,13
    Beans,14
    Eggs,21
    Chips,32
    Beans,43

    $ cat data.txt | aggr -p key,sum
    Beans,57
    Chips,45
    Eggs,33

## Why?

Answers to "How do I sum like `uniq -c `" weren't satisfactory.

## Usage

Feed your data through a pipe or specify a file using the `-i` flag. Provide a pattern `-p`. Your pattern must have the same number of fields and delimiter as your data. Possible fields for the pattern are:

* key - the field should form part of your key
* sum
* max
* min
* len - count the records
* first
* last
* any - returns True if any of the fields values are "Truthy", False otherwise.
* A lambda function that can be passed to `reduce`. See below.

## Examples

Dates, times, integers and floats are inferred.

    $ cat data2.txt
    2015-05-13,Eggs,1200
    2015-05-13,Chips,1300
    2015-05-13,Chips,1300
    2015-05-13,Bean,1300
    2015-05-15,Eggs,1300
    2015-05-15,Eggs,1300
    2015-05-15,Eggs,1300
    2015-05-15,Chips,1300
    2015-05-15,Beans,1300

    $ cat data2.txt | aggr -p key,len,sum
    2015-05-13,4,5100
    2015-05-15,5,6500

Composite keys are supported.

    $ cat data2.txt | aggr -p key,key,len
    2015-05-13,Bean,1300
    2015-05-13,Chips,2600
    2015-05-13,Eggs,1200
    2015-05-15,Beans,1300
    2015-05-15,Chips,1300
    2015-05-15,Eggs,3900

Custom aggregators are supported. Since lambdas use commas to separate parameters you must switch your delimiter to something other than a comma.

    $ cat data2.txt | sed 's/,/#/g' |
        aggr -d '#' -p 'key#key#lambda acc,v: int(acc + v / 100)' |
        sed 's/#/,/g'

    2015-05-13,Bean,13
    2015-05-13,Chips,26
    2015-05-13,Eggs,12
    2015-05-15,Beans,13
    2015-05-15,Chips,13
    2015-05-15,Eggs,39

## Install

    $ git clone http://github.com/Horb/aggr.git
    $ ln -s ~/aggr/aggr.py /usr/local/bin/aggr 
    $ aggr --help
    usage: aggr [-h] -p PATTERN [-i INFILE] [-o OUTFILE] [-d FIELD_DELIMITER] [-v]
                [--datetime-format DATETIME_FORMAT] [--time-format TIME_FORMAT]
                [--date-format DATE_FORMAT]

    optional arguments:
      -h, --help            show this help message and exit
      -p PATTERN, --pattern PATTERN
      -i INFILE, --infile INFILE
      -o OUTFILE, --outfile OUTFILE
      -d FIELD_DELIMITER, --field-delimiter FIELD_DELIMITER
      -v, --verbose
      --datetime-format DATETIME_FORMAT
      --time-format TIME_FORMAT
      --date-format DATE_FORMAT
