import csv
import sys
import os
from utils import Utils


class PostProcessing:

    _results = {}

    def __init__(self):
        self._results = {}

    @property
    def results(self):
        return self._results

    def replaceAll(self, row):
        row[0] = row[0].replace(".", ",")
        row[0] = row[0].replace("false", "")
        row[0] = row[0].replace("true", "1")
        row[0] = row[0].replace("new Model: ", "")

    def extractResults(self, lines, filename):
        detected_count  = 0
        false_positive_count = 0
        false_negative_count = 0
        true_positive_count = 0
        true_negative_count = 0
        new_model_count = 0
        avg_model_size = 0
        traffic = 0
        models = []


        detected_count_400 = 0
        false_positive_count_400 = 0
        true_positive_count_400 = 0
        new_model_count_400 = 0
        avg_model_size_400 = 0
        models_400 = []


        agent_count = Utils.get_agent_count(filename)
        nr = Utils.get_nr(filename)
        expnr = Utils.get_expnr(filename)
        trainsetsize = Utils.get_trainset_size(filename, expnr)

        for line in lines[1:]:
            parts = line[0].split(";")

            if 'true' in parts[4]:
                detected_count+=1

                if 'false' in parts[5]:
                    false_positive_count+=1

            if 'true' in parts[5]:
                true_positive_count+=1

                if 'false' in parts[4]:
                    false_negative_count+=1

            if 'false' in parts[4] and 'false' in parts[5]:
                true_negative_count+=1

            if len(parts) > 6:
                new_model_count+=1;
                models.append(parts[6].replace('new Model: ',''))

            # 400 ------
            if lines.index(line) > (400*agent_count):

                if 'true' in parts[4]:
                    detected_count_400+=1

                    if 'false' in parts[5]:
                        false_positive_count_400+=1

                if 'true' in parts[5]:
                    true_positive_count_400 += 1

                if len(parts) > 6:
                    new_model_count_400 += 1;
                    models_400.append(parts[6].replace('new Model: ', ''))


        size = len(lines)-1

        size_400 = size - 400 * agent_count;

        for model in models:
            avg_model_size += int(model)

        if new_model_count > 0:
            avg_model_size = avg_model_size / new_model_count

        # 400 ------
        for model in models_400:
            avg_model_size_400 += int(model)

        if new_model_count_400 > 0:
            avg_model_size_400 = avg_model_size_400 / new_model_count_400

        traffic = detected_count * 631 * 2
        traffic = traffic + (new_model_count * avg_model_size)

        result_overview = []
        result_overview.append("experiment nr   : " + str(nr) +"\n")
        result_overview.append("filename        : " + filename[filename.rindex('/')+1:] +"\n")
        result_overview.append("agent count     : " + str(agent_count) + "\n")
        result_overview.append("train set size  : " + str(trainsetsize) + "\n")
        result_overview.append("detected        : " + str(detected_count) + "\n")
        result_overview.append("true positive   : " + str(true_positive_count) + "\n")
        result_overview.append("true negative   : " + str(true_negative_count) + "\n")
        result_overview.append("false positive  : " + str(false_positive_count) + "\n")
        result_overview.append("   type 1 error : " + str(100.0 / size * false_positive_count) + "\n")
        result_overview.append("false negative  : " + str(false_negative_count) +"\n ")
        result_overview.append("   type 2 error : " + str(100.0 / size * false_negative_count) + "\n")
        result_overview.append("diff            : " + str(detected_count - true_positive_count) + "\n")
        result_overview.append("generated models: " + str(new_model_count) + "\n")
        result_overview.append("avg model size  : " + str(avg_model_size) + "\n")

        result_overview.append("detected  400   : " + str(detected_count_400) + "\n")
        result_overview.append("diff 400        : " + str(detected_count_400 - true_positive_count_400) + "\n")
        result_overview.append("f p  400        : " + str(false_positive_count_400) +"\n")
        result_overview.append("type 1 error 400: " + str(100.0 / (size - (400*agent_count)) * false_positive_count_400) + "\n")
        result_overview.append("avg m size 400  : " + str(avg_model_size_400) +"\n")

        result_overview.append("learning rate   : " + str(100-(100.0 / size * false_positive_count)) + "\n")
        result_overview.append("network traffic : " + str(traffic) + "\n")

        result_overview.append("size            : " + str(size) + "\n")
        result_overview.append("size 400        : " + str(size_400) + "\n")
        result_overview.append("generated models 400 : " + str(new_model_count_400) + "\n\n")

        parent_path = os.path.abspath(os.path.join(filename, os.pardir))
        file = Utils.get_or_create_file(parent_path, "result.txt")
        #file = open(parent_path + "/result.txt", "ab")
        file.write(''.join(map(str, result_overview)))
        file.close()

        csv_content = []
        csv_content.append(str(nr))
        csv_content.append(filename[filename.rindex('/')+1:])
        csv_content.append(str(agent_count))
        csv_content.append(str(trainsetsize))
        csv_content.append(str(size))
        csv_content.append(str(detected_count))
        csv_content.append(str(true_positive_count))
        csv_content.append(str(true_negative_count))
        csv_content.append(str(false_positive_count))
        csv_content.append(str(100.0 / size * false_positive_count))
        csv_content.append(str(false_negative_count))
        csv_content.append(str(100.0 / size * false_negative_count))
        csv_content.append(str(detected_count - true_positive_count))
        csv_content.append(str(new_model_count))
        csv_content.append(str(avg_model_size))
        csv_content.append(str(detected_count_400))
        csv_content.append(str(detected_count_400 - true_positive_count_400))
        csv_content.append(str(false_positive_count_400))
        csv_content.append(str(100.0 / (size - (400*agent_count)) * false_positive_count_400))
        csv_content.append(str(avg_model_size_400))
        csv_content.append(str(100-(100.0 / size * false_positive_count)))
        csv_content.append(str(traffic))
        csv_content.append(str(size))
        csv_content.append(str(size_400))
        csv_content.append(str(new_model_count_400))

        self._results[filename[filename.rindex('/') + 1:]] = csv_content


        if not os.path.exists(parent_path + "/"+"resulttable.txt"):
            header = ["nr; filename; agent count; train set size; dataset size; detected; true positive; true negative; "
                      "false positive; type 1 error; false negative; type 2 error; diff; generated models; avg model size; "
                      "detected 400; diff 400; f p 400; type 1 error 400; avg m size 400; learing rate; network traffic; size; size 400; generated models 400 "]
            file = Utils.get_or_create_file(parent_path, "resulttable.txt")
            writer = csv.writer(file, delimiter='\t')
            writer.writerow(header)
            file.close()

        file = Utils.get_or_create_file(parent_path, "resulttable.txt")
        writer = csv.writer(file, delimiter=';')
        #writer = csv.writer(open(parent_path + "/resulttable.txt", "ab"), delimiter=';')
        writer.writerow(csv_content)
        file.close()

    def start_processing(self):
        header = ["Agent ID; DataX; Timestamp; DataY; Detected; Validated; New Model"]
        Utils.rm_files(["resulttable.txt", "result.txt"] ,"../statistics/")
        files = Utils.find_csv_files("../statistics/")

        for filename in files:
            lines = []
            # lines.append(header)
            reader = csv.reader(open(filename, "rb"))
            try:
                for row in reader:

                    if (len(row) != 0):
                        lines.append(row)
            except csv.Error, e:
                sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))
            writer = csv.writer(open(filename.replace(".csv", ".txt"), "wb"), delimiter='\t')
            lines = Utils.sort_list(lines, 1)
            lines.insert(0, header)
            self.extractResults(lines, filename)

            for row in lines:
                self.replaceAll(row)
                writer.writerow(row)

        self.combine_data()

    def combine_data(self):

        data, name = self.create_table(12)
        self.write_csv_table(data, name, "DIFF")

        data, name = self.create_table( 9)
        self.write_csv_table(data, name, "FALSE_POSTIVE")

        data, name = self.create_table( 11)
        self.write_csv_table(data, name, "FALSE_NEGATIVE")

        data, name = self.create_table( 13)
        self.write_csv_table(data, name, "GENERATED_MODELS")

        data, name = self.create_table( 14)
        self.write_csv_table(data, name, "AVG_MODEL_SIZE")

        data, name = self.create_table( 16)
        self.write_csv_table(data, name, "DIFF_400")

        data, name = self.create_table( 18)
        self.write_csv_table(data, name, "FALSE_POSTIVE_400")

        data, name = self.create_table( 19)
        self.write_csv_table(data, name, "AVG_MODEL_SIZE_400")

        data, name = self.create_table( 20)
        self.write_csv_table(data, name, "LEARNING_RATE")

        data, name = self.create_table( 21)
        self.write_csv_table(data, name, "TRAFFIC")

        data, name = self.create_table( 24)
        self.write_csv_table(data, name, "GENERATED_MODELS_400")

        # data.append(value[2]) # agents
        # data.append(value[3]) # trainset
        # data.append(value[12]) # diff
        # data.append(value[9]) # false positive
        # data.append(value[15]) # detected_count_400
        # data.append(value[16]) # diff 400
        # data.append(value[17]) # false positive 400
        # data.append(value[18]) # avg_model_size_400


    def create_table(self, index):
        sa = "SERVICEAGENT"
        ca = "CLIENTAGENT"
        name = ""
        data = {}

        for exp in self._results:
            value = self._results.get(exp)
            name = value[1]
            trainsetsize = int(value[3])
            diff = float(value[index])

            if diff.is_integer():
                diff = int(diff)

            if sa in name:

                if not data.has_key(sa):
                    data[sa] = {}
                diffset = data[sa]

            elif ca in name:

                if not data.has_key(ca):
                    data[ca] = {}
                diffset = data[ca]

            if not diffset.has_key(trainsetsize):
                diffset[trainsetsize] = [diff]
            else:
                diffset[trainsetsize].append(diff)
        return data, name

    def write_csv_table(self, data, name, nameext):
        parent_path = os.path.abspath(os.path.join(name, os.pardir))
        for a in data:
            keys = sorted(data[a].keys())

            if not os.path.exists(parent_path + "/../statistics/" + a + "_" + nameext + "_Table.csv"):
                csv_header = []

                for key in keys:
                    csv_header.append(key)

                file = Utils.get_or_create_file(parent_path + "/../statistics", a + "_" + nameext +"_Table.csv")
                writer = csv.writer(file, delimiter=';')
                writer.writerow(csv_header)
                file.close()

            # for index in range(0, len(data[a][0])):
            for index in range(0, len(data[a].keys())):
                csv_content = []

                for key in sorted(keys):
                    _set = data[a][key]

                    if index < len(_set):
                        csv_content.append(_set[index])

                file = Utils.get_or_create_file(parent_path + "/../statistics", a + "_" + nameext + "_Table.csv")
                writer = csv.writer(file, delimiter=';')
                writer.writerow(csv_content)
                file.close()
