import src.tools.morphs.morphs_files as file_tool
import src.tools.morphs.morphs_format as morphs_format

def morphs_from_all(files):
    raw_morphs = []
    for file in files:
        raw_morphs += file_tool.get_morphs_from(file)

    return raw_morphs

def merge_morphs(files):
    morphs = morphs_from_all(files)
    asorted = morphs_format.sort(morphs)
    formatted = morphs_format.format(asorted)

    print(formatted)
