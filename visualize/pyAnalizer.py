import os

class AnalizeStructure():
    def __init__(self, root_folder, outputpath="pyoutput.txt"):
        self.root_folder = root_folder
        self.source_structure = {}
        self.outputpath = outputpath

    def get_structure(self, ftype, fnotype):
        file_depth = []
        layer = 0
        for (dirpath, dirnames, filenames) in os.walk(self.root_folder):
            is_python = False
            python_files = []
            for f in filenames:
                if ftype in f and fnotype not in f:
                    is_python = True
                    python_files.append(dirpath + "/" + f)
            if is_python:
                file_depth.append(python_files)
            self.source_structure["type:" + str(ftype)] = file_depth

    def get_relevant_files_structure(self):
        self.get_structure(ftype=".py", fnotype=".pyc")
        self.get_structure(ftype=".txt", fnotype="-")
        self.get_structure(ftype=".log", fnotype="-")

    def echo_structure(self):
        #datastruct = {type0: [[layer1, file2] [layer2] [layerX]],
        #              type2: [[layer1, filex] [layer2] [layerX]],
        #              typeX: [[layer1] [layer2] [layerX, filey]]}
        for key in self.source_structure:
            for layer, files in enumerate(self.source_structure[key]):
                print("KEY[{}] LAYER[{}]\t-=-\t{}".format(key, layer, files))

    def get_relevant_file_content(self):
        output_container = ""
        file_counter = 0
        for key in self.source_structure:
            if ".py" in str(key):
                for layer, files in enumerate(self.source_structure[key]):
                    for file_ in files:
                        file_counter += 1
                        string = self.read_file(file_)
                        structure_str = self.analize_file(string)
                        msg = "-"*80 + "\n"
                        msg += "LAYER\t" + str(layer) + "\t" + str(file_) + "\n"
                        msg += "-"*80 + "\n"
                        msg += structure_str
                        print(msg)
                        output_container+=msg
        lines = len(output_container.rstrip().split('\n'))
        summary = "Generated lines: {} pcs".format(lines)
        summary += "\nAnalized files: {} pcs".format(file_counter)
        summary += "\nProject forders: {} pcs".format(len(self.source_structure))
        print(summary)
        output_container += "\n" + summary
        self.write_to_file(output_container)

    def analize_file(self, content, findobj=["import ", "class ", "def "]):
        selected_msg = ""
        if content is not None:
            content_list = content.splitlines()
            for line in content_list:
                for obj in findobj:
                    if str(obj) in line:
                        selected_msg += line + "\n"
            return selected_msg
        else:
            return None

    def read_file(self, path):
        try:
            with open(path, "r") as f:
                string = f.read()
            return string
        except Exception as e:
            print(e)
            return None

    def write_to_file(self, content):
        try:
            with open(self.outputpath, "w") as f:
                f.write(content)
        except Exception as e:
            print(e)
            return False
        return True

if __name__ == "__main__":
    path = "/Users/bnm/PycharmProjects/HcSMeasurement/"
    astruc = AnalizeStructure(path)
    astruc.get_relevant_files_structure()
    #astruc.echo_structure()
    astruc.get_relevant_file_content()
