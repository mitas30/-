<script setup>
import { onMounted,ref } from 'vue';
import { useRouter } from 'vue-router';
import { io } from 'socket.io-client';
import ProgressBar from './ProgressBar.vue';

const state=ref(0)

onMounted(() => {
  const socket = io('http://localhost:5000');
  const router = useRouter();

  socket.on('connect', () => {
    // ここで start_search イベントを発火
    socket.emit('start_search');
    state.value = 10;
  });

  socket.on('convert_complete', data => {
    console.log(data.message);
    state.value = 30;
  });

  socket.on('search_complete', data => {
    console.log(data.message);
    state.value = 80;
  });

  socket.on('response_ready', () => {
    state.value = 100;
    router.push('/display');
  });
});
</script>

<template>
    <div class="waiting-screen">
      <h1>処理中です...</h1>
      <p>特許の検索と取得処理を行っています。これは数十秒かかる場合がありますので、しばらくお待ちください。</p>
      <progress-bar :progress_data="state" />
      <div class="engagement-content">
        <p>ご存知ですか？特許申請の平均審査期間は約2年です。</p>
      </div>
    </div>
  </template>
  
  <style scoped>
  .waiting-screen {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
    text-align: center;
  }  
  
  .engagement-content {
    margin-top: 30px;
  }
  </style>