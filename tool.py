import bs4
import os
import re
import sys


def html_list(directory_path):
        filenames = next(os.walk(directory_path))[2]
        max_index = len(filenames)
        curr_index = 0
        while curr_index < max_index:
            file_name = filenames[curr_index]
            if re.search(".*\.html$", file_name):
                yield file_name
            curr_index += 1
            

def overwrite_file(file_name, element):
    """
    Credit to https://stackoverflow.com/questions/11469228/replace-and-overwrite-instead-of-appending
    for the seek() and truncate() idea.

    seek() puts us at the start of the file. write() will output content and set the offset to just after
    the content. truncate() will remove everything after the offset.
    """
    with open(file_name, "r+") as f:
        raw_data = f.read()
        file_soup = bs4.BeautifulSoup(raw_data, features="html.parser")
        elem_found = file_soup.find_all(element)
        if elem_found:
            f.seek(0)
            f.write(str(elem_found[0]))
            f.truncate()


def main():
    """
        python tool.py <directory_path> <html_element_type> <num_of_elems>

        Most likely desired is `` python tool.py . 'table' 1 ``
    """
    directory_path = sys.argv[1]
    element_type = sys.argv[2]
    for file_name in html_list(directory_path):
        rel_path = os.path.join(directory_path, file_name)
        overwrite_file(rel_path, element_type)

main()
