<script setup>
import { useRouter } from 'vue-router';
import { ref }from 'vue';
import axios from 'axios';

const router = useRouter();

const form=ref({
  way_to_solve:'',
});

const submitForm = async() => {
  try{
    await axios.post('http://localhost:5000/api/set_info/solve', {
      solve: form.value.way_to_solve
    });
    router.push('/waiting');
  }catch(error){
    console.error('There was an error submitting the form:', error);
  }
};
</script>

<template>
  <div class="form-container">
    <h1>Step4:どのように問題を解決するか教えてください</h1>
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label for="ideaSummary">問題解決の方法</label>
        <textarea id="ideaSummary" v-model="form.way_to_solve"
        placeholder="クリーンエア・アーバンシールドは、統合された空気清浄技術を使用して都市部の大気汚染問題を解決します。
高度なHEPAフィルターは、PM2.5やPM10などの微細粒子物質を効果的に捕捉し、除去します。

活性炭フィルターは、NOxやSOxなどの有害ガスを吸収します。

光触媒コーティングは、太陽光の下で活性化し、有害物質を無害な物質に分解します。

このシステムは、エネルギー効率の良い設計に基づいており、太陽光発電パネルと組み合わせることでさらに環境に優しいものとなります。

スマートモニタリングシステムにより、大気の質をリアルタイムで監視し、汚染レベルに応じて清浄システムの動作を調整します。

これらの技術を通じて、都市部の空気質を大幅に改善し、市民の健康リスクを軽減する効果を期待できます。"></textarea>
       </div>
      <button type="submit">Next</button>
    </form>
  </div>
</template>

<style scoped>
.form-container {
  width: 55%;
  height: 60%;
  margin: 10px 10%;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #f9f9f9;
}

form{
  height: 65%;
  margin:auto 5%;
}

.form-group {
  height: 80%;
  margin-bottom: 20px;
}


label {
  display: block;
  margin-bottom: 5px;
}

textarea {
  width: 100%;
  height: 70%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button[type="submit"] {
  padding: 10px 20px;
  background-color: #007bff;
  border: none;
  border-radius: 4px;
  color: white;
  cursor: pointer;
}

button[type="submit"]:hover {
  background-color: #0056b3;
}
</style>