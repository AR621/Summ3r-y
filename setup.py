from summ3ry.app import app
import os

def project_directory():
    summ3ry_structure = (os.listdir(os.path.join(os.getcwd(), 'summ3ry')))
    # print(summ3ry_structure)
    if 'text' not in summ3ry_structure:
        os.makedirs(os.path.join(os.path.join(os.getcwd(), 'summ3ry' ), 'text'))
    if 'downloads' not in summ3ry_structure:    
        os.makedirs(os.path.join(os.path.join(os.getcwd(), 'summ3ry' ), 'downloads'))
    if 'uploads' not in summ3ry_structure:
        os.makedirs(os.path.join(os.path.join(os.getcwd(), 'summ3ry' ), 'uploads'))

project_directory()
app.run(debug=True)
