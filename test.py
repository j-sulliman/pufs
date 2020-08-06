import argparse
parser = argparse.ArgumentParser(description='Configure UCS from spreadsheet')
parser.add_argument('-a', help='UCSM IP (a)ddress (not URL)',type=str,
                    required=False)
parser.add_argument('-u', help='UCSM (u)ser name',type=str, required=False)
parser.add_argument('-p', help='UCSM (p)assword',type=str, required=False)
parser.add_argument('-f', help='Excel Spreadsheet File Name and Path',type=str,
                    required=False)
args = parser.parse_args()
print(args.u)
