<script setup>
import { RouterView,useRoute } from 'vue-router'
import {ref,watch} from 'vue'
import DemoHeader from './components/DemoHeader.vue'
import ProgressBar from './components/ProgressBar.vue';
import FormInstruction from './components/FormInstruction.vue'
const progress_per = ref(0);
const show_input_components=ref(true);
const route=useRoute();

watch(route, (to, from) => {
  // ルート変更時に実行されるロジック
  updateProgress(to);
});

function updateProgress(toRoute) {
  switch (toRoute.path) {
    case '/step2':
      progress_per.value = 25;
      break;
    case '/step3':
      progress_per.value = 50;
      break;
    case '/step4':
      progress_per.value = 75;
      break;
    case '/waiting':
      show_input_components.value=false;
      break;
    default:
      break;
  }
}
</script>

<template>
  <div class="app-container">
    <header>
      <DemoHeader msg="特許検索のデモ" />
    </header>
    <FormInstruction v-if="show_input_components"/>
    <main class="content-wrapper">
      <RouterView />
    </main>
    <div class="bar">
      <ProgressBar v-if="show_input_components" :progress_data="progress_per"/>
    </div>
  </div>
</template>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  height: 100vh; /* 画面の高さ全体を使用 */
}

.content-wrapper {
  flex-grow: 1; /* コンテンツ領域が残りのスペースを埋めるように */
  display: flex;
  justify-content: center; /* 中央揃え */
  align-items: center; /* 垂直方向も中央揃え */
}
.bar{
  display: flex;
  margin-bottom: 10%;
  justify-content: center; /* 中央揃え */
}
</style>
