import Vue from 'vue'
import Router from 'vue-router'
import DashboardLayout from '@/layout/DashboardLayout'
import AuthLayout from '@/layout/AuthLayout'
Vue.use(Router)

export default new Router({
  linkExactActiveClass: 'active',
  routes: [
    {
      path: '/',
      redirect: 'Pacientes',
      component: DashboardLayout,
      children: [
        {
          path: '/Pacientes',
          name: 'Pacientes',
          // route level code-splitting
          // this generates a separate chunk (about.[hash].js) for this route
          // which is lazy-loaded when the route is visited.
          component: () => import(/* webpackChunkName: "demo" */ './views/Pacientes.vue')
        },
        {
          path: '/Perfil/:foo',
          name: 'Perfil',
          component: () => import(/* webpackChunkName: "demo" */ './views/Perfil.vue')
        },
        {
          path: '/Perfil',
          name: 'Perfil',
          component: () => import(/* webpackChunkName: "demo" */ './views/Perfil.vue')
        },
        
        
      ]
    },
    {
      path: '/Landing',
      name: 'landing',
      component: () => import(/* webpackChunkName: "demo" */ './views/Landing.vue')
    }

  ]
})
