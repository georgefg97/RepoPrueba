<template>
    <v-app>
      <v-main>
        <v-container fluid class="register-background fill-height d-flex align-center justify-center">
          <v-card
            class="pa-6 glass-card"
            max-width="460"
            elevation="15"
          >
            <v-card-title class="text-h5 font-weight-bold text-center">Crea tu cuenta en Subasteitor</v-card-title>
            <v-card-subtitle class="text-center mb-4">Y comienza a pujar por lo mejor 🎯</v-card-subtitle>
  
            <v-form ref="form" v-model="formValido" lazy-validation>
              <v-text-field
                v-model="nombre"
                :rules="[v => !!v || 'El nombre es requerido']"
                label="Nombre completo"
                prepend-inner-icon="mdi-account"
                variant="outlined"
                density="comfortable"
              />
              <v-text-field
                v-model="email"
                :rules="[v => /.+@.+\..+/.test(v) || 'Ingresa un email válido']"
                label="Correo electrónico"
                prepend-inner-icon="mdi-email"
                variant="outlined"
                density="comfortable"
              />
              <v-text-field
                v-model="password"
                :type="mostrarPassword ? 'text' : 'password'"
                :append-inner-icon="mostrarPassword ? 'mdi-eye-off' : 'mdi-eye'"
                @click:append-inner="mostrarPassword = !mostrarPassword"
                :rules="[v => v.length >= 6 || 'Mínimo 6 caracteres']"
                label="Contraseña"
                prepend-inner-icon="mdi-lock"
                variant="outlined"
                density="comfortable"
              />
            </v-form>
  
            <v-card-actions class="justify-center mt-4">
              <v-btn
                :disabled="!formValido"
                color="primary"
                class="rounded-pill px-8"
                size="large"
                @click="registrarse"
              >
                Registrarme
              </v-btn>
            </v-card-actions>
  
            <v-card-subtitle class="text-center mt-4">
              ¿Ya tienes cuenta?
              <RouterLink to="/login" class="text-decoration-underline text-primary">Inicia sesión</RouterLink>
            </v-card-subtitle>
          </v-card>
        </v-container>
      </v-main>
    </v-app>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'
  import api from '../services/api'
  
  const router = useRouter()
  const form = ref(null)
  const formValido = ref(false)
  
  const nombre = ref('')
  const email = ref('')
  const password = ref('')
  const mostrarPassword = ref(false)
  
  const registrarse = async () => {
    if (!(await form.value.validate())) return
  
    try {
      const body = {
        nombre: nombre.value,
        email: email.value,
        password: password.value,
      }
  
      await api.post('/register', body)
      alert('🎉 ¡Cuenta creada con éxito!')
      router.push('/login')
    } catch (err) {
      console.error(err)
      alert('❌ No se pudo crear la cuenta. Verifica los datos.')
    }
  }
  </script>
  
  <style scoped>
  .register-background {
    background-image: linear-gradient(
        rgba(0, 0, 0, 0.4),
        rgba(0, 0, 0, 0.4)
      ),
      url('https://images.unsplash.com/photo-1556742400-b5d6bfa9d86b');
    background-size: cover;
    background-position: center;
    filter: brightness(0.95);
  }
  
  .glass-card {
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(10px);
    border-radius: 20px;
  }
  </style>
  