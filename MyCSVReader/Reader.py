import csv # for reading csv files

class Reader(object):
    def __init__(self, file_name, height):
        self.__curr_line = 0               # line that holds first row of the page
        self.__block_size = height         # block_size holds number of rows at page
        self.open_file(file_name)

    def read_head(self):
        self.__curr_line = 1               # reads header (first line of file)
        return self.__reader[0]

    def readln(self, next):
        if next:                         # reads next line
            if self.__curr_line + self.__block_size != self.__size: # reads if last line on the page not equal to last page of the file
                self.__curr_line += 1
        else:                            # reads previous line
            if self.__curr_line != 1 :     # reads if line not equal to 1
                self.__curr_line -= 1
        return self.__reader[self.__curr_line:self.__curr_line+self.__block_size]

    def readpg(self, next):
        if next:                         # reads next page
            if self.__curr_line > self.__size - 2*self.__block_size : # if (size - curr_line) is less than page height
                self.__curr_line = self.__size - self.__block_size    # then next page starts from (size - page) height
            else:                                               
                self.__curr_line += self.__block_size
        else:                            # reads previous page
            if self.__curr_line - self.__block_size >= 0: 
                self.__curr_line -= self.__block_size
            else:
                self.__curr_line = 1
        return self.__reader[self.__curr_line:self.__curr_line+self.__block_size]

    def open_file(self, file_name):
        self.file = file_name
        self.__reader = list()
        i = 0
        with open(file_name, newline='') as csvfile:
            file = csv.reader(csvfile)      
            for row in file:
                self.__reader.append(row)
        self.__size = len(self.__reader)          # rows count
        self.widths = {a: 0 for a in range(len(self.__reader[0]))} # dictionary with columns widths
        for row in self.__reader:
            i = 0
            for word in row:
                if len(word) > self.widths.get(i):
                    self.widths[i] = len(word)
                i += 1

    def to_begin(self):
        self.__curr_line = 1
        return self.__reader[self.__curr_line:self.__curr_line+self.__block_size]

    def to_end(self):
        self.__curr_line = self.__size - self.__block_size
        return self.__reader[self.__curr_line:self.__size]

    def get_block_size(self):
        return self.__block_size