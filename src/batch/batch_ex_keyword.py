# 特許の説明から、特許を端的に表す10個のキーワードを抽出する
# 前処理段階の処理
import sys

sys.path.append("SearchPatentAI/src")
from service import LLMManipulator as Manip
from model import PatentsAdmin, KeywordManager
from concurrent.futures import ThreadPoolExecutor


# LLMで特許文書からキーワードを抽出するbatch処理
def process_document(doc, manipulator, updator, manager):
    (
        priority_key,
        name_of_invention,
        tech_field,
        way_to_solve_problems,
        effect_of_invention,
        detail_assignment,
    ) = updator.extractDesirableKeyword(doc)
    response_text = manipulator.extractKeywordFromSentence(
        name_of_invention,
        tech_field,
        way_to_solve_problems,
        effect_of_invention,
        detail_assignment,
    )
    if type(response_text) == str:
        keyword_list = manager.insertKeywordsOfOnePatentIntoMongo(response_text)
        updator.insertAllKeywords(priority_key, keyword_list)


manipulator = Manip()
updator = PatentsAdmin()
manager = KeywordManager()
all_docs = updator.findAllTarget()
# マルチスレッドでの並行処理(これもAPI処理がメイン)
with ThreadPoolExecutor(max_workers=7) as executor:
    completed_count = 0
    futures = [
        executor.submit(process_document, doc, manipulator, updator, manager)
        for doc in all_docs
    ]
