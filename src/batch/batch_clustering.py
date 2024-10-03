import os, sys

# path.dirnameは、このファイルのディレクトリ名。ターミナルで、どこから呼び出したとかは関係ない
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from model import KeywordManager
from service import ClusteringAdmin
import numpy as np
import time

# 階層的クラスタリングは現在、時間計算量O(N^2)、空間計算量O(N^2)であり、スケーリングが困難
kmanager = KeywordManager()
cadmin = ClusteringAdmin()
print("Batch[クラスタリング] Start")
start_time = time.perf_counter()
keyword_list, embed_list = kmanager.extractAllKeywordForClustering(1000)
clustering_method = "a_cluster"
embed_list = np.array(embed_list)
linkage, distance_t, result = cadmin.executeACluster(embed_list)
cadmin.visualizeEmbedding(clustering_method, embed_list, result)
end_time = time.perf_counter()
print("クラスタリング終了", f"処理時間:{format(end_time-start_time,'.4f')}秒", sep="\n")
for i in range(len(keyword_list)):
    kmanager.insertGroupNum(keyword_list[i], result[i])
cadmin.plotGroup(
    clustering_method, keyword_list, result, linkage="average", threshold="1.0"
)
