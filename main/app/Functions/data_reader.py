import os

def data_reader(filepath):
  
  fileDir = os.path.dirname(os.path.realpath(__file__))
  filename = os.path.join(fileDir, filepath)
  filename = os.path.abspath(os.path.realpath(filename))
  file_data = open(filename, "r")
  return file_data



  


