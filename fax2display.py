#!/usr/bin/python3
import os
import sys
import tempfile
import time
import pysftp

filename = time.strftime("%C%y%m%d%H%M")

sftp_user = "USERNAME"
sftp_pass = "PASSWORD"

from pdf2image import convert_from_path

def pdf_to_png(source,destino):

    print(f"Converting {source} to {destino}")
    convert_from_path(pdf_path=source,
    dpi=300,
    output_folder=destino,
    fmt="png",
    output_file=filename,
    single_file=True)

def send_fax2display(img_path):
    print(img_path)
    with pysftp.Connection('10.10.10.30', username=sftp_user, password=sftp_pass) as sftp:

        with sftp.cd('/your/dir/of/choice/'): # cd to the display folder
            print("sending", img_path)
            sftp.put(f"{img_path}")  # upload fax


def print_usage():
    print("Gets the first page of a PDF and sends it to the display")
    print("Usage:")
    print("fax2display.py [PATH TO PDF]")
    print("")
    sys.exit()

def main():

    if len(sys.argv) < 2:
        print("pdf_path required")
        print_usage()

    pdf_path = sys.argv[1]

    if pdf_path is None:
        print("pdf_path not set")
        print_usage()

    print(f"Starting fax2display")

    with tempfile.TemporaryDirectory() as path:
        print("Created temp dir", path)
        pdf_to_png(pdf_path, f"{path}")
        print("sending fax to display")
        send_fax2display(f"{path}/{filename}.png")
        print("Sent")

if __name__ == "__main__":
    main()
