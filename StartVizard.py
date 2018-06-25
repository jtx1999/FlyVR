from tkinter import messagebox
import subprocess
from subprocess import PIPE
import argparse


def open_vizard(vizard_path, script_path):
    p = subprocess.Popen([vizard_path, script_path], shell=True,
                         stdout=PIPE, stderr=PIPE)
    output, error = p.communicate()
    if p.returncode != 0:  # Failed to start Vizard
        messagebox.showerror("Error",
                             "Vizard is not configured properly:\n"+output.decode("utf-8")+error.decode("utf-8"))


parser = argparse.ArgumentParser()
parser.add_argument("vizard_path", help="Path for the Vizard program",
                    type=str)
parser.add_argument("script_path", help="Path for the Vizard script",
                    type=str)

args = parser.parse_args()
open_vizard(args.vizard_path, args.script_path)
