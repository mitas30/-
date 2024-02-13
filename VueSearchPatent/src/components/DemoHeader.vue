<script setup>
defineProps({
  msg: {
    type: String,
    required: true
  }
})
</script>

<template>
  <div class="header">
    <h1>{{ msg }}</h1>
    <p>--LLMを使ったキーワード抽出とキーワード一致数による検索--</p>
  </div>
</template>

<style scoped>
.header {
  text-align: center; /* テキストを中央揃えに */
  padding: 20px;
  background-color: #333; /* ヘッダーの背景色 */
  color: #fff; /* ヘッダーの文字色 */
}
.green {
  color: #4CAF50; /* タイトルの色 */
}
</style>

