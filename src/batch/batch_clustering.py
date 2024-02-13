#TODO modelからではなく、service層からのみ行えるように
import sys
sys.path.append("D:\OneDrive - 筑波大学\自主制作\特許探索アプリ\SearchPatentAI")
from model import KeywordManager
from service import ClusteringAdmin
import numpy as np
import time

#階層的クラスタリングは現在、時間計算量O(N^2)、空間計算量O(N^2)であり、スケーリングが困難
kmanager=KeywordManager()
cadmin=ClusteringAdmin()
print("Batch[クラスタリング] Start")
start_time=time.perf_counter()
keyword_list,embed_list=kmanager.extractAllKeywordForClustering(50000)
embed_list=np.array(embed_list)
linkage,distance_t,result=cadmin.executeACluster(embed_list)
end_time=time.perf_counter()
print("クラスタリング終了",f"処理時間:{format(end_time-start_time,'.4f')}秒",sep="\n")
for i in range(len(keyword_list)):
    kmanager.insertGroupNum(keyword_list[i],result[i])
cadmin.plotGroup('a_cluster',keyword_list,result,linkage="average",threshold="1.0")