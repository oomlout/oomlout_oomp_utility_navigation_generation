import os
import yaml
import glob
import copy
import jinja2    
import shutil


folder_configuration = "configuration"
folder_configuration = os.path.join(os.path.dirname(__file__), folder_configuration)

folder_navigation = "navigation"


file_configuration = os.path.join(folder_configuration, "configuration.yaml")
#import templates
with open(file_configuration, 'r') as stream:
    try:
        configuration = yaml.load(stream, Loader=yaml.FullLoader)
    except yaml.YAMLError as exc:   
        print(exc)


def main(**kwargs):

        
    
    folder = kwargs.get("folder", f"os.path.dirname(__file__)/parts")
    folder = folder.replace("\\","/")
    
    kwargs["file_template_list"] = configuration
    print(f"oomlout_oomp_utility_readme_generation for folder: {folder}")
    #create_recursive(**kwargs)
    generate_navigation(**kwargs)


def generate_navigation(**kwargs):
    folder = kwargs.get("folder", os.getcwd())
    folder = folder.replace("parts",folder_navigation)
    directory_navigation = folder
    #get all the directories recurively using glob
    directory_list = glob.glob(f"{folder}/**/", recursive=True)
    
    # Create a dictionary to store categories and their corresponding items
    for directory in directory_list:        
        if not directory.endswith("part"):
            current_directory_list = glob.glob(f"{directory}/**/", recursive=True)
            file_readme = os.path.join(directory, "readme.md")
            
            # for each directory in the list
            current_directory_list_new = []
            for item in current_directory_list:
                item = item.replace("\\","/")
                directory_navigation_sanitized = directory_navigation.replace("\\","/")
                item = item.replace(directory_navigation_sanitized,"")
                if item.endswith("part/"):
                    #remove leading /
                    item = item[1:]
                    current_directory_list_new.append(item)
            current_directory_list = current_directory_list_new

            if len(current_directory_list) < 1000:

                # split the glob into a nice dict of the data
                file_paths = current_directory_list
                directory_dict = {}
                for file_path in file_paths:
                    #print(file_path)                
                    file_path_split = file_path.split("/")
                    file_path_split = file_path_split[:-2]
                    current_dict = directory_dict
                    for item in file_path_split:
                        if item not in current_dict:
                            current_dict[item] = {}
                        current_dict = current_dict[item]
                
                markdown_content = ""
                #display the directory_dict in a nested list            
                for key, value in directory_dict.items():
                    current_link = f"{key}"
                    markdown_content += f"* {key}\n"
                    for key2, value2 in value.items():
                        current_link += f"/{key2}"
                        markdown_content += f"  * {key2}\n"
                        for key3, value3 in value2.items():
                            current_link += f"/{key3}"
                            markdown_content += f"    * [{key3}]({current_link})\n"
                            for key4, value4 in value3.items():
                                current_link += f"/{key4}"
                                markdown_content += f"      * [{key4}]({current_link})\n"
                                for key5, value5 in value4.items():
                                    current_link += f"/{key5}"
                                    markdown_content += f"        * [{key5}]({key5})\n"
                                    for key6, value6 in value5.items():
                                        markdown_content += f"          * [{key6}]({key6})\n"
                                        for key7, value7 in value6.items():
                                            markdown_content += f"            * [{key7}]({key7})\n"
                                            for key8, value8 in value7.items():
                                                markdown_content += f"              * [{key8}]({key8})\n"
                                                for key9, value9 in value8.items():
                                                    markdown_content += f"                * [{key9}]({key9})\n"
                                                    for key10, value10 in value9.items():
                                                        markdown_content += f"                  * [{key10}]({key10})\n"
                                                    
                #write the markdown content to the readme
                with open(file_readme, "w") as f:
                    f.write(markdown_content)
                

            

def create_recursive(**kwargs):
    folder = kwargs.get("folder", os.path.dirname(__file__))
    kwargs["folder"] = folder
    folder_template_absolute = kwargs.get("folder_template_absolute", "")
    kwargs["folder_template_absolute"] = folder_template_absolute
    for item in os.listdir(folder):
        item_absolute = os.path.join(folder, item)
        if os.path.isdir(item_absolute):
            #if working.yaml exists in the folder
            if os.path.exists(os.path.join(item_absolute, "working.yaml")):
                kwargs["directory"] = item_absolute
                create(**kwargs)

def create(**kwargs):
    directory = kwargs.get("directory", os.getcwd())    
    kwargs["directory"] = directory
    file_template_list = kwargs.get("file_template_list", configuration)
    kwargs["file_template_list"] = file_template_list
    generate(**kwargs)
    

def generate(**kwargs):
    directory = kwargs.get("directory", os.getcwd())
    folder = kwargs.get("folder", os.getcwd())
    yaml_file = os.path.join(directory, "working.yaml")
    kwargs["yaml_file"] = yaml_file
    #load the yaml file
    with open(yaml_file, 'r') as stream:
        try:
            details = yaml.load(stream, Loader=yaml.FullLoader)
        except yaml.YAMLError as exc:   
            print(exc)

    folder_name = ""
    folder_order = ["classification", "type", "color","description_main", "description_extra", "manufacturer","part_number"]
    for item in folder_order:
        if item in details:   
            if details[item] != "":         
                folder_name += f"/{details[item]}"
    folder_name += f"/part"
    folder_no_parts = folder.replace("/parts",f"/{folder_navigation}")
    folder_name = f"{folder_no_parts}{folder_name}"

    directory_source = directory
    directory_destination = folder_name

    #copy the folder and create neccesary directories using xcopy for windows with overwite and cp for linux
    if os.name == "nt":
        command = f"xcopy \"{directory_source}\" \"{directory_destination}\" /e /i /y"
    else:
        command = f"cp -r \"{directory_source}\" \"{directory_destination}\""
    os.system(command)
    



if __name__ == '__main__':
    #folder is the path it was launched from
    
    kwargs = {}
    folder = os.path.dirname(__file__)
    #folder = "C:/gh/oomlout_oomp_builder/parts"
    folder = "C:/gh/oomlout_oomp_part_generation_version_1/parts"
    kwargs["folder"] = folder
    overwrite = False
    kwargs["overwrite"] = overwrite
    main(**kwargs)