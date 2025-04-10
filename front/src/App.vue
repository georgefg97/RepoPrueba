<script setup>
import { ref, onMounted, computed } from "vue";
import { useRouter } from "vue-router";

const token = ref(localStorage.getItem("token"));
const router = useRouter();

const isAuthenticated = computed(() => !!token.value);

const logout = () => {
  token.value = null;
  localStorage.removeItem("token");
  alert("Sesión cerrada ✅");
  router.push("/login");
};

onMounted(() => {
  token.value = localStorage.getItem("token");
});
</script>

<template>
  <v-app>
    <v-container>
      <v-toolbar color="primary" dense>
        <v-btn to="/login" text>Login</v-btn>
        <v-btn v-if="isAuthenticated" to="/dashboard" text>Dashboard</v-btn>
        <v-btn v-if="isAuthenticated" @click="logout" text>Cerrar Sesión</v-btn>
      </v-toolbar>

      <v-main>
        <router-view />
      </v-main>
    </v-container>
  </v-app>
</template>
