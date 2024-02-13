#TODO modelからではなく、service層からのみ行えるように
#特許データをmongoDBに格納する
import sys
sys.path.append("D:\OneDrive - 筑波大学\自主制作\特許探索アプリ\SearchPatentAI")
from model import DBIngestor

#ダウンロードファイルからPDFを取り出して、JSONに格納する
test=DBIngestor()
test.movingAllFile()
test.batchExtractPatentDatas()