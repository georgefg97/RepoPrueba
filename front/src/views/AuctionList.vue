<template>
    <v-container>
      <v-row>
        <v-col cols="12">
          <h1 class="text-h4">Subastas Disponibles</h1>
        </v-col>
  
        <v-col v-for="auction in auctions" :key="auction.id" cols="12" md="4">
          <v-card class="mx-auto" max-width="400">
            <v-card-title>{{ auction.titulo }}</v-card-title>
            <v-card-subtitle>Tipo: {{ auction.tipo }} | Estado: {{ auction.estado }}</v-card-subtitle>
            <v-card-text>
              <p>{{ auction.descripcion }}</p>
              <p><strong>Precio actual:</strong> {{ auction.precio_actual }} Bs</p>
            </v-card-text>
            <v-card-actions>
              <v-btn :to="`/auctions/${auction.id}`" color="primary" text>Ver más</v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import api from '../services/api'
  
  const auctions = ref([]);
  
  onMounted(async () => {
    try {
      const res = await api.get('/auctions'); // ⚠️ Asegúrate de que esta ruta sea correcta
      auctions.value = res.data.items || res.data; // Adaptar según tu respuesta
    } catch (error) {
      console.error('Error al cargar subastas:', error);
    }
  });
  </script>
  