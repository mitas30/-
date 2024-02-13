<script setup>
import { reactive, onMounted } from 'vue';

const patentList = reactive({ patents: [] });

const fetchPatentsFromServer = async () => {
    try {
        const response = await fetch('http://localhost:5000/api/get_result');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        patentList.patents = data;
    } catch (error) {
        console.error('Fetch error:', error);
    }
};

const viewFullPatent = async(patent) => {
    try{
        const response = await fetch('http://localhost:5000/api/get_patent_fullpage_url/'+patent.app_num_str);
        const data=await response.json();
        window.location.href=data.url;
    }catch(error){
        console.error('url error:', error);
    }
};
onMounted(() => fetchPatentsFromServer());
</script>

<template>
    <div class="table-container">
        <table>
            <thead>
                <tr>
                    <th>順位</th>
                    <th>一致キーワード数/<br>サブスコア</th>
                    <th>公開番号</th>
                    <th>公開日/公告日</th>
                    <th>発明の名称</th>
                    <th>キーワードリスト</th>
                    <th>詳しく見る</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(patent,index) in patentList.patents" :key="patent.priority_key">
                    <td>{{ index+1 }}</td>
                    <td>{{ patent.count }}/<br>{{ patent.score.toFixed(5) }}</td>
                    <td>{{ patent.priority_key }}</td>
                    <td>{{ patent.laid_open_date }}</td>
                    <td>{{ patent.name_of_invention }}</td>
                    <td>{{ patent.keyword_list.join(', ') }}</td>
                    <td>
                        <button class="button" @click="viewFullPatent(patent)">この特許の完全な情報を見る</button>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<style scoped>
.table-container {
    font-family: Arial, sans-serif;
    border-collapse: collapse;
    width: 100%;
    overflow-x: auto; /* テーブルが幅を超えた場合にスクロール可能にする */
}

.table-container th,
.table-container td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left; /* 左揃えにする */
    min-width: 100px; /* 各セルの最小幅 */
}

.table-container th {
    background-color: #4CAF50;
    color: white;
}

/* 重要な列のスタイル */
.table-container td:nth-child(6), 
.table-container td:nth-child(5) { 
    font-weight: bold;
    color: #333;
    background-color: #ddd;
}

.button {
    background-color: #437545;
    /* Green */
    border: none;
    color: white;
    padding: 10px 20px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 4px 2px;
    transition-duration: 0.4s;
    cursor: pointer;
}

.button:hover {
    background-color: white;
    color: black;
    border: 1px solid #437545;
}</style>