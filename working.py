import os
import yaml
import glob
import copy
import jinja2    
import shutil
import pickle
from pygments.formatters import HtmlFormatter
import markdown


folder_configuration = "configuration"
folder_configuration = os.path.join(os.path.dirname(__file__), folder_configuration)

folder_navigation = "navigation_oomp"

cnt_navigation = 1

file_configuration = os.path.join(folder_configuration, "configuration.yaml")
file_configuration = file_configuration.replace("\\","/")
#if configuration file doesn't exist use configuration_default.yaml
if not os.path.exists(file_configuration):
    file_configuration = os.path.join(folder_configuration, "configuration_default.yaml")
    file_configuration = file_configuration.replace("\\","/")
    print(f"using default configuration file: {file_configuration}")
#import templates
with open(file_configuration, 'r') as stream:
    try:
        configuration = yaml.load(stream, Loader=yaml.FullLoader)
    except yaml.YAMLError as exc:   
        print(exc)



def main(**kwargs):

        
    
    folder = kwargs.get("folder", f"{os.path.dirname(__file__)}/parts")
    folder = folder.replace("\\","/")
    
    filt = kwargs.get("filter", "")

    kwargs["file_template_list"] = configuration

    print(f"oomlout_oomp_utility_navigation_generation for folder: {folder}")

    #if no filter is provided, set it to empty string
    #if filt == "":
    if True:
        create_recursive(**kwargs)
        generate_navigation(**kwargs)
    else:
        print(f"******  skipping because a filter is present  ******")


def generate_navigation(**kwargs):
    folder = kwargs.get("folder", os.getcwd())
    folder = folder.replace("parts",folder_navigation)
    folder = folder.replace("things",folder_navigation)
    directory_navigation = folder
    #get all the directories recurively using glob
    directory_list = glob.glob(f"{folder}/**/", recursive=True)
    
    # Create a dictionary to store categories and their corresponding items
    for directory in directory_list:    
        #if starts with a / remove it
        if directory.startswith("/"):
            directory = directory[1:]
        directory = directory.replace("\\","/") 
        directory_short = directory.replace(folder,"")  
        if directory_short.startswith("/"):
            directory_short = directory_short[1:] 
        if not directory.endswith("part/"):
            current_directory_list = glob.glob(f"{directory}/**/", recursive=True)
            file_readme = os.path.join(directory, "readme.md")
            file_html = os.path.join(directory, "index.html")
            
            
            # for each directory in the list
            current_directory_list_new = []
            for item in current_directory_list:
                item = item.replace("\\","/")
                directory_navigation_sanitized = directory_navigation.replace("\\","/")
                item = item.replace(directory_navigation_sanitized,"")
                if item.endswith("part/"):
                    #remove leading /
                    if item.startswith("/"):
                        item = item[1:]
                    current_directory_list_new.append(item)
            current_directory_list = current_directory_list_new

            if len(current_directory_list) < 6000:

                # split the glob into a nice dict of the data
                file_paths = current_directory_list
                directory_dict = {}
                for file_path in file_paths:
                    #print(file_path)   
                    file_path = file_path.replace("\\","/")
                    file_path = file_path.replace(directory_short,"")             
                    file_path_split = file_path.split("/")
                    file_path_split = file_path_split[:-2]
                    current_dict = directory_dict
                    for item in file_path_split:
                        if item not in current_dict:
                            current_dict[item] = {}
                        current_dict = current_dict[item]
                
                markdown_content = ""
                markdown_content = generate_markdown(directory_dict)
                pass
                """
                #display the directory_dict in a nested list            
                for key, value in directory_dict.items():
                    current_link = f"{key}"
                    markdown_content += f"* [{key}]({current_link})\n"
                    for key2, value2 in value.items():
                        current_link += f"/{key2}"
                        markdown_content += f"  * [{key2}]({current_link})\n"
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
                 """                                   
                #write the markdown content to the readme
                if markdown_content != "":
                    with open(file_readme, "w") as f:
                        #print(f"writing {file_readme}")
                        f.write(markdown_content)
                #write the html content to the index.html
                import markdown
                #html_content = markdown.markdown(markdown_content)
                html_content = md_to_pretty_html(markdown_content, title=f"{item} - OOMLout Part")
                if html_content != "":
                    with open(file_html, "w") as f:
                        #print(f"writing {file_html}")
                        f.write(html_content)
                
def generate_markdown(directory_dict, current_link='', indent=0):
    markdown_content = ''
    for key, value in directory_dict.items():
        if current_link != '':
            key_sanitized = key
            if key_sanitized.startswith("/"):
                key_sanitized = key_sanitized[1:]
            current_link_sanitized = current_link
            if current_link_sanitized.startswith("/"):
                current_link_sanitized = current_link_sanitized[1:]
            markdown_content += '  ' * indent + f'* [{key}]({current_link_sanitized}/{key})\n'
        else:
            key_sanitized = key
            if key_sanitized.startswith("/"):
                key_sanitized = key_sanitized[1:]
            markdown_content += '  ' * indent + f'* [{key_sanitized}]({key_sanitized})\n'
        if isinstance(value, dict):
            current_link_sanitized = current_link
            if current_link_sanitized.startswith("/"):
                current_link_sanitized = current_link_sanitized[1:]                
            markdown_content += generate_markdown(value, f'{current_link_sanitized}/{key}', indent + 1)
    
    return markdown_content

def generate_markdown_working_well(directory_dict, current_link='', indent=0):
    markdown_content = ''
    for key, value in directory_dict.items():
        if current_link != '':
            markdown_content += '  ' * indent + f'* [{key}]({current_link}/{key})\n'
        else:
            markdown_content += '  ' * indent + f'* [{key}]({key})\n'
        if isinstance(value, dict):
            current_link_sanitized = current_link
            if current_link_sanitized.startswith("/"):
                current_link_sanitized = current_link_sanitized[1:]                
            markdown_content += generate_markdown(value, f'{current_link_sanitized}/{key}', indent + 1)
    
    return markdown_content



counter = 1      

def create_recursive(**kwargs):
    folder = kwargs.get("folder", os.path.dirname(__file__))
    kwargs["folder"] = folder
    filter = kwargs.get("filter", "")
    kwargs["filter"] = filter
    
    
    import threading
    semaphore = threading.Semaphore(1000)
    threads = []

    print("******  creating copy command list  ******")
    def create_thread(item, commands, **kwargs):
        global counter
        with semaphore:
            command = create_recursive_thread(item,**kwargs)
            if command != None:
                commands.append(command)
                counter += 1
                if counter % 100 == 0:
                    print(".", end="", flush=True)
    
    from functools import partial

    commands = []
    counter = 1
    for item in os.listdir(folder):
        #kwargs["item"] = copy.deepcopy(item)
        #thread = threading.Thread(target=create_thread, kwargs=copy.deepcopy(kwargs))
        #thread = threading.Thread(target=create_thread, kwargs))
        #create thread sent item and kwargs sperately
        thread = threading.Thread(target=partial(create_thread, item=item, commands=commands,**kwargs))
        threads.append(thread)
        thread.start()
    print()

    #wait for threads to finish
    for thread in threads:
        thread.join()    
    
    print("******  copying across  ******")
    counter = 1
    for command in commands:
        #run as os.system don't print output to terminal        
        mode = "subprocess"
        if mode == "os":
            os.system(command)
        elif mode == "subprocess":
            import subprocess
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"Error: {result.stderr}")
            else:
                pass
                #print(f"Output: {result.stdout}")
        counter += 1
        if counter % 100 == 0:
            print(".", end="", flush=True)
    print()
    pass

    
    



def create_recursive_thread(item, **kwargs):
    #item = kwargs.get("item", "")
    filter = kwargs.get("filter", "")
    folder = kwargs.get("folder")
    #if filter in item: #don't use filter for navigation
    if True:
        item_absolute = os.path.join(folder, item)
        item_absolute = item_absolute.replace("\\","/")
        if os.path.isdir(item_absolute):
            #if working.yaml exists in the folder
            if os.path.exists(os.path.join(item_absolute, "working.yaml")):
                directory = item_absolute
                return create(item, directory, **kwargs)



def create(item, directory, **kwargs):
    #directory = kwargs.get("directory", os.getcwd())    
    #kwargs["directory"] = directory
    file_template_list = kwargs.get("file_template_list", configuration)

    #kwargs["file_template_list"] = file_template_list
    return generate(item, directory, **kwargs)
    

def generate(item, directory, **kwargs):
    #directory = kwargs.get("directory", os.getcwd())
    folder = kwargs.get("folder", os.getcwd())

    yaml_file = os.path.join(directory, "working.yaml")
    kwargs["yaml_file"] = yaml_file
    #load the yaml file
    with open(yaml_file, 'r') as stream:
        details = None
        try:
            details = yaml.load(stream, Loader=yaml.FullLoader)
        except yaml.YAMLError as exc:   
            print(exc)

    if details != None:

        folder_name = ""
        folder_order = ["classification", "type", "size", "color","description_main", "description_extra", "manufacturer","part_number"]
        for item in folder_order:
            if item in details:   
                if details[item] != "":         
                    folder_name += f"/{details[item]}"
        folder_name += f"/part"
        folder_no_parts = folder.replace("parts",f"{folder_navigation}")
        folder_no_parts = folder_no_parts.replace("things",f"{folder_navigation}")
        folder_name = f"{folder_no_parts}{folder_name}"

        directory_source = directory
        directory_destination = folder_name

        #copy the folder and create neccesary directories using xcopy for windows with overwite and cp for linux
        if os.name == "nt":
            if True:
                command = f"xcopy \"{directory_source}\" \"{directory_destination}\" /e /i /y"
                #os.system(command)
                return command
            else:
                shutil.copytree(directory_source, directory_destination, dirs_exist_ok=True)
        else:
            command = f"cp -r \"{directory_source}\" \"{directory_destination}\""
            os.system(command)
        
        return command
        

    else:
        print(f"no yaml file found in {directory}")    

def md_to_pretty_html(md_text: str, title="My Page") -> str:
    exts = [
        "extra",          # tables, fenced code, footnotes, attr_list, etc.
        "toc",            # heading anchors + optional [TOC]
        "admonition",     # !!! note style callouts
        "codehilite",     # pygments syntax highlighting
    ]
    html_body = markdown.markdown(
        md_text,
        extensions=exts,
        extension_configs={
            "toc": {"permalink": "¶"},
            "codehilite": {"guess_lang": False, "pygments_style": "friendly"},
        },
    )
    pyg_css = HtmlFormatter(style="friendly").get_style_defs(".codehilite")

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<!-- Classless CSS = modern look without touching your HTML -->
<link rel="stylesheet" href="https://unpkg.com/@picocss/pico@latest/css/pico.classless.min.css">
<style>
{pyg_css}
/* small niceties */
main{{max-width:72ch;margin:auto;padding:2rem 1rem}}
pre{{overflow-x:auto}}
img{{max-width:100%;height:auto}}
.admonition{{border-left:4px solid rgba(0,0,0,.15);padding:.75rem 1rem;margin:1rem 0;background:rgba(0,0,0,.03);border-radius:.5rem}}
.admonition > .admonition-title{{font-weight:600;margin-bottom:.25rem}}
</style>
</head>
<body>
<main>
{html_body}
</main>
</body>
</html>"""

if __name__ == '__main__':
    #folder is the path it was launched from
    
    kwargs = {}
    folder = os.path.dirname(__file__)
    #folder = "C:/gh/oomlout_oomp_builder/parts"
    folder = "C:/gh/oomlout_oomp_part_generation_version_1/parts"
    #folder = "C:/gh/oomlout_oobb_version_4/things"
    kwargs["folder"] = folder
    overwrite = False
    kwargs["overwrite"] = overwrite
    main(**kwargs)