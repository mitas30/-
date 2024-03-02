#embedされたkeywordをpineconeに格納するbatch処理
import sys
sys.path.append("D:\OneDrive - 筑波大学\自主制作\特許探索アプリ\SearchPatentAI")
from model import PineConeAdmin,KeywordManager
import time

pc=PineConeAdmin()
keymanager=KeywordManager()

print("batch[Pineconeへのembed挿入]開始")
start_time=time.perf_counter()
key_attr_list=keymanager.provideAllKeywordAsDictNotInPineCone()
print(len(key_attr_list))
#POINT: Pineconeは、asciiしか対応していないので、str(_id)を格納する
batch_lists = [key_attr_list[i:i + 100] for i in range(0, len(key_attr_list), 100)]
for batch_list in batch_lists:
    pc.upsertSomeTargetEmbed(batch_list)
    keymanager.addCheckToKeywords(batch_list)
pc.knowDbInfo()
end_time=time.perf_counter()
print("batch[Pineconeへのembed挿入]完了",f"処理時間:{format(end_time-start_time,'.4f')}秒",sep="\n")