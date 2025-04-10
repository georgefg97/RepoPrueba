<template>
    <v-container>
      <v-row justify="center">
        <v-col cols="12" md="8">
          <v-card elevation="6" class="pa-4">
            <v-card-title class="text-h5">{{ auction?.titulo }}</v-card-title>
            <v-card-subtitle>
              <div>Tipo: {{ auction?.tipo }}</div>
              <div>Estado: {{ auction?.estado }}</div>
            </v-card-subtitle>
  
            <v-card-text>
              <p><strong>Descripción:</strong> {{ auction?.descripcion }}</p>
              <p><strong>Precio actual:</strong> {{ auction?.precio_actual }} Bs</p>
              <p><strong>Fecha de cierre:</strong> {{ auction?.fecha_fin || 'No especificada' }}</p>
            </v-card-text>
  
            <v-divider class="my-4" />
  
            <!-- Sección para pujar -->
            <v-card-text>
              <v-text-field
                v-model="monto"
                label="Tu oferta (Bs)"
                type="number"
                prepend-icon="mdi-cash"
              />
              <v-btn color="primary" @click="pujar">Enviar puja</v-btn>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { useRoute } from 'vue-router'
  import api from '../services/api'
  
  const route = useRoute()
  const auction = ref(null)
  const monto = ref(0)
  
  const fetchAuction = async () => {
    try {
      const res = await api.get(`/auctions/${route.params.id}`)
      auction.value = res.data
    } catch (err) {
      console.error('Error cargando subasta:', err)
    }
  }
  
  const pujar = async () => {
    try {
      const body = {
        subasta_id: auction.value.id,
        monto: parseFloat(monto.value),
      }
      await api.post('/bids', body)
      alert('¡Puja realizada con éxito!')
      fetchAuction() // recarga los datos por si cambió el precio
    } catch (err) {
      console.error('Error al pujar:', err)
      alert('No se pudo realizar la puja. Revisa los requisitos.')
    }
  }
  
  onMounted(() => {
    fetchAuction()
  })
  </script>
  