import src.tools.morphs.morphs_files as file_tool
import src.tools.morphs.morphs_format as morphs_format

def merge_morphs(files):
    morphs = file_tool.morphs_from_files(files)
    asorted = morphs_format.sort(morphs)
    formatted = morphs_format.format(asorted)

    print(formatted)
