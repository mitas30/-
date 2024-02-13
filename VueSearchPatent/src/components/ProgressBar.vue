<script setup>
import { ref,computed } from 'vue';

const props=defineProps({
    progress_data: {type: Number,default:0}
})

const progressWidth=computed(()=>{
    return `${props.progress_data}%`
})
</script>

<template>
  <br/>
    <div class="progress-container">
      <div class="progress-bar" v-bind:style="{ width: progressWidth }"></div>
    </div>
</template>

<style scoped>
.progress-container {
  width: 35%; /* コンテナの幅をフル幅に変更 */
  background-color: #eee; /* 背景色を設定 */
  border-radius: 10px; /* 角を丸くする */
  height: 10%;
}

.progress-bar {
  height: 100%; /* プログレスバーの高さを設定 */
  background-color: rgb(6, 143, 6); /* プログレスバーの色を設定 */
  transition: width 0.5s ease; /* 幅の変更にアニメーションを適用 */
  border-radius: 10px; /* 角を丸くする */
}
</style>