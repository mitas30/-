<script setup>
import { useRouter } from 'vue-router';
import { ref } from 'vue';
import axios from 'axios';

const form = ref({
  ideaName: '',
  problem: ''
});
const router = useRouter();
const submitForm = async() => {
  try{
    await axios.post('http://localhost:5000/api/set_info/idea_and_problem', {
      "idea":form.value.ideaName,
      "problem": form.value.problem
    });
    router.push('/step2');
  }catch(error){
    console.error('There was an error submitting the form:', error);
  }
};
</script>

<template>
  <FormInstruction />
  <div class="form-container">
    <h1>Step1:アイデアと、そのアイデアが解決できる問題を教えてください</h1>
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label for="ideaName">アイデアの名称</label>
        <input type="text" id="ideaName" v-model="form.ideaName" placeholder="クリーンエア・アーバンシールド">
      </div>
      <div class="form-group">
        <label for="problemSolves">そのアイデアが解決する問題</label>
        <textarea id="problemSolves" v-model="form.problem" placeholder="都市部の大気汚染による健康リスクの軽減"></textarea>
      </div>
      <button type="submit">Next</button>
    </form>
  </div>
</template>


<style scoped>
form{
  height: 65%;
  margin:auto 5%;
}
.form-container {
  width: 55%; /* 最大幅を調整 */
  margin: 40px auto; /* 上下のマージンを増やして中央揃え */
  padding: 20px; /* パディングを調整 */
  border: 1px solid #ccc; /* 枠線を追加 */
  border-radius: 8px; /* 角を丸くする */
  background-color: #f9f9f9; /* 背景色をわずかにオフホワイトに */
}

.form-group {
  margin-bottom: 20px; /* フォームグループの下マージンを増やす */
}

label {
  display: block;
  margin-bottom: 5px;
}

input[type="text"],
textarea {
  width: 95%;
  padding: 10px;
  margin-bottom: 10px;
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

