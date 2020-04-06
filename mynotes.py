#!/usr/bin/env python3
# This script will store personal notes entered on the CLI
# They are stored as Base64 strings, and can be ~any size
# It presumes the existence of ~/mynotes/mynotes.db
# If that file doesn't exist, touch ~/mynotes/mynotes.db
# Ideally, ~/mynotes/ would be a veracrypt mount point
# ./mynotes.py --help will provide usage switches
##

'''store personal notes'''

import argparse,sys,base64,time,os

def main():
    db_file=os.environ['HOME']+"/mynotes/mynotes.db" #mkdir ~/mynotes/
    parser = argparse.ArgumentParser(description='Store Personal Notes')
    parser.add_argument('-a', '--add', action='store_true', help='add note with current datetime (default)')
    parser.add_argument('-s', '--search', help='case insensitive search notes for arg')
    parser.add_argument('-d', '--display', help='display notes for YYYYMMDD date substring match')
    parser.add_argument('-e', '--export', action='store_true', help='export all notes to STDOUT')
    args = parser.parse_args()
    # search, display, export
    if args.search:
        with open(db_file) as notes:
            for line in notes:
                datetime_stamp,byte_line = line.split(",")
                byte_line = bytes(byte_line, "utf-8")
                str_line = base64.b64decode(byte_line.decode("utf-8")).decode("utf-8").rstrip()
                if (args.search.casefold() in str_line.casefold()): #if the note line matches, print it
                    print(datetime_stamp+","+str(str_line),sep="")
            notes.close()
        return

    if args.display:
        with open(db_file) as notes:
            for line in notes:
                datetime_stamp,byte_line = line.split(",")
                byte_line = bytes(byte_line, "utf-8")
                str_line = base64.b64decode(byte_line.decode("utf-8")).decode("utf-8").rstrip()
                if (args.display in datetime_stamp): #if the date matches, print it
                    print(datetime_stamp+","+str(str_line),sep="")
            notes.close()
        return

    if args.export:
        with open(db_file) as notes:
            for line in notes:
                datetime_stamp,byte_line = line.split(",")
                byte_line = bytes(byte_line, "utf-8")
                str_line = base64.b64decode(byte_line)
                print(datetime_stamp + "," + str_line.decode("utf-8").rstrip(),sep="")
            notes.close()
        return

    # Add Mode (default)
    else:
        print('Enter your note, end with newline + ctrl-d')
        time_str=time.strftime('%Y%m%d%H%M%S', time.localtime())
        cli_note = sys.stdin.read().rstrip()
        if not cli_note:
            print("Nothing entered, nothing written.")
            return
        cli_note_encoded = base64.b64encode(str.encode(cli_note,"utf-8", "replace")) #encode multi-line input to base64
        note_file = open(db_file, 'a') #open file for appending, at the end
        note_file.write(time_str + "," + cli_note_encoded.decode("utf-8") +"\n") #convert to string to write to file
        note_file.close() # and close file handle

if __name__ == "__main__":
    main()
