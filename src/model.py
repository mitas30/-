"""データベースにアクセスする層
service層を介して実際の操作を行うこと"""
import fitz,os,re,shutil,requests
from redis import Redis
from pymongo import MongoClient
from typing import Tuple,List,Union
from pinecone import Pinecone
from bson.objectid import ObjectId
from error_class import SplitError

r=Redis()

class DBIngestor:
    SUCCESS=1
    ERROR_IN_OTHER=-1
    ERROR_IN_ABSTRACT=-2
    ERROR_IN_DETAIL=-3
    
    """PDFファイルの内容を取得して、DBに格納する"""
    def _get_file_number(self,filename)->int:
        """ファイル名から数値を抽出する関数（ファイル名が数値でなければ-1を返す）"""
        ret_digit=re.split("\.",filename)[0]
        if ret_digit.isdecimal()==False:
            return -1
        else:
            return int(ret_digit)

    def movingAllFile(self,source_folder:str="D:\特許、実用新案データ\MastDownloadHere",
                      dest_folder:str="D:\特許、実用新案データ\FileNotYetMovingToDatabase",
                      not_dest_folder:str="D:\特許、実用新案データ\FileNotObject")->None:
        """フォルダ内の(ネストされていても可能)全てのファイルをdest_folderに移動させる。特開でない場合はnot_dest_folderに移動させる"""
        print("Batch[ダウンロードしたPDFを移動させる] 開始")
        #step1: とりあえず全部移動させる
        for dirpath, dirnames, filenames in os.walk(source_folder):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                dest_path = os.path.join(dest_folder, filename)
                # ファイルの移動
                shutil.move(file_path, dest_path)
        #step2: 数字以外のファイルも移動させる
        for irregular_filename in os.listdir(dest_folder):
            if self._get_file_number(irregular_filename)==-1:
                    dest_path = os.path.join(dest_folder, irregular_filename)
                    not_dest_path = os.path.join(not_dest_folder, irregular_filename)
                    shutil.move(dest_path, not_dest_path)
                    print("moving to not object file:",irregular_filename)
        #step3:連番ではない、変更要請のファイルも移動させる 念のため3回繰り返す
        for i in range(3):
            print(str(i+1),"周目:")
            # フォルダ内のファイル名を取得して昇順にソート
            files = sorted(os.listdir(dest_folder), key=self._get_file_number)
            previous_number = None
            previous_filename=None
            for filename in files:
                # 現在のファイルの番号を取得
                current_number = self._get_file_number(filename)
                # 前のファイルの番号と比較して、連番でなければ移動
                if previous_number is not None and current_number != previous_number + 1:
                    dest_path = os.path.join(dest_folder, previous_filename)
                    not_dest_path = os.path.join(not_dest_folder, previous_filename)
                    shutil.move(dest_path, not_dest_path)
                    print("moving to not_dest_file:",previous_filename)
                # 現在のファイル番号を前のファイル番号として記憶
                previous_number = current_number
                previous_filename=filename
        print("Batch[ダウンロードしたPDFを移動させる] 完了")
                
    def convertClassStrToList(self,ipc_class_str)->List[str]:
        """現時点では、class_strから、単一のキーワードのリストに変換する"""
        class_list=[]
        raw_class_list=re.split("\n",ipc_class_str)[:-1]
        for raw_keycode in raw_class_list:
            keycode=re.sub("\s+\(.+\)","",raw_keycode)
            class_list.append(keycode)
        return class_list
        
    def _extractAbstractAtLpatent(self,description:str)->Tuple[str,List[str],str,str,str,str]:
        """
    公開特許広報の要約から特定の情報を抽出する。

    このメソッドでは、与えられた特許の要約テキストから、特許の基本情報を抽出する。
    主に正規表現を使用してテキストを処理し、特定のパターンに基づいてテキストを分割して情報を取得する。
    テキストが予期されたフォーマットになっていない場合、エラーとして0のタプルを返す。

    Parameters:
    description (str): 抽出対象の特許の要約テキスト。

    成功した場合は、(priority_key, application_number,ipc_class_list, laid_open_date, name_of_invention, problem, solving_way) のタプルを返す。
    失敗した場合は、SplitErrorを返す
        """
        normalize_data=re.sub("\(\d+\)","",re.sub("JP\s+.*\n","",re.sub("【\s*選\s*択\s*図\s*】.*\n","",description)))
        split_data_list=re.split("【\s*要\s*約\s*】.*\n",normalize_data)
        if len(split_data_list)!=2:
            raise SplitError("【要約】が存在しない")
        basic_info_list=re.split("【発明の名称】",split_data_list[0])
        if len(basic_info_list)!=2:
            raise SplitError("【発明の名称】が存在しない")
        name_of_invention=basic_info_list[1]
        #()で囲うと、groupで取得できる
        if extracted_number:=re.search(r'特願(\d{4})-(\d+)',basic_info_list[0]):
            year = extracted_number.group(1)
            number = int(extracted_number.group(2))
            application_number = f"{year}{number:06}"
        else:
            raise ValueError("出願番号が存在しない")
        fh_basic_info=re.split("ＦＩ",basic_info_list[0])
        if len(fh_basic_info)!=2:
           raise SplitError("ＦＩが存在しない")
        ipc_list=re.split("Int\.Cl.+\n",fh_basic_info[0])
        if len(ipc_list)!=2:
          raise SplitError("Int Cl.が存在しない")
        ipc_class_str=ipc_list[1]
        ipc_class_list=self.convertClassStrToList(ipc_class_str)
        if m:=re.search("公開日.*\n",fh_basic_info[0]):
            if m2:=re.search("\(.+\)",m.group()):
                laid_open_date=re.sub("[\(\)]","",m2.group())
            else:
                laid_open_date=""
        else:
            laid_open_date=""
        lh_splited_data=re.sub("(?<!】)(?<!）)(?<!。)\n","",split_data_list[1])
        split_data_list=re.split("【\s*解\s*決\s*手\s*段\s*】",lh_splited_data)
        if len(split_data_list)!=2:
            raise SplitError("【解決手段】が存在しない")
        problem=re.sub("【課題】","",split_data_list[0])
        solving_way=split_data_list[1]
        return application_number,ipc_class_list,laid_open_date,name_of_invention,problem,solving_way
    
    def _extractAbstractAtGpatent(self,description:str)->Tuple[str,List[str],str,str,str]:
        normalize_data=re.sub("\(\d+\)","",re.sub("JP\s+.*\n","",re.sub("【\s*選\s*択\s*図\s*】.*\n","",description)))
        split_data_list=re.split("【\s*要\s*約\s*】.*\n",normalize_data)
        if len(split_data_list)!=2:
            raise SplitError("【要約】が存在しない")
        abstract=split_data_list[1]
        basic_info_list=re.split("【発明の名称】",split_data_list[0])
        if len(basic_info_list)!=2:
            raise SplitError("【発明の名称】が存在しない")
        name_of_invention=basic_info_list[1]
        #()で囲うと、groupで取得できる
        if extracted_number:=re.search(r'特願(\d{4})-(\d+)',basic_info_list[0]):
            year = extracted_number.group(1)
            number = int(extracted_number.group(2))
            application_number = f"{year}{number:06}"
        else:
            raise ValueError("出願番号が存在しない")
        fh_basic_info=re.split("ＦＩ",basic_info_list[0])
        if len(fh_basic_info)!=2:
           raise SplitError("ＦＩが存在しない")
        ipc_list=re.split("Int\.Cl.+\n",fh_basic_info[0])
        if len(ipc_list)!=2:
          raise SplitError("Int Cl.が存在しない")
        ipc_class_str=ipc_list[1]
        ipc_class_list=self.convertClassStrToList(ipc_class_str)
        if m:=re.search("公開日.*\n",fh_basic_info[0]):
            if m2:=re.search("\(.+\)",m.group()):
                laid_open_date=re.sub("[\(\)]","",m2.group())
            else:
                laid_open_date=""
        else:
            laid_open_date=""
        return application_number,ipc_class_list,laid_open_date,name_of_invention,abstract

    def _extractDetailDescription(self,description:str)->Tuple[str,str,str,str]:
        """特許の詳細を返す関数。エラーのときはValueErrorを返す。"""
        sub_data1=re.sub("(10\n20\n30\n40\n50\n)|(10\n20\n)","",description)
        sub_data2=re.sub("\(\d+\)\n","",sub_data1)
        sub_data3=re.sub("【\d+】\n","",sub_data2)
        sub_data4=re.sub("JP\s+.*\n","",sub_data3)
        save_data=re.sub("(?<!】)(?<!）)(?<!。)\n","",sub_data4)
        split_at_background=re.split("【背景技術】",save_data)
        if len(split_at_background)!=2:
            raise SplitError("【背景技術】が存在しない")
        split_at_tech_field=re.split("【技術分野】",split_at_background[0])
        if len(split_at_tech_field)!=2:
           raise SplitError("【技術分野】が存在しない")
        tech_field=split_at_tech_field[1]
        #print("tech_field",tech_field)
        #print(split_at_background[1])
        split_at_detail_problem=re.split("【発明が解決しようとする課題】",split_at_background[1])
        if len(split_at_detail_problem)!=2:
            raise SplitError("【発明が解決しようとする課題】が存在しない")
        split_at_solving_way=re.split("【課題を解決するための手段】",split_at_detail_problem[1])
        if len(split_at_solving_way)!=2:
            raise SplitError("【課題を解決するための手段】が存在しない")   
        detail_problem=split_at_solving_way[0]
        #print("detail_problem",detail_problem)
        split_at_effect_of_invention=re.split("【発明の効果】",split_at_solving_way[1])
        if len(split_at_effect_of_invention)!=2:
            way_to_solve_problem=split_at_solving_way[1]
            effect_of_invention=""
        else:
            way_to_solve_problem=split_at_effect_of_invention[0]
            effect_of_invention=split_at_effect_of_invention[1]
        #print("way_to_solve_proble",way_to_solve_proble)
        #print("effect_of_invention",effect_of_invention)
        return tech_field,effect_of_invention,way_to_solve_problem,detail_problem

    def _insertDataAsJSON(self,p_type:str,priority_key:str,application_number:str,ipc_class_list:List[str],laid_open_date:str,name_of_invention:str,problem:str,solving_way:str,abstract:str,tech_field:str,effect_of_invention:str,detail_way_to_solve_problems:str,detail_problem:str)->int:
        """JSONを作ってそのままmongoDBに格納する 成功ならSUCCESSを返す"""
        client=MongoClient()
        #db->collection->データの階層構造
        db=client["patent_db"]
        collection=db["patents"]
        #Jsonは、pythonの辞書のような書き方をする
        if p_type=="local":
            patent_data={
                'priority_key':priority_key,
                'application_number':application_number,
                'ipc_class_code_list':ipc_class_list,
                'laid_open_date':laid_open_date,
                'name_of_invention':name_of_invention,
                'problem':problem,
                'solving_way':solving_way,
                'tech_field':tech_field,
                'effect_of_invention':effect_of_invention,
                'detail_way_to_solve_problems':detail_way_to_solve_problems,
                'detail_problem':detail_problem
                }
        elif p_type=="global":
            patent_data={
                'priority_key':priority_key,
                'application_number':application_number,
                'ipc_class_code_list':ipc_class_list,
                'laid_open_date':laid_open_date,
                'name_of_invention':name_of_invention,
                'abstract':abstract,
                'tech_field':tech_field,
                'effect_of_invention':effect_of_invention,
                'detail_way_to_solve_problems':detail_way_to_solve_problems,
                'detail_problem':detail_problem
                }
        if collection.find_one({'priority_key':priority_key})==None:
            collection.insert_one(patent_data)
            #print("データ登録完了:",priority_key)
            return self.SUCCESS
        else:
            if priority_key=="":
                print("主キーが抽出できてないファイル:",name_of_invention)
                return self.ERROR_IN_OTHER
            else:
                print("すでに同じkeyのデータが登録されている:",priority_key)
                return self.ERROR_IN_OTHER
        
    def insertPatentDataIntoDB(self,full_file_path:str)->int:
        """
    指定されたPDFファイルから特許データを抽出し、データベースに挿入する。

    この関数は、PDFファイルを読み込み、特許の要約と詳細な説明部分を抽出する。
    抽出したデータは、_subtractAbstract と _subtractDetailDescription メソッドを
    用いてさらに解析され、最終的に _insertDataAsJSON メソッドを通じて
    データベースに挿入される。特定のセクションが見つからない場合、
    関数は異なるエラーコードを返す。

    Parameters:
    full_file_path (str): 抽出する特許データが含まれるPDFファイルのパス。

    Returns:
    int: 処理の成否を示すコード。成功した場合は正の整数、失敗した場合は負の整数または0。
        """
        pdf_doc=fitz.open(full_file_path)
        i=0
        content=""
        while i<pdf_doc.page_count:
            pdf_page=pdf_doc[i]
            content+=pdf_page.get_text("text")
            areas = pdf_page.search_for("【図面の簡単な説明】")
            if areas !=[]:
                break
            i+=1
        try:
            if i==pdf_doc.page_count:
                raise SplitError("【図面の簡単な説明】が見つからなかった")
            split_data1=re.split("【特許請求の範囲】",re.split("【図面の簡単な説明】",content)[0])
            if len(split_data1)!=2:
                raise SplitError("【特許請求の範囲】が見つからなかった")
            split_data2=re.split("【発明の詳細な説明】",split_data1[1])
            if len(split_data2)!=2:
                raise SplitError("【発明の詳細な説明】が見つからなかった")
            detail_description="【発明の詳細な説明】"+split_data2[1]
        except SplitError as e:
            print(f"全体構造のSplitError: {e}")
            return self.ERROR_IN_OTHER
        #Step 文字列を成形する
        try:
            if substring:=re.search(r"特開.+\n",split_data1[0]):
                priority_key="特開"+re.sub(r"\D","",substring.group())
                application_number,ipc_class_list,laid_open_date,name_of_invention,problem,solving_way=self._extractAbstractAtLpatent(split_data1[0])
                p_type="local"
                abstract=""
            elif m:=re.search(r"特表.+\n",split_data1[0]):
                priority_key="特表"+re.sub(r"\D","",m.group())
                application_number,ipc_class_list,laid_open_date,name_of_invention,abstract=self._extractAbstractAtGpatent(split_data1[0])
                p_type="global"
                problem="",
                solving_way=""
            else:
                raise ValueError("主キーが存在しない")
        except SplitError as e:
            print(f"要約部分のSplitError: {e}")
            return self.ERROR_IN_ABSTRACT
        except ValueError as e:
            print(f"{e}")
            return self.ERROR_IN_ABSTRACT
        try:
            #Localなら発明の効果は抜き出さないほうが良い
            tech_field,effect_of_invention,detail_way_to_solve_problems,detail_problem=self._extractDetailDescription(detail_description)
        except SplitError as e:
            print(f"詳細部分のSplitError:{e}")
            return self.ERROR_IN_DETAIL
        retcode=self._insertDataAsJSON(p_type,priority_key,application_number,ipc_class_list,laid_open_date,name_of_invention,problem,solving_way,abstract,tech_field,effect_of_invention,detail_way_to_solve_problems,detail_problem)
        return retcode

    def batchExtractPatentDatas(self,fetch_folder_path:str="D:\特許、実用新案データ\FileNotYetMovingToDatabase",
                                abstract_exception_folder:str="D:\特許、実用新案データ\ErrorFile\AboutAbstract",
                                detail_exception_folder:str="D:\特許、実用新案データ\ErrorFile\AboutDetail",
                                other_exception_folder:str="D:\特許、実用新案データ\ErrorFile\Others")->None:
        """
    指定されたフォルダ内の全てのPDFファイルから特許データを抽出し、データベースに格納するバッチ処理を行う。

    この関数は、fetch_folder_path 内の各PDFファイルに対して insertPatentDataIntoDB メソッドを実行し、
    特許データをデータベースに格納する。データの抽出と格納が成功した場合はファイルを削除し、
    失敗した場合はエラーの種類に応じて異なる例外フォルダにファイルを移動する。

    Parameters:
    fetch_folder_path (str): データを抽出するPDFファイルが格納されているフォルダのパス。
    abstract_exception_folder (str): 要約データの抽出に失敗したファイルを移動するフォルダのパス。
    detail_exception_folder (str): 詳細データの抽出に失敗したファイルを移動するフォルダのパス。
    other_exception_folder (str): その他の理由で処理に失敗したファイルを移動するフォルダのパス。

    Returns:
    None
        """
        print("Batch[データベースへの格納] start")
        for filename in os.listdir(fetch_folder_path):
            file_path = os.path.join(fetch_folder_path, filename)
            if os.path.isfile(file_path):
                retval=self.insertPatentDataIntoDB(file_path)
                if retval<0:
                    print("正常でないpdfファイル:",file_path)
                    print("-"*80)
                    if retval==self.ERROR_IN_OTHER:
                        shutil.move(file_path,other_exception_folder)
                    if retval==self.ERROR_IN_ABSTRACT:
                        shutil.move(file_path,abstract_exception_folder)
                    elif retval==self.ERROR_IN_DETAIL:
                        shutil.move(file_path,detail_exception_folder)
                else:
                    os.remove(file_path)
        print("Batch[データベースへの格納] complete")

class PatentsAdmin:
    """MongoのPatentsコレクションの管理者"""
    
    def __init__(self,collction_name:str="patents",db_name:str="patent_db",port:int=27017,ip_addr:str="localhost"):
        self.client=MongoClient(ip_addr,port)
        self.db=self.client[db_name]
        self.collection=self.db[collction_name]
        
    def findAllTarget(self):
        """keywordが作成されていない全ての特許を取得する"""
        return self.collection.find({"keyword_list":{"$exists":False}})
    
    def extractDesirableKeyword(self,target_doc)->Tuple[str,str,str,str,str,str]:
        """特許からキーワードを抽出するのに使用する"""
        priority_key=target_doc.get("priority_key")
        name_of_invention=target_doc.get("name_of_invention")
        tech_field=target_doc.get("tech_field")
        way_to_solve_problems=target_doc.get("detail_way_to_solve_problems")
        effect_of_invention=target_doc.get("effect_of_invention")
        detail_problem=target_doc.get("detail_problem")
        return priority_key,name_of_invention,tech_field,way_to_solve_problems,effect_of_invention,detail_problem
    
    def insertAllKeywords(self,priority_key:str,keyword_list:list):
        if len(keyword_list)==10:
            self.collection.update_one(
                {'priority_key':priority_key},
                { "$set": { 'keyword_list': keyword_list } }
            )
            print("Done")
            
    def fetchPatentPKeysHaveCertainKeyword(self,keyword_name:str):
        """あるキーワードをキーワードリストに持つ特許の主キーを返す。"""
        return self.collection.find({"keyword_list":{"$in":[keyword_name]}})
    
    def sendPatentInfo(self,sim_patent:Tuple[str,Tuple[int,float]])->dict[str,str,str,str,List[str],int,float]:
        """特許の完全な情報を見るための情報"""
        info_dict={}
        priority_key=sim_patent[0]
        #projectionのデフォルトは1(表示)
        patent_doc=self.collection.find_one({'priority_key':priority_key},projection={"_id":0,"solving_way":0,"tech_field":0,"effect_of_invention":0,"detail_way_to_solve_problems":0,"detail_problem":0})
        info_dict['priority_key']=patent_doc.get('priority_key')
        info_dict['app_num_str']=patent_doc.get('application_number')
        info_dict['laid_open_date']=patent_doc.get('laid_open_date')
        info_dict['name_of_invention']=re.sub("\n","",patent_doc.get('name_of_invention'))
        info_dict['keyword_list']=patent_doc.get('keyword_list')
        info_dict['count']=sim_patent[1][0]
        info_dict['score']=sim_patent[1][1]
        return info_dict
             
class KeywordManager:
    """キーワードとそのembeddingの管理(バックアップ用)を行う"""

    def __init__(self,collction_name:str="keywords",db_name:str="patent_db",port:int=27017,ip_addr:str="localhost"):
        self.client=MongoClient(ip_addr,port)
        self.db=self.client[db_name]
        self.collection=self.db[collction_name]
        
    def processKeywordsStrToList(self,keywords:str)->List[str]:
        """受け取ったキーワードをListに変換する"""
        keywords=re.search("\[.+\]",keywords)
        if keywords:
            keywords_list=re.split(",",re.sub("\[|\]","",keywords.group()))
            return keywords_list
        else:
            return []
    
    def insertKeywordsOfOnePatentIntoMongo(self,api_response_txt:str)->List[str]:
        """あるkeywordがdbに存在しなかった場合、dbにkeywordを格納する"""
        keywords_list=self.processKeywordsStrToList(api_response_txt)
        if len(keywords_list)==10:
            for keyword in keywords_list:
                keyword_info={
                    'keyword':keyword
                }
                if self.collection.find_one({'keyword':keyword})==None:
                    self.collection.insert_one(keyword_info)
        return keywords_list
    
    def extractAllKeywordNotEmbed(self,limit_count:int):
        return self.collection.find({"embed":{"$exists":False}}).limit(limit_count)
     
    def insertEmbedOfOnePatentIntoMongo(self,keyword:str,embedding:List[int]):
        self.collection.update_one({'keyword':keyword},{"$set":{'embed':embedding}})
        
    def extractAllKeywordForClustering(self,limit_count:int)->Tuple[List[str],List[List[float]]]:
        keyword_list=[]
        embed_list=[]
        cursor=self.collection.find({"embed":{"$exists":True}}).limit(limit_count)
        for keyword_attr in cursor:
            keyword=keyword_attr.get('keyword')
            embed=keyword_attr.get('embed')
            keyword_list.append(keyword)
            embed_list.append(embed)
        return keyword_list,embed_list
    
    def provideAllKeywordAsDictNotInPineCone(self)->List[dict]:
        ret_list=[]
        #{}は辞書 pineconeだけど、pinecoreとしてしまったので、そのままにしておく
        cursor=self.collection.find({
            "is_in_pinecore":{"$exists":False},
            "embed":{"$exists":True}
            })
        for collection in cursor:
            key=str(collection.get("_id"))
            embed=collection.get("embed")
            keyword_attr_dict={
                'id':key,
                'values':embed
            }
            ret_list.append(keyword_attr_dict)
        return ret_list
    
    def addCheckToKeywords(self,key_attr_list:List[dict]):
        for key_attr in key_attr_list:
            _id=ObjectId(key_attr["id"])
            self.collection.update_one({'_id':_id},{'$set':{'is_in_pinecore':"true"}})
            
    def findKeywordFromID(self,_id:str):
        doc=self.collection.find_one({"_id":ObjectId(_id)})
        return doc
    
    def findAllKeywordInSameGroup(self,_id:str)->Tuple[int,List[str]]:
        """_id(入力)のグループを探し、同じグループのkeyword名をList形式で全て返却する"""
        doc=self.collection.find_one({"_id":ObjectId(_id)},projection={"embed":0,"_id":0})
        group=doc.get("group")
        name_of_keyword=doc.get("keyword")
        print("group:",group,"name of keyword:",name_of_keyword)
        cursor=self.collection.find({"group":group})
        count=0
        ret_list=[]
        for doc in cursor:
            count+=1
            keyword=doc.get("keyword")
            ret_list.append(keyword)
        return count,ret_list
            
    def insertGroupNum(self,keyword:str,group_num:int):
        """keyword(入力)に、グループ番号を挿入する。ただし、update処理"""
        self.collection.update_one({"keyword":keyword},{"$set":{"group":group_num}})
        
class PineConeAdmin:
    """ベクトルデータベースPineConeに関する処理を行う"""
    
    def __init__(self):
        client=Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        self.index=client.Index('patents-index')
        
    def upsertSomeTargetEmbed(self,keyword_attr_dict:List[dict])->None:
        self.index.upsert(vectors=keyword_attr_dict,namespace='keyword_embed')
        
    def findNearestKeyword(self,embed:List[float])->List[dict[str,float]]:
        """strで最も距離の近い_idのデータとscoreを返却する"""
        response=self.index.query(
            namespace='keyword_embed',
            top_k=1,
            include_values=False,
            include_metadata=False,
            vector=embed
        )
        return response["matches"]
    
    def deleteAll(self,namespace):
        """NOTE:PineConeのあるnamespace上の全てのベクトルを消去するので注意しよう"""
        self.index.delete(delete_all=True,namespace=namespace)
        
    def knowDbInfo(self):
        #RESTful API
        url = "https://patents-index-reonxyg.svc.gcp-starter.pinecone.io/describe_index_stats"
        api_key=os.getenv("PINECONE_API_KEY")
        headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "Api-Key":api_key
    }
        response = requests.post(url,headers=headers)
        print(response.text)

class PatentOfficeAdmin:
    def __init__(self):
        pass
    
    def setTimeGetAuthBefor(self,time:float):
        r.set("auth_time",time)
        
    def fetchTimeGetAuthBefor(self)->Union[str,None]:
        auth_time=r.get("auth_time")
        if auth_time!=None:
            return auth_time.decode('utf-8')
        else:
            return None
    
    def setAuth(self,token:str):
        r.set("token",token)
    
    def fetchAuth(self)->Union[str,None]:
        token=r.get("token")
        if token!=None:
            return token.decode('utf-8')
        else:
            return None
    