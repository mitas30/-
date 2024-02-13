<script setup>
import { useRouter } from 'vue-router';
import { ref }from 'vue';
import axios from 'axios';

const router = useRouter();

const form=ref({
  usingtech:'',
});

const submitForm = async() => {
  try{
    await axios.post('http://localhost:5000/api/set_info/tech', {
      tech: form.value.usingtech
    });
    router.push('/step4');
  }catch(error){
    console.error('There was an error submitting the form:', error);
  }
};
</script>

<template>
  <div class="form-container">
    <h1>Step3:使用するテクノロジーを記述してください</h1>
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label for="ideaSummary">使用するテクノロジー</label>
        <textarea id="ideaSummary" v-model="form.usingtech"
        placeholder="高度なHEPAフィルター：これらのフィルターは、大気中の微小粒子物質（PM2.5やPM10など）を効率的に捕捉し、除去します。また、大気中の有害な化学物質やアレルゲンもフィルターする能力を持っています。

活性炭フィルター：活性炭は、その高い吸着性能により、有害なガスや臭気を吸収するのに適しています。これにより、大気からNOxやSOxなどの有害な化学物質を除去することができます。

光触媒コーティング：このコーティングは、太陽光や人工光源の下で活性化し、大気中の有害物質を無害な物質に分解します。この技術は、維持費が低く、自己清浄能力を持っているため、メンテナンスの手間を軽減します。

エネルギー効率の良い設計：システムは省エネ設計に基づいており、必要最小限の電力で動作します。太陽光発電パネルなどの再生可能エネルギー源と組み合わせることで、その持続可能性をさらに高めることが可能です。

スマートモニタリングシステム：大気の質をリアルタイムで監視し、汚染レベルに応じて清浄システムの動作を調整します。これにより、効率的かつ効果的に大気汚染を管理することができます。"></textarea>
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