from openpyxl import load_workbook
import redis

class ProcessMetrics:

    def __init__(self, inputFileName):
        self.inputFileName = inputFileName

    def generateMetricsFile(self):
        # Open the data file
        workbook = load_workbook(self.inputFileName)
        defaultSheet = workbook.active

        # Kick start redis
        redis_db = redis.StrictRedis(host="127.0.0.1", port=6379, db=0)
        redis_db.flushall()
        i = 0
        key = ''
        offset = 2
        prev_assettype = ''
        curr_assettype = ''
        prev_offset = 2
        currAssetName = ''
        prevAssetName = ''
        keyList = []
        for row in defaultSheet.rows:
            if i == 0:
                i += 1
                for cellInRow in row:
                    if cellInRow.value == 'AssetType':
                        marker = cellInRow.col_idx
                        # xy = coordinate_from_string(cell)  # returns ('A',4)
                        # marker = column_index_from_string(xy[0])  # returns 1
                        print('marker', marker)
            else:
                for cellInRow in row:
                    if cellInRow.col_idx == 1:
                        currAssetName = cellInRow.value
                    if cellInRow.col_idx > 1 and cellInRow.col_idx < marker:
                        if cellInRow.col_idx == 2:
                            key = cellInRow.value
                        else:
                            key = key + ":" + cellInRow.value
                    if cellInRow.col_idx == marker:
                        key = key + ":" + cellInRow.value
                        curr_assettype = cellInRow.value
                        if prev_assettype == curr_assettype:
                            if prevAssetName == currAssetName:
                                offset = prev_offset
                            else:
                                offset += 1
                                prevAssetName = currAssetName
                                prev_offset = offset
                        else:
                            if prevAssetName != currAssetName:
                                offset = 2
                                prev_offset = offset
                                prev_assettype = curr_assettype
                                prevAssetName = currAssetName
                print(key, offset - 1, 1)
                keyList.append(key)

                # see what keys are in Redis

                redis_db.setbit(key, offset - 1, 1)
                key = ''

        for key in keyList:
            print(key, redis_db.bitcount(key))