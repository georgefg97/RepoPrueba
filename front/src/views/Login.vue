<template>
  <v-app>
    <v-main>
      <v-container fluid class="login-background fill-height d-flex align-center justify-center">
        <v-card
          class="pa-6"
          max-width="420"
          elevation="12"
          style="background-color: rgba(255, 255, 255, 0.95); border-radius: 20px"
        >
          <v-card-title class="justify-center text-h5 font-weight-bold mb-2">
            Bienvenido a Subasteitor
          </v-card-title>
          <v-card-subtitle class="text-center mb-4">
            Inicia sesión para acceder a las subastas
          </v-card-subtitle>

          <v-card-text>
            <v-text-field
              v-model="email"
              label="Correo electrónico"
              prepend-inner-icon="mdi-email-outline"
              variant="outlined"
              density="comfortable"
            />
            <v-text-field
              v-model="password"
              label="Contraseña"
              type="password"
              prepend-inner-icon="mdi-lock-outline"
              variant="outlined"
              density="comfortable"
            />
          </v-card-text>

          <v-card-actions class="justify-center mt-2">
            <v-btn color="primary" class="rounded-pill px-6" size="large" @click="login">
              Entrar
            </v-btn>
          </v-card-actions>

          <v-card-subtitle class="text-center mt-4">
            ¿No tienes cuenta?
            <RouterLink to="/register" class="text-decoration-underline text-primary">Regístrate aquí</RouterLink>
          </v-card-subtitle>
        </v-card>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import api from '../services/api';

const email = ref('');
const password = ref('');
const router = useRouter();

const login = async () => {
  try {
    const form = new URLSearchParams();
    form.append('username', email.value);
    form.append('password', password.value);

    const res = await api.post('/token', form, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    });

    localStorage.setItem('token', res.data.access_token);
    router.push('/dashboard');
  } catch (error) {
    alert('❌ Credenciales incorrectas o error en el servidor.');
    console.error(error);
  }
};
</script>

<style scoped>
.login-background {
  background-image: url('https://laculturasocial.com/wp-content/uploads/2023/06/Casas-de-subastas-en-Barcelona.jpg');
  background-size: cover;
  background-position: center;
  filter: brightness(0.95);
}
</style>
