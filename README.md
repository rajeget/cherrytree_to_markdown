# cherrytree_to_markdown

## What and Why ? 
Simple program to covert Cherrytree exported html file to markdown. The reason for creating this was because the export from cherrytree to html is clean , but import to html from markdown is not . Used multiple tools like Pandoc but nothing worked. . BEST works with obsidian .

## How to use ?
Export cherrytree notes into html , use this html file as input to the script . It is a simple python3 script. 

```console 
python3 cherrytree_to_markdown.py -h
usage: cherrytree_to_markdown.py [-h] --file FILE_ROOT

optional arguments:
  -h, --help            show this help message and exit
  --file FILE_ROOT, -f FILE_ROOT
                        Enter the cherry tree exported html 
```
