from flask import Flask,request
from flask_blueprint.api import api
from flask_socketio import SocketIO
from flask_cors import CORS
import redis,json
from service import LLMManipulator as Manip,Embedder,FetchSearchResult

#初期化
app = Flask(__name__)
app.register_blueprint(api)
app.config['SECRET_KEY'] = 'test_secret'
CORS(app)
socketio = SocketIO(app,cors_allowed_origins="*")
r=redis.Redis()

#多数からアクセスされることを考えていない設計(動画で見せるだけ)
@socketio.on('connect')
def handle_connect():
    r.set("sid",request.sid)
    print(f"Client connected: session_id={request.sid}")

@socketio.on('disconnect')
def handle_disconnect():
    print(f"Client disconnected")
    
@socketio.on('start_search')
def socketioStart():
    idea=r.get('idea').decode('utf-8')
    problem=r.get('problem').decode('utf-8')
    abstract=r.get('abstract').decode('utf-8')
    tech=r.get('tech').decode('utf-8')
    solve=r.get('solve').decode('utf-8')
    #step1: アイデアをキーワードに変換する
    manip=Manip()
    keyword_list=manip.extractKeywordFromUserIdea(idea,problem,abstract,tech,solve)
    print(keyword_list)
    socketio.emit('convert_complete',{'message':"アイデアをキーワードに変換しました。"})
    #step2: アイデアの各キーワードをベクトル化して、同じグループのキーワードを集める
    fsresult=FetchSearchResult()
    embedder=Embedder()
    #keyword名の格納されたList
    all_keyword_list=[]
    for idea_keyword in keyword_list:
        embeded_keyword=embedder.embedKeyword(idea_keyword)
        nearest_keyword_id=fsresult.tellKwardInSameGroup(embeded_keyword)
        if nearest_keyword_id!="":
            all_keyword_list+=fsresult.fetchAllKeywordInSameGroup(nearest_keyword_id)
    socketio.emit('search_complete',{'message':"同じグループのキーワードを全て集計しました。"})
    #step3: アイデアと類似度の高い特許を取ってきてredisのsimilar_resに格納する
    similar_patent_list=fsresult.suggest10NearestPatents(all_keyword_list)
    result_dict_list=fsresult.setSimPatentsInfo(similar_patent_list)
    r.set("similar_res",json.dumps(result_dict_list))
    socketio.emit('response_ready')

#コマンドラインから実行された場合のみ、__name__=='__main__'となる
if __name__ == '__main__':
    socketio.run(app,debug=True)
    r.flushall()

