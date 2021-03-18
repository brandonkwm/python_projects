import os

while True:
    try:
        log_folder_to_scan = input('Enter log folder name: ')
        stringToMatch = input('Enter string to search: ')
        preceding_lines_to_capture = input('Enter # of preceding lines (keep to 4 or 5): ')
        os.walk(os.path.join(os.getcwd(),log_folder_to_scan))
        break
    except FileNotFoundError:
         print('That folder does not exist in the current directory '+os.getcwd()+'\nPlease try again')
         
#extract all Execution timings and sort by descending order
linefile = 'line_output.txt'
summaryfile = 'line_summary_output.txt'
try:
    os.remove(linefile)
except FileNotFoundError:
    print('...creating '+linefile)

try:
    os.remove(summaryfile)
except FileNotFoundError:
    print('...creating '+summaryfile)


for root, dirs, files in os.walk(os.path.join(os.getcwd(),log_folder_to_scan)):
    for log_file in files:
        with open(os.path.join(os.getcwd(),log_folder_to_scan,log_file),'r') as log_fileOpen:
            lines = log_fileOpen.readlines()
            for index,line in enumerate(lines):
                if stringToMatch in line:
                    if line[22:27] != '00:00': #execution takes less than 1 min, ignore
                        query = ("".join(lines[max(0, index - int(preceding_lines_to_capture)):index + 1])) #output preceding 5 lines... value can be changed due to large queries...
                        with open(linefile,'a+') as linefileOpen:
                            linefileOpen.write(query +'\n')
                        with open(summaryfile,'a+') as summaryfileOpen:
                            summaryfileOpen.write(line.strip() + '| line number: '  + str(index+1) + '| file name: ' + log_file +'\n')
                    else:
                        continue

print('...done processing on: ' + os.path.join(os.getcwd(),log_folder_to_scan))
print('...output file: ' + linefile)
print('...summary file: ' + summaryfile)