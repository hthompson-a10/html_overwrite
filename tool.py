import bs4
import os
import re
import sys


class html_list(object):

    def __init__(self, directory_path):
        # os.walk returns a 3-tuple of (dirpath, dirnames, filenames)
        self.filenames = next(os.walk(directory_path))[2]
        self.max_index = len(self.filenames) - 1
        self.curr_index = -1

    def __iter__(self):
        return self
    
    def __next__(self):
        return self.next()

    def next(self):
        if self.curr_index < self.max_index:
            self.curr_index += 1
            file_name = self.filenames[self.curr_index]
            if re.search(".*\.html$", file_name):
                return file_name
            else:
                self.next()
        raise StopIteration()


def overwrite_file(file_name, element, num_elem):
    """
    Credit to https://stackoverflow.com/questions/11469228/replace-and-overwrite-instead-of-appending
    for the seek() and truncate() idea.

    seek() puts us at the start of the file. write() will output content and set the offset to just after
    the content. truncate() will remove everything after the offset.
    """
    with open(file_name, "r+") as f:
        raw_data = f.read()
        file_soup = bs4.BeautifulSoup(raw_data, features="html.parser")
        elem_foud = file_soup.find_all(element)[:num_elem]
        f.seek(0)
        f.write(str(elem_foud))
        f.truncate()


def main():
    """
        python tool.py <directory_path> <html_element_type> <num_of_elems>

        Most likely desired is `` python tool.py . 'table' 1 ``
    """
    for file_name in html_list(sys.argv[1]):
        overwrite_file(file_name, sys.argv[2], int(sys.argv[3]))

main()
