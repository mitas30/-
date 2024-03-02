#keywordをembedしてデータ保存する スレッドでの並行処理を行って高速化する
import sys
sys.path.append("D:\OneDrive - 筑波大学\自主制作\特許探索アプリ\SearchPatentAI")
from service import Embedder
from model import KeywordManager
from concurrent.futures import ThreadPoolExecutor

def processKeyword(keyword:str):
    embed_list=embedder.embedKeyword(keyword)
    keywordmanager.insertEmbedOfOnePatentIntoMongo(keyword,embed_list)

#keywordをembedding化して、もう一度mongoに保存する処理
keywordmanager=KeywordManager()
embedder=Embedder()

cursor=keywordmanager.extractAllKeywordNotEmbed(15000)
print("embedding Start")
#API呼び出しなので、スレッド単位の並行処理
with ThreadPoolExecutor(max_workers=5) as executor:
    for keyword_docs in cursor:
        keyword = keyword_docs.get('keyword')
        executor.submit(processKeyword, keyword)
print("embedding End")
