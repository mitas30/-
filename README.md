# SearchPatentWithLLM
**SearchPatentWithLLM**は、ユーザのアイデアと近い特許が無いか簡単に調べることができるebアプリケーション。
このアプリは、従来の[特許調査サイト](https://www.j-platpat.inpit.go.jp/)では自分のアイデアと似た特許があるか調べられない全ての発明家のために作られた。
ユーザは「どんな問題に対するアイデアか」、「アイデア名」、「アイデアに使う技術」、「どうやって問題を解決するか」を入力するだけで、自分のアイデアに近い特許を調べることができる。

詳細な設計については[こちら](URLを貼る)

## デモビデオ 
https://github.com/mitas30/SearchPatentWithLLM/assets/83048191/55631110-a75e-455d-a945-1d55f83efa7a

## 特徴
- a

# 技術概要
## System Architecture Diagram
### batch処理
[図](URL)
### 特許探索処理
[図](URL)

## Technologies Used
### python:
- [gemini-pro](https://platform.openai.com/docs/api-reference/chat)
- [embedding(made by OpenAI)](https://platform.openai.com/docs/api-reference/embeddings)
- [numpy](https://numpy.org/ja/),[fastcluster](https://danifold.net/fastcluster.html),[scilit-learn](https://scikit-learn.org/stable/),[scipy](https://scipy.org/)
- [matplotlib](https://matplotlib.org/stable/api/pyplot_summary.html#module-matplotlib.pyplot)
- [flask](https://flask.palletsprojects.com/en/3.0.x/),[flask_socketio](https://flask-socketio.readthedocs.io/en/latest/)
- [mongoDB](https://pymongo.readthedocs.io/en/stable/),[redis](https://github.com/redis/redis-py),[pinecone](https://docs.pinecone.io/reference/upsert)
- [Mupdf](https://pymupdf.readthedocs.io/ja/latest/)
- [concurrent.futures](https://docs.python.org/ja/3/library/concurrent.futures.html)

### javascript:
- [Vue.js](https://ja.vuejs.org/)
- [vue-router(for_SPA)](https://router.vuejs.org/)
- [socket.io](https://socket.io/)
- [axios](https://github.com/axios/axios)
