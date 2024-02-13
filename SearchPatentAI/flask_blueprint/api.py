from flask import Blueprint,request,jsonify
from redis import Redis
from service import PatentOffice

#デコレータにつけるobject名
api = Blueprint('api',__name__,url_prefix='/api')
r=Redis()

@api.route('/set_info/idea_and_problem',methods=["POST"])
def setIdeaAndProblem():
    data = request.json
    r.set("idea",data["idea"])
    r.set("problem",data["problem"])
    return jsonify({"message":"データの受け取り完了"})

@api.route('/set_info/abstract',methods=["POST"])
def setAbstract():
    data = request.json
    r.set("abstract",data["abstract"])
    return jsonify({"message":"データの受け取り完了"})

@api.route('/set_info/tech',methods=["POST"])
def setInfo():
    data = request.json
    r.set("tech",data["tech"])
    return jsonify({"message":"データの受け取り完了"})

@api.route('/set_info/solve',methods=["POST"])
def setSolve():
    data = request.json
    r.set("solve",data["solve"])
    return jsonify({"message":"データの受け取り完了"})

@api.route('/get_result',methods=["GET"])
def getResult():
    #json形式で渡される
    return r.get("similar_res")

@api.route('/get_patent_fullpage_url/<app_num>',methods=["GET"])
def geturlToFullPage(app_num:str):
    poffice=PatentOffice()
    url=poffice.getUrlToFullPage(app_num)
    return jsonify({"url":url})
    