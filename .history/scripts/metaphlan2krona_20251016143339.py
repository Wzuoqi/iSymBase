#!/usr/bin/env python

# ==============================================================================
# Conversion script: from MetaPhlAn output to Krona text input file
# Author: Daniel Brami (daniel.brami@gmail.com)
# Updated by: Your Name
# ==============================================================================

import sys
import optparse
import re

def main():
    # Parse Command Line
    parser = optparse.OptionParser()
    parser.add_option('-p', '--profile', dest='profile', default='', action='store', help='The input file is the MetaPhlAn standard result file')
    parser.add_option('-k', '--krona', dest='krona', default='krona.out', action='store', help='the Krona output file name')
    (options, spillover) = parser.parse_args()

    if not options.profile or not options.krona:
        parser.print_help()
        sys.exit()

    re_candidates = re.compile(r"s__")
    re_replace = re.compile(r"\w__")
    re_bar = re.compile(r"\|")

    with open(options.profile, 'r') as f:
        metaPhLan = f.readlines()

    with open(options.krona, 'w') as metaPhLan_FH:
        for aline in metaPhLan:
            if re.search(re_candidates, aline):
                aline = aline.strip()
                x = re.sub(re_replace, '\t', aline)
                x = re.sub(re_bar, '', x)
                x_cells = x.split('\t')

                # Check last column and remove until a float is found
                while x_cells:
                    try:
                        abundance = float(x_cells[-1])
                        lineage = '\t'.join(x_cells[:-2])
                        metaPhLan_FH.write(f'{abundance}\t{lineage}\n')
                        break
                    except ValueError:
                        x_cells.pop()  # Remove the last element if it's not a float
                    except IndexError:
                        print(f"Skipping line, no more elements to check: {aline}")
                        break

if __name__ == '__main__':
    main()