<script setup>
import { useRouter } from 'vue-router';
import {ref} from 'vue'; 
import axios from 'axios';

const router = useRouter();
const form = ref({
  ideaSummary: '',
});

const submitForm = async() => {
  try{
    await axios.post('http://localhost:5000/api/set_info/abstract', {
      abstract:form.value.ideaSummary});
    router.push('/step3');
  }catch(error){
    console.error('There was an error submitting the form:', error);
  }
};
</script>

<template>
  <div class="form-container">
    <h1>Step2:アイデアの概要を教えてください</h1>
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label for="ideaSummary">アイデアの概要</label>
        <textarea id="ideaSummary" v-model="form.ideaSummary"
          placeholder="「クリーンエア・アーバンシールド」は、都市部の大気汚染問題に対応するために開発された画期的な発明です。このシステムは、建物の外壁や都市インフラに設置されることを想定しており、空気清浄技術を活用して周辺の大気を浄化します。具体的には、汚染物質を吸収し、フィルターを通してクリーンな空気を放出することで、都市部の空気質を改善します。
このシステムは、特に交通量の多い地域や工業地域において有効であり、大気中の有害物質を削減することで、市民の健康リスクを軽減します。さらに、クリーンエア・アーバンシールドは、エネルギー効率の高い方法で運用され、環境への負荷も最小限に抑えられています。
また、このシステムのデザインは、都市景観に溶け込むよう工夫されており、美観を損なうことなく都市部の空気質を改善することができます。究極の目標は、都市部の生活環境を改善し、すべての市民がクリーンで健康的な空気を呼吸できるようにすることです。"></textarea>
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