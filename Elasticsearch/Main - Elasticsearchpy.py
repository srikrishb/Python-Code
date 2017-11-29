import csv
import sys
from elasticsearch import Elasticsearch

if __name__ == '__main__':


    # Connect to Elasticsearch on localhost
    es = Elasticsearch([
        {'host': 'localhost', 'port':9200}
    ])

    # Create an index
    es.indices.create(index="bulktest", ignore=400)

    # Find the CSV file to be inserted
    paramFileName = sys.argv[1]

    # Temporary variable to store row count
    totalRowCount = 0

    dataLine = {}
    #os.chdir("K:\Git Code\Python\ParameterFiles")
    with open(paramFileName) as dataFile:
        row = csv.DictReader(dataFile)
        for line in row:
            for map in line:
                if map != '':
                     dataLine[map] = line[map]

            es.index(index="bulktest", doc_type="bulktype", body=dataLine, id=dataLine['id'])
            totalRowCount += 1

    # Loop through the index to print sample data
    for rowIndex in range(totalRowCount):

         response = es.get(index="bulktest", doc_type="bulktype", _source = "true", id=rowIndex)
         print(response['_source']['id']+' '+response['_source']['country']+' '+response['_source']['designation'])
