# SearchPatentWithLLM
**SearchPatentWithLLM**は、ユーザのアイデアと近い特許が無いか簡単に調べることができるwebアプリケーションである。<br>
このアプリは、従来の[特許調査サイト](https://www.j-platpat.inpit.go.jp/)を使う知識の無い全ての発明家のために作られた。<br>
ユーザは「どんな問題に対するアイデアか」、「アイデア名」、「アイデアに使う技術」、「どうやって問題を解決するか」を入力するだけで、自分のアイデアに近い特許が無いか調べることができる。

## デモビデオ 
https://github.com/mitas30/SearchPatentWithLLM/assets/83048191/55631110-a75e-455d-a945-1d55f83efa7a

## 特徴
このソフトウェアは、特許検索のための新しいアプローチを提供します。主な特徴は以下の通りです：

- **アイデアベースの入力**
    - ユーザーはキーワードではなく、自分のアイデアの概要、技術、問題解決方法、解決する問題の4つの側面から入力します。

- **LLMによる自動キーワード抽出**
    - Large Language Model (LLM) を使用して、特許文書とあなたのアイデアから10個のキーワードを自動的に抽出します。

### 技術的観点
- **embeddingと階層的クラスタリングを使用した前処理**
    - キーワードをembeddingに変換し、階層的クラスタリングを使用して、意味的に近いキーワードを同じクラスに分類します。

- **セマンティック検索手法**
    - embeddingされたキーワードから最も近いワードを特定し、そのワードのクラスに属する全てのワードを使用して、ワード一致数が多いトップ10の特許を特定します。

### 新しいアプローチ
- **LLM、特許検索、AIの組み合わせ**
    - これらの技術を組み合わせることで、従来のキーワードベースの検索とは異なる、新しい特許検索手法を提供します。

# 技術概要
## workflow
### batch処理
![pre_activity](https://github.com/mitas30/SearchPatentWithLLM/assets/83048191/5493b22a-b84e-4543-a38a-6087ddcb3e02)

### 特許探索処理
![main_activity](https://github.com/mitas30/SearchPatentWithLLM/assets/83048191/5962d5fa-bf97-4e01-92ac-f177553d9e5e)


## 使用した主要ライブラリ、API
### python:
- [gemini-pro](https://platform.openai.com/docs/api-reference/chat)
- [text-embedding-3-small](https://platform.openai.com/docs/api-reference/embeddings)
- [numpy](https://numpy.org/ja/),[fastcluster](https://danifold.net/fastcluster.html),[scilit-learn](https://scikit-learn.org/stable/),[scipy](https://scipy.org/)
- [matplotlib](https://matplotlib.org/stable/api/pyplot_summary.html#module-matplotlib.pyplot)
- [flask](https://flask.palletsprojects.com/en/3.0.x/),[flask_socketio](https://flask-socketio.readthedocs.io/en/latest/)
- [mongoDB](https://pymongo.readthedocs.io/en/stable/),[redis](https://github.com/redis/redis-py),[pinecone](https://docs.pinecone.io/reference/upsert)
- [Mupdf](https://pymupdf.readthedocs.io/ja/latest/)
- [concurrent.futures](https://docs.python.org/ja/3/library/concurrent.futures.html)

### javascript:
- [Vue.js](https://ja.vuejs.org/)
- [vue-router(SPA)](https://router.vuejs.org/)
- [socket.io](https://socket.io/)
- [axios](https://github.com/axios/axios)
