import { createRouter, createWebHistory } from 'vue-router'
import Step1 from '../components/InputIdeaName.vue'
import Step2 from '../components/InputAbstract.vue';
import Step3 from '../components/InputTech.vue';
import Step4 from '../components/InputSolveWay.vue';
import Waiting from '../components/Waiting.vue';
import Display from '../components/DisplayResult.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', component: Step1},
    { path: '/step2', component: Step2 },
    { path: '/step3', component: Step3 },
    { path: '/step4', component: Step4 },
    { path: '/waiting', component: Waiting},
    { path: '/display', component: Display},
  ]
})

export default router;
