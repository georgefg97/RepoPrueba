import { createRouter, createWebHistory } from 'vue-router'

import Login from './views/Login.vue'
import Register from './views/Register.vue'
import Dashboard from './views/Dashboard.vue'
import AuctionList from './views/AuctionList.vue'
import AuctionDetail from './views/AuctionDetail.vue'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/dashboard', component: Dashboard },
  { path: '/auctions', component: AuctionList },
  { path: '/auctions/:id', component: AuctionDetail, props: true },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
