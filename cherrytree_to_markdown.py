#!/usr/bin/python

import os,pathlib,shutil,subprocess,re
from os import path
import argparse

# directory from where code is picked
root = '/'

def check_if_string_in_file(file_name, string_to_search):
    # Author : https://thispointer.com/python-search-strings-in-a-file-and-get-line-numbers-of-lines-containing-the-string/
    """ Check if any line in the file contains given string """
    # Open the file in read only mode
    with open(file_name, 'r') as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            # For each line, check if line contains the string
            if string_to_search in line:
                return True
    return False

def find_image_place_into_attachment(createpath):
    # the the images in the html file and move them into a new folder attachment . Move the image from the base images folder to this new attachment folder
    #check_if_string_in_file(createpath,"something")
    pattern = re.compile("images")
    for line in open(createpath):
        for match in re.finditer(pattern,line):
            print(line)

def scan_recursive(fpath):
    """Recursively iterate all the .py files in the root directory and below"""
    for path, dirs, files in os.walk(fpath):
        yield from ((path, file) for file in files if pathlib.Path(file).suffix == '.html')

def create_file_folder_structure(root_path):
    i = 0
    for fpath, ffile in scan_recursive(root_path):
        splitfile = ffile.split('--')
        oldFilepath = os.path.join(fpath,ffile)
        for sfiles in splitfile:
            createpath = os.path.join(fpath, sfiles)
            fpath = os.path.join(fpath, sfiles)
            if not('.html' in createpath): # its a folder
                if (path.exists(createpath)):
                    print("this is already exisitng ",createpath)
                else: #create Folder
                    os.makedirs(createpath)
            else: # files is a html file
                i = i +1
                print("Exisiting",oldFilepath,path.exists(oldFilepath))
                print("Exisiting",createpath,path.exists(createpath))
                # move file
                new_path = shutil.move(oldFilepath,createpath)
                # change the images to the repective folder
                find_image_place_into_attachment(createpath)
    print("Made ",i, " changes")

# Covert all html to md
def convert_html_to_md(root_path):
    # Bash script
    batch_script = 'find '+root_path+' -name "*.html" | while read i; do pandoc -f html -t markdown_strict "$i" -o "${i%.*}.md"; done'
    print(batch_script)
    subprocess.call(batch_script, shell=True)

# Delete html files
def convert_del_html(root_path):
    # Bash script
    batch_script = 'find '+root_path+'/. -name "*.html" | while read i; do rm $i; done'
    subprocess.call(batch_script, shell=True)

def string_cleanup(root_path,oldstring,newstring):
    batch_script = 'find '+ root_path +' -name "*.md" -exec sed -i \'s/"'+oldstring+'"/'+newstring+'/g\' {} +'
    print(batch_script)
    subprocess.call(batch_script, shell=True)

def cleanup(root_path):
    # delete html files
    convert_del_html(root_path)
    #Some how this is always found in the bottom of the html - better to cleanup
    #string_cleanup(root_path,'<img src=\"images/home.svg\" width=\"22\" height=\"22\" /> [Index](index.html)','')


def covert_actions(file_root):
    try:
        print('[+] Creating file structure.')
        create_file_folder_structure(root)
        # change the code block
        # move the relevant images from global location to ./attachment/
        # change the images to attachment folder
        print('[+] Coverting html to md')
        convert_html_to_md(root)
        print('[+] Clearnin up')
        cleanup(root)
    except Error as e:
        print('[-] Terminated with error')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', '-f',
                        required=True,
                        dest='file_root',
                        help='Enter the cherry tree exported html')
    args = parser.parse_args()

    covert_actions(args.file_root)
