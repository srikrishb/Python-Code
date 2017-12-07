import os

if __name__ == '__main__':

    dir = 'K:\Git Code\Python\Role Fix'
    searchStr = 'Data Steward'
    newStr = 'MS: Data Steward'

    for file in os.listdir(dir):
        if file.endswith('.bpmn'):

            print('File : ', file)

            # Open the old file
            oldFile = open(file,'r')

            # Open a new file
            newFile = open(os.path.splitext(file)[0]+'_new.bpmn','w')

            # Setup counter
            rowNum=0

            # Read lines in old file and replace the searchStr with newStr
            for line in oldFile:
                if searchStr in line:
                    print('Replacement found in line', rowNum, ': ', line.strip() )
                rowNum +=1
                newFile.write(line.replace(searchStr,newStr))

            # Close the file objects
            oldFile.close()
            newFile.close()
            print('\n')




