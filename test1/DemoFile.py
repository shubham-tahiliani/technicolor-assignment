import re
from os import listdir, getcwd
import sys
from os.path import isfile, join

def extractFiles():
    if len(sys.argv) > 1:
        try:
            mypath = str(sys.argv[1])                     
            files = [fil for fil in listdir(mypath) if isfile(join(mypath, fil))]
            if not files:
                print("No files in the directory.")
            else:
                createExtensions(files)
        except OSError as e:
            print("Invalid path!")            
    else:
        mypath = getcwd()
        # extracting the item into a list if the item is a file
        files = [fil for fil in listdir(mypath) if isfile(join(mypath, fil))]    
        # checking if the files list is empty
        if not files:
            print("No files in the directory.")
        else:
            createExtensions(files)

def createExtensions(files):
    ext = []
    
    # file extension will be everthing after the last period in the string
    for i in files:
        # traversing the string from the end
        j=len(i)-1
        name = ""
        while(j>0):
            if(i[j]=="."):
                name = i[j]+name
                break
            else:
                name = i[j]+name
                j = j-1
        ext.append(name)
    file_extensions = {
        i: []
        for i in set(ext)
    }
    for i in range(len(ext)):
        file_extensions[ext[i]].append(files[i])

    for extension in file_extensions:
        extractNum(file_extensions, extension)

def extractNum(file_extensions, extension):
    result_list = []
    name_list = []
        
    for files in file_extensions[extension]:
        num_list=[]
        name = ""
        start = 0
        for num in re.finditer(r"\d+",files):
            num_len = num.end() - num.start()
            num_list.append([num.group(0), num_len, num.start(), num.end()])
            last = num.start()
            name = name + files[start:last] + "*"*num_len 
            start = num.end()
        name = name + files[start:]
        if name == "":
            name_list.append(files)
        else:
            name_list.append(name)
        result_list.append(num_list)
    
    checkMatch(result_list, name_list, file_extensions, extension)

def checkMatch(result_list, name_list, file_extensions, keys):
    result_dict = {}
    tracking = [0] * len(result_list)

    # comparing the elements in the result_list in pairs of two.
    for i in range(len(result_list)-1):
        isEqual = False
        curr = result_list[i]
        after = result_list[i+1]
        if((len(curr)>0 and len(after)>0) and (len(curr)==len(after)) and (name_list[i] == name_list[i+1])):
            for j in range(len(curr)):
                check = [int(a)-int(b) for a,b in zip(after[j],curr[j])]
                if ((len(curr)>1) and set(check)=={0}):
                    isEqual = True
                    filename = fileName(curr[j][2], curr[j][0], curr[j][3], name_list[i])
                    if(filename not in result_dict):
                        result_dict[filename] = []
                elif (len(curr)==1):
                    isEqual = True
                    filename = zero_padding(name_list[i].count("*"), name_list[i])
                    if(filename not in result_dict):
                        result_dict[filename] = []
                    start = int(curr[j][0])
                    end = int(after[j][0])
                else:
                    start = int(curr[j][0])
                    end = int(after[j][0])

            if(isEqual):
                tracking[i] = 1
                tracking[i+1] = 1
                result_dict[filename].append(start)
                result_dict[filename].append(end)
           
    checkTracking(file_extensions, keys, tracking, result_dict)

def checkTracking(file_extensions, keys, tracking, result_dict):
    for k in range(len(tracking)):
        if tracking[k] == 0:
            result_dict[file_extensions[keys][k]] = file_extensions[keys][k]
            
    compactNumform(result_dict)

def fileName(num_start, num, num_end, name_list):
    length = num_end - num_start
    filename = name_list[:num_start] + name_list[num_start:num_end].replace("*"*length,num) + name_list[num_end:]
    return zero_padding(filename.count("*"), filename)

def zero_padding(frequency, filename):
    if frequency > 2:
        filename = filename.replace("*"*frequency, "%0"+str(frequency)+"d")
    else:
        filename = filename.replace("*"*frequency, "%d")    
    return filename

def compactNumform(result_dict):
    count = {}
    
    for key in result_dict:
        if key != result_dict[key]:
            result_dict[key] = list(set(result_dict[key]))
            ranges = []
            for t in zip(result_dict[key], result_dict[key][1:]):
                if (t[0]+1 != t[1]):
                    ranges.append(t[0])
                    ranges.append(t[1])
            iranges = iter(result_dict[key][0:1] + ranges + result_dict[key][-1:])
            count[key] = len(set(result_dict[key]))
            result_dict[key] = (', '.join([str(n) + '-' + str(next(iranges)) for n in iranges]))
        else:
            count[key] = 1
    finalPrint(result_dict, count)

def finalPrint(result_dict, count):
    for key in result_dict:
        if count[key] > 1:
            print(str(count[key]) + " " + key + "       " + result_dict[key])
        else:
            print(str(count[key]) + " " + key)

def main():
    extractFiles()

if __name__ == "__main__":
   
   main()
