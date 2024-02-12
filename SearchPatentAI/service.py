import os,google.generativeai as genai
from openai import OpenAI
import requests,time,fastcluster,numpy as np,matplotlib.pyplot as plt
from typing import List,Union,Tuple
from numpy import ndarray
from model import KeywordManager,PineConeAdmin,PatentsAdmin,PatentOfficeAdmin
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE 
from scipy.cluster.hierarchy import fcluster
from matplotlib.colors import ListedColormap

class LLMManipulator():
    """LLMのAPI関連を行うクラス"""

    def __init__(self):
        GOOGLE_API_KEY=os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=GOOGLE_API_KEY)
        genai.GenerationConfig(candidate_count=1)
    
    def extractKeywordFromSentence(self,name_of_invention:str,tech_field:str,way_to_solve_problems:str,effect_of_invention:str,detail_assignment:str)->Union[str,int]:
        model = genai.GenerativeModel('gemini-pro')
        user_content1="""あなたは、たくさんの技術を知っていて、アイデアを聞くとそれを端的に表すために必要な単語を思いつくことができます。以下の指示に従ってください。
    特許とその詳細が<patent>にかかれています。
    その内容から、その特許を10個のキーワードで端的に表してください。ただし、キーワードは、重要なものから順に出力してください。
    つまり、人々がその10個のキーワードを見たときに、特許の内容を理解できるような10個で構成してください。
    また、回答は<format>の形式で、キーワードのみ列挙する形で答えてください。

    <format>
    [keyword1,keyword2,keyword3,....,keyword10]

    <patent>
    発明の名称:カテーテル及び脳梗塞治療デバイス
    
    技術分野:
    本発明は、脊椎から挿入されて高酸素溶液を注入および排出するカテーテル及び脳梗塞治療デバイスに関する。

    解決する問題:
    上記目的を達成する本発明に係るカテーテル及び脳梗塞治療デバイスは、生体内に挿入される管本体を有するカテーテルであって、前記管本体は、先端部に設けられる透過部と、基端側から前記透過部に向かって流体を流動させる注入ルーメンと、前記透過部から基端側に向かって流体を流動させる排出ルーメンと、を有し、前記透過部は、前記流体に含まれる特定の気体を前記管本体の外部に透過させる透過膜部を有する。
    
    発明の効果:
    上記のように構成したカテーテル及び脳梗塞治療デバイスは、液体を管本体の外部に流出させることなく、特定の気体を放出できるので、頭蓋内圧を変動させないようにすることができる。\n前記注入ルーメンと前記排出ルーメンは前記透過部内で互いに連通すると共に、並列配置されるようにしてもよい。これにより、流体を、管本体内の外部に流出させることなく流動させることができる。\n前記注入ルーメンと前記排出ルーメンは同心状に配置されるようにしてもよい。これにより、管本体の径を小さくすることができる。\n前記管本体は、前記注入ルーメンおよび前記排出ルーメンと連通する貯留部を先端部に有するようにしてもよい。これにより、貯留部に流体が留まりやすいので、透過部から効率的に特定の気体を放出できる。\n前記排出ルーメンは、前記注入ルーメンの内側に同心状に配置されると共に、前記注入ルーメンと連通する連通部を先端より基端側に有するようにしてもよい。これにより、流体が管本体の先端部に留まりやすいので、透過部から効率的に特定の気体を放出できる。\n前記注入ルーメンの先端部には、前記透過膜部で形成されたバルーンが設けられ、前記バルーンは、前記注入ルーメンから流体が注入されることで径方向に拡張するようにしてもよい。これにより、流体がバルーン内に留まりやすく、また、径方向に拡張したバルーンは表面積が大きくなるため、より効率的に特定の気体を放出することができる。\n前記管本体は、先端部に造影マーカーを有するようにしてもよい。これにより、管本体を生体内に挿入する際に、先端部を目的部位へ確実に送達することができる。
    
    解決手段:
    特許文献１には、高酸素溶液を脳にアプローチする治療のための具体的な医療デバイスについては開示されていない。この治療のためには、医療デバイスは、脳に対して高酸素溶液を注入すると共に、髄液を排出する機能を有する必要がある。しかし、医療デバイスが流体の注入と排出をバランスよく行うことができないと、頭蓋内圧が変動するリスクを生じる。\n本発明は、上述した課題を解決するためになされたものであり、頭蓋内圧の変動を生じることなく安全に脳に酸素を送ることのできるカテーテル及び脳梗塞治療デバイスを提供することを目的とする。
    """
        model_answer1="[カテーテル,脳梗塞治療,流体注入排出,頭蓋内圧調整,高酸素溶液,透過膜部,同心状配置,貯留部,バルーン拡張,造影マーカー]"

        user_content2=f"""あなたは、たくさんの技術を知っていて、アイデアを聞くとそれを端的に表すために必要な単語を思いつくことができます。以下の指示に従ってください。
    特許とその詳細が<patent>にかかれています。
    その内容から、その特許を10個のキーワードで端的に表してください。ただし、キーワードは、重要なものから順に出力してください。
    つまり、人々がその10個のキーワードを見たときに、特許の内容を理解できるような10個で構成してください。
    また、回答は<format>の形式で、キーワードのみ列挙する形で答えてください。

    <format>
    [keyword1,keyword2,keyword3,...,keyword10]

    <patent>
    発明の名称:{name_of_invention}
    
    技術分野:
    {tech_field}

    解決する問題:
    {detail_assignment}

    発明の効果:
    {effect_of_invention}
    
    解決手段:
    {way_to_solve_problems}
    """
        try:
            response=model.generate_content(f"""user_content1:{user_content1}\nmodel_answer1:{model_answer1}\nuser_content2:{user_content2}""")
            return response.text
        except ValueError as e:
            print("エラーの発生",e)
            print("-"*80)
            return 0
    
    def extractKeywordFromUserIdea(self,idea_name:str,problem:str,abstract:str,use_tech:str,way_to_solve:str)->Union[List[str],int]:
        """ユーザが入力したアイデアから、それを端的に表すワード10個を取り出す。"""
        model = genai.GenerativeModel('gemini-pro')
        user_content1="""
    あなたは、たくさんの技術を知っていて、アイデアを聞くとそれを端的に表すために必要な単語を思いつくことができます。以下の指示に従ってください。
    アイデアとその詳細が<idea>にかかれています。
    その内容から、そのアイデアを10個のキーワードで端的に表してください。ただし、キーワードは、重要なものから順に出力してください。
    つまり、人々がその10個のキーワードを見たときに、特許の内容を理解できるような10個で構成してください。
    また、回答は<format>の形式で、キーワードのみ列挙する形で答えてください。
    
    <format>
    [keyword1,keyword2,keyword3,....,keyword10]

    <patent>
    発明の名称:クリーンエア・アーバンシールド
    解決する問題:都市部の大気汚染による健康リスクの軽減
    
    発明の概要:
    「クリーンエア・アーバンシールド」は、都市部の大気汚染問題に対応するために開発された画期的な発明です。このシステムは、建物の外壁や都市インフラに設置されることを想定しており、空気清浄技術を活用して周辺の大気を浄化します。具体的には、汚染物質を吸収し、フィルターを通してクリーンな空気を放出することで、都市部の空気質を改善します。
    このシステムは、特に交通量の多い地域や工業地域において有効であり、大気中の有害物質を削減することで、市民の健康リスクを軽減します。さらに、クリーンエア・アーバンシールドは、エネルギー効率の高い方法で運用され、環境への負荷も最小限に抑えられています。
    また、このシステムのデザインは、都市景観に溶け込むよう工夫されており、美観を損なうことなく都市部の空気質を改善することができます。究極の目標は、都市部の生活環境を改善し、すべての市民がクリーンで健康的な空気を呼吸できるようにすることです。

    使用する技術:
    高度なHEPAフィルター：これらのフィルターは、大気中の微小粒子物質（PM2.5やPM10など）を効率的に捕捉し、除去します。また、大気中の有害な化学物質やアレルゲンもフィルターする能力を持っています。
    活性炭フィルター：活性炭は、その高い吸着性能により、有害なガスや臭気を吸収するのに適しています。これにより、大気からNOxやSOxなどの有害な化学物質を除去することができます。
    光触媒コーティング：このコーティングは、太陽光や人工光源の下で活性化し、大気中の有害物質を無害な物質に分解します。この技術は、維持費が低く、自己清浄能力を持っているため、メンテナンスの手間を軽減します。
    エネルギー効率の良い設計：システムは省エネ設計に基づいており、必要最小限の電力で動作します。太陽光発電パネルなどの再生可能エネルギー源と組み合わせることで、その持続可能性をさらに高めることが可能です。
    スマートモニタリングシステム：大気の質をリアルタイムで監視し、汚染レベルに応じて清浄システムの動作を調整します。これにより、効率的かつ効果的に大気汚染を管理することができます。
    
    問題の解決手段:
    クリーンエア・アーバンシールドは、統合された空気清浄技術を使用して都市部の大気汚染問題を解決します。
    高度なHEPAフィルターは、PM2.5やPM10などの微細粒子物質を効果的に捕捉し、除去します。
    活性炭フィルターは、NOxやSOxなどの有害ガスを吸収します。
    光触媒コーティングは、太陽光の下で活性化し、有害物質を無害な物質に分解します。
    このシステムは、エネルギー効率の良い設計に基づいており、太陽光発電パネルと組み合わせることでさらに環境に優しいものとなります。
    スマートモニタリングシステムにより、大気の質をリアルタイムで監視し、汚染レベルに応じて清浄システムの動作を調整します。
    これらの技術を通じて、都市部の空気質を大幅に改善し、市民の健康リスクを軽減する効果を期待できます。
    """
        model_answer1="[大気汚染対策, HEPAフィルター, 活性炭フィルター, 光触媒コーティング, エネルギー効率, スマートモニタリング, 健康リスク軽減, 都市インフラ, 環境持続可能性, スマートシティ]"
        user_content2=f"""あなたは、たくさんの技術を知っていて、アイデアを聞くとそれを端的に表すために必要な単語を思いつくことができます。以下の指示に従ってください。
    アイデアとその詳細が<idea>にかかれています。
    その内容から、そのアイデアを10個のキーワードで端的に表してください。ただし、キーワードは、重要なものから順に出力してください。
    つまり、人々がその10個のキーワードを見たときに、特許の内容を理解できるような10個で構成してください。
    また、回答は<format>の形式で、キーワードのみ列挙する形で答えてください。
    
    <format>
    [keyword1,keyword2,keyword3,....,keyword10]

    <patent>
    発明の名称:{idea_name}
    解決する問題:{problem}\n
    発明の概要:\n{abstract}\n
    使用する技術:\n{use_tech}\n
    問題の解決手段:\n{way_to_solve}\n
    """
    
        try:
            #selfを使うならinstanceから関数を呼び出すこと
            manager=KeywordManager()
            response=model.generate_content(f"""user_content1:{user_content1}\nmodel_answer1:{model_answer1}\nuser_content2:{user_content2}""")
            keyword_list=manager.processKeywordsStrToList(response.text)
            return keyword_list
        except ValueError as e:
            print("エラーの発生",e)
            print("-"*80)
            return 0        
    
class Embedder:
    def __init__(self):
        self.client = OpenAI()
        
    def embedKeyword(self,keyword:str)->List[float]:
        """keyword(str)をベクトル化する"""
        response=self.client.embeddings.create(
            model="text-embedding-3-small",
            input=keyword,
            encoding_format="float"
        )
        return response.data[0].embedding

class ClusteringAdmin:
    """キーワードのクラスタリングに関する仕事を行う"""
    def __init__(self):
        pass
    
    #O(n^2)
    def executeACluster(self,embed_array:ndarray)->tuple[str,int,ndarray]:
        method="average"
        distance_threshold=1.0
        linkage_matrix=fastcluster.linkage(embed_array,method=method)
        #linkage_matrix=fastcluster.linkage_vector(embed_array,method=method)
        clusters = fcluster(linkage_matrix, t=distance_threshold, criterion='distance')
        clusters=clusters.tolist()
        return method,distance_threshold,clusters

    #1500次元の場合にはさすがに約に立たない?
    def visualizeEmbedding(self,method:str,embeddings: ndarray, labels: ndarray):
        # PCAを使用して最初に次元を削減
        pca = PCA(n_components=50)
        embeddings_reduced = pca.fit_transform(embeddings)
        print("complete pca")

        # t-SNEを使用してさらに次元削減（2次元）
        tsne = TSNE(n_components=2, random_state=0)
        embeddings_2d = tsne.fit_transform(embeddings_reduced)
        print("complete t-SNE")

        plt.figure(figsize=(10, 10))
        unique_labels = np.unique(labels)

        # クラスタごとに異なる色でプロットする
        colors = ListedColormap(np.random.rand(len(unique_labels), 3))

        for label in unique_labels:
            # クラスタに属するデータポイントを取得
            indices = np.where(labels == label)

            # labelが-1の場合は黒色、それ以外はランダムな色
            if label == -1:
                color = 'black'
            else:
                color = colors(label)

            plt.scatter(embeddings_2d[indices, 0], embeddings_2d[indices, 1], color=color, label=f'Cluster {label}')

        plt.title(f't-SNE visualization of {method} clustering')
        plt.xlabel('t-SNE Feature 1')
        plt.ylabel('t-SNE Feature 2')
        plt.legend(loc='best')
        plt.show()
        
    def plotGroup(self,method: str, keyword_list, cluster_result: ndarray, **kwargs):
        # kwargsを使用してファイル名の追加部分を作成
        extra_filename = '_'.join([f'{key}={value}' for key, value in kwargs.items()])
        # ファイル名を組み立て
        filename = f'../search_result/{method}/keyword={len(keyword_list)}_{extra_filename}'
        with open(filename, 'w', encoding='utf-8') as file:
            # クラスタリストとカウントの初期化
            class_list = {i: [] for i in set(cluster_result)}
            num_memo = {i: 0 for i in set(cluster_result)}

            # カテゴリごとにキーワードを分類し、カウントを行う
            for keyword, cluster in zip(keyword_list, cluster_result):
                class_list[cluster].append(keyword)
                num_memo[cluster] += 1

            # 無所属カテゴリのカウントを出力
            print("カテゴリ 無所属:", num_memo.get(-1, 0), file=file)
            print("カテゴリ クラスタ内:", len(cluster_result) - num_memo.get(-1, 0), file=file, end="")

            # 各カテゴリに属するキーワードの数とキーワードを表示
            for cluster_id, keywords in class_list.items():
                print("\n" + "-" * 80, file=file)
                print("カテゴリ", cluster_id, ":", num_memo[cluster_id], file=file)
                for i, keyword in enumerate(keywords):
                    if i % 50 == 49:
                        print(keyword, file=file)
                    else:
                        print(keyword, end=" ", file=file)

class FetchSearchResult:
    def __init__(self):
        pass
    
    def fetchAllKeywordInSameGroup(self,_id:str)->List[dict[int,str]]:
        kmanager=KeywordManager()
        count,kwards_list=kmanager.findAllKeywordInSameGroup(_id)
        ret_list=[]
        for kward in kwards_list:
            ret_list.append({"count":count,"keyword":kward})
        return ret_list
        
    def tellKwardInSameGroup(self,embeded_keyword:List[float])->str:
        "アイデアから抽出したkeywordと同じグループのkeyword_idを返す"
        #同じグループとみなすしきい値
        cos_threshold=0.60
        pcadimn=PineConeAdmin()
        response=pcadimn.findNearestKeyword(embeded_keyword)
        if response[0]["score"]<cos_threshold:
            print(f"似ているキーワードは存在しない。 cos_sim:{response[0]['score']}")
            return ""
        else:
            print(f"cos_sim:{response[0]['score']}")
            return response[0]["id"]
        
    def suggest10NearestPatents(self,all_keyword_list:List[dict[int,str]])->List[Tuple[str,Tuple[int,float]]]:
        """入力のkeywordリストから、キーワードが一致する特許を調べ、
        参照回数の多い上位10件(同じ参照回数ならスコア評価)のpriority_key,count,scoreを含んだTupleのListを返却する"""
        p_admin=PatentsAdmin()
        #priority_key(特許):str,(count:int,score:float)の辞書
        candidate_dict={}
        #step1 特許の集計
        for keyword_info in all_keyword_list:
            key_freq=keyword_info["count"]
            keyword_name=keyword_info["keyword"]
            cursor=p_admin.fetchPatentPKeysHaveCertainKeyword(keyword_name)
            for doc in cursor:
                p_key=doc['priority_key']
                #特許が既に存在する場合
                if  p_key in candidate_dict:
                    c_val=candidate_dict[p_key]
                    #scoreは単純に1/xとする(グループの少ないほうが一致度が高いと思われる)
                    candidate_dict[p_key]=(c_val[0]+1,c_val[1]+(1/key_freq))
                else:
                    n_val=(1,1/key_freq)
                    candidate_dict[p_key] = n_val
        #step2 sortによる上位特許の出力(count降順、score降順で並べ替え)
        sorted_items = sorted(candidate_dict.items(), key=lambda x: (-x[1][0], -x[1][1]))
        return sorted_items[:10]
    
    def setSimPatentsInfo(self,similar_patent_list:List[Tuple[str,Tuple[int,float]]])->List[dict[int,str,str,List[str]]]:
        """似た特許上位10個の完全な情報を返す"""
        p_admin=PatentsAdmin()
        result_dict_list=[]
        for similar_patent in similar_patent_list:
            result_dict=p_admin.sendPatentInfo(similar_patent)
            result_dict_list.append(result_dict)
        return result_dict_list
    
class PatentOffice:
    def __init__(self):
        pass
    
    def auth(self):
        po_admin=PatentOfficeAdmin()
        username = "g7nt4ga-q-s3"
        password = "yjdy9siq2k.2"

        # トークン取得のためのデータ
        data = {
            "grant_type": "password",
            "username": username,
            "password": password
        }

        # トークン取得のためのエンドポイント
        token_url = "https://ip-data.jpo.go.jp/auth/token"

        # HTTPヘッダー
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        # POSTリクエストを送信し、トークンを取得
        response = requests.post(token_url, data=data, headers=headers)

        # レスポンスの確認
        if response.status_code == 200:
            token = response.json().get("access_token")
            c_time=time.time()
            po_admin.setTimeGetAuthBefor(c_time)
            po_admin.setAuth(token)
            print("トークンの取得に成功しました")
        else:
            print(f"トークンの取得に失敗しました: ステータスコード {response.status_code}")
    
    def getUrlToFullPage(self,apply_number:str)->str:
        po_admin=PatentOfficeAdmin()
        b_time=po_admin.fetchTimeGetAuthBefor()
        c_time=time.time()
        #認証が1時間で切れるため
        if b_time == None or c_time-float(b_time)>3000:
            self.auth()
        access_token=po_admin.fetchAuth()
        # HTTPヘッダー
        headers={
            "Authorization":f"Bearer {access_token}"
        }
        # 固定アドレス取得のためのエンドポイント
        api_url =f"https://ip-data.jpo.go.jp/api/patent/v1/jpp_fixed_address/{apply_number}"
        print(api_url)
        response = requests.get(api_url, headers=headers)
        # レスポンスの確認
        if response.status_code == 200:
            data_dict=response.json().get("result")
            if int(data_dict["statusCode"])==100:
                url = data_dict.get("data").get("URL")
                print(f"取得したURL: {url}")
                return url
            else:
                error_message=data_dict["errorMessage"]
                print(error_message)
        else:
            print(f"トークンの取得に失敗しました: ステータスコード {response.status_code}")