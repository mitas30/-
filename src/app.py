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
    r.set("idea","バーチャルコンパニオンアシスタント")
    r.set("problem","高齢者の孤独と社会的孤立")
    r.set('abstract',"""個別化されたインタラクション： AIアシスタントは、高齢者の個人的な興味や趣味に基づいてカスタマイズされた会話を提供します。
日常生活のサポート： リマインダー機能、健康管理、アポイントメントのスケジューリングなど、日常生活の様々な側面をサポートします。
感情的な支援： AIは高齢者の感情を認識し、適切な会話やアクティビティを通じて感情的なサポートを提供します。
社会的接続： ビデオ通話やメッセージング機能を通じて、家族や友人との繋がりをサポートします。
「バーチャルコンパニオンアシスタント」は、高齢者が社会的に活動的で健康的な生活を送るための手段を提供し、孤独感を軽減することを目指しています。""")
    r.set('tech',"""「バーチャルコンパニオンアシスタント」は、高齢者の日常生活を支援し、孤独感を軽減するために、以下のような先進的なAI技術を利用します。
1. 自然言語処理（NLP）
AIアシスタントは、自然言語処理（NLP）技術を使用して、高齢者との対話を実現します。これには、音声認識、テキスト解析、意図の理解、自然な応答生成が含まれます。高度なNLPアルゴリズムにより、アシスタントは会話のコンテキストを把握し、適切な返答を生成します。
2. 感情認識
AIアシスタントは、音声のトーン、言葉の選択、表情（ビデオ通話を使用する場合）を分析し、高齢者の感情状態を認識します。これにより、アシスタントはより感情的なサポートを提供し、対話を個人的かつ意味のあるものにします。
3. 機械学習とパーソナライゼーション
AIアシスタントは機械学習アルゴリズムを利用して、高齢者の興味、好み、行動パターンを学習します。これにより、個々のユーザーに合わせたカスタマイズされた体験を提供することができます。
4. ヘルスケアインテグレーション
健康管理機能を統合し、高齢者の健康状態をモニタリングします。これには、運動のリマインダー、薬の管理、必要に応じた医療サービスへのリンクなどが含まれます。
5. IoTデバイスとの統合
家庭内のスマートデバイスやセンサーとの連携を通じて、高齢者の安全と快適さをサポートします。例えば、温度調節、照明制御、安全監視などが自動化されます。""")
    r.set('solve',"""「バーチャルコンパニオンアシスタント」は、高齢者の孤独感を軽減し、社会的孤立を防ぐために以下のような方法で機能します。
1. 対話とエンゲージメント
アシスタントは日常会話を通じて高齢者とのエンゲージメントを図ります。これは、話し相手としての役割を果たすことで、孤独感を軽減し、心理的なサポートを提供します。話題は、高齢者の興味や過去の経験に基づいて選ばれ、個々のユーザーに合わせた対話が行われます。
2. 日常生活の支援
アシスタントはリマインダー機能を提供し、日常生活のスケジュール管理をサポートします。これには、薬の服用リマインダー、医療アポイントメント、日常的な活動のスケジューリングが含まれます。これにより、高齢者は自立した生活を送ることができ、生活の質が向上します。
3. 感情的なサポート
AIアシスタントは、高齢者の感情状態を認識し、適切な応答やアクティビティを提供します。例えば、ユーザーが寂しそうに見える場合、アシスタントは慰めの言葉をかけたり、気晴らしのためのアクティビティを提案したりします。
4. 家族や友人との繋がり
アシスタントはビデオ通話やメッセージング機能を通じて、家族や友人との社会的な繋がりをサポートします。これにより、高齢者は社会的に孤立することなく、愛する人たちとの関係を保つことができます。
5. ユーザーの健康と安全の促進
健康管理機能とIoTデバイスの統合により、高齢者の健康と安全が促進されます。アシスタントは、健康状態のモニタリングを行い、必要に応じて家族や医療提供者に通知することができます。""")
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

