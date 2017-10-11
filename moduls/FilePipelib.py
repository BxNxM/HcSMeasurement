import os

# get source path parent's folder parent's folder
source_dirname = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pipePath = source_dirname + '/DataBase/ConsolePipe'

class FilePipe():
    """ This is a simple communications between running python programs """

    def __init__(self, path):
        if os.path.exists(path):
            self.path = path
        else:
            self.path = path
            self.WritePipe("Pipe file created")

    def ReadPipe(self):
        if os.stat(self.path).st_size != 0:
            #open file with safe mode (with) close not needed
            with open(self.path, 'r') as file:
                #read file to message
                self.message = file.read()
                #cleanf file after read
                open(self.path, 'w').close()
                return self.message
        else:
            return None

    def WritePipe(self, message):
        self.message = str(message)
        with open(self.path, 'a') as file:
            file.write(self.message)
            return True

def InitPipe():

    #pipe = FilePipe("DataBase/ConsolePipe")
    pipe = FilePipe(pipePath)
    return pipe

if __name__ == "__main__":

    #pipe = FilePipe("DataBase/ConsolePipe")
    pipe = FilePipe(pipePath)
    pipe.WritePipe("Hello bello")
    m = pipe.ReadPipe()
    print(m)
