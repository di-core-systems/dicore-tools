import os
import re

class Utils:

    def __init__(self):
        self.data = []

    @staticmethod
    def find_csv_files(path):
        files = []
        my_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(my_path, path)

        Utils.find(files, path, '.csv')

        return files;

    @staticmethod
    def find(files, path, expression):
        for file in os.listdir(path):

            if os.path.isdir(path + file):
                Utils.find(files, path + file, expression)

            if re.search(expression, file):
                files.append(path + "/" + file)
                print(file)

        return files

    @staticmethod
    def sort_list(list, pos):
        dict={}

        for entry in list:
            string = entry[0]
            parts = string.split(";")
            index = int(parts[pos])

            if (index not in dict):
                dict[index] = entry
            else:
                dict[index].append(entry)
        result = sorted(dict.iterkeys())
        new_list= []

        for line in dict.values():

            if len(line) > 1:
                i = 0

                for l in line:

                    if i == 0:
                        n_l = []
                        n_l.append(l)
                        new_list.append(n_l)
                    else:
                        new_list.append(l)
                    i=i+1

            else:
                new_list.append(line)
        return new_list

    @staticmethod
    def get_or_create_file(path, filename):

        if os.path.exists(path + "/"+filename):
            file = open(path + "/"+filename, "ab")
        else:
            file = open(path + "/"+filename, "wb")

        return file

    @staticmethod
    def get_nr(filepath):
        filename = filepath[filepath.rindex('/')+1:]
        number = filename[filename.rindex('_')+1:filename.rindex('.csv')]
        return number


    @staticmethod
    def get_expnr(filepath):
        filename = filepath[filepath.rindex('/')+1:]
        path = filepath[:filepath.rindex('/')]

        files = []
        if os.path.isdir(path):
             Utils.find(files, path, '.csv')

        dict={}

        for file in files:
            fname = file[file.rindex('/')+1:]
            number = file[file.rindex('_')+1:file.rindex('.csv')]
            dict[number] = fname

        keys = sorted(dict.keys())

        index = 0

        for key in keys:

            if dict[key] == filename:
                return index
            index+=1

        return -1

    @staticmethod
    def get_agent_count(filepath):

        path = filepath[:filepath.rindex('/')]

        for file in os.listdir(path):

            if re.search('scenario_', file):
                #files.append(path + "/" + file)
                file = open(path + "/"+file, "rb")
                lines = file.readlines()
                line = lines[0]
                count = line[line.rindex(':')+1:line.rindex('\n')]
                return int(count)

        return -1

    @staticmethod
    def get_trainset_size(filepath, expnr):
        path = filepath[:filepath.rindex('/')]

        for file in os.listdir(path):

            if re.search('scenario_', file):
                file = open(path + "/"+file, "rb")
                lines = file.readlines()

                i = 0
                line = ""

                for _line in lines:

                    if "Start point set   :" in _line:

                        if i == expnr:
                            line = _line
                            break
                        i+=1

                #line = lines[1 + (expnr * 3)] # TODO: index count
                trainset = line[line.rindex('Start point set   :')+19:line.rindex('duration')-1]
                return int(trainset)

        return -1

    @staticmethod
    def rm_files(list, path):
        my_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(my_path, path)

        for file_expression in list:
            files = []
            Utils.find(files, path, file_expression)

            for filename in files:
                os.remove(filename)



