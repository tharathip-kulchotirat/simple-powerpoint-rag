import os
def get_info():
    root = 'src/assets/slides/'
    files = [pptx_file for pptx_file in os.listdir(root) if pptx_file[-5:] == '.pptx']
    return files