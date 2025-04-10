<template>
    <v-container>
        <v-card class="pa-4">
            <v-toolbar color="primary" dense>
                <v-toolbar-title>Dashboard - Mis Charlas</v-toolbar-title>
                <v-spacer></v-spacer>
                <v-btn color="red" dark @click="logout">Cerrar Sesión</v-btn>
            </v-toolbar>

            <v-card-title class="text-h5 mt-4">Charlas Registradas</v-card-title>

            <v-data-table 
                :headers="[ 
                    { text: 'Título', value: 'titulo' },
                    { text: 'Orador', value: 'orador' },
                    { text: 'Fecha Fin', value: 'fecha_fin' },
                    { text: 'Acciones', value: 'acciones' }
                ]"
                :items="charlasRegistradas"
                class="mt-4"
            >
                <template v-slot:item.acciones="{ item }">
                    <v-btn v-if="charlaTerminada(item.fecha_fin)" color="green" @click="evaluarCharla(item.charla_id)">
                        Evaluar
                    </v-btn>
                    <v-btn color="red" class="ml-2" @click="eliminarEvaluacion(item.charla_id)">
                        Eliminar Evaluación
                    </v-btn>
                </template>
            </v-data-table>
        </v-card>
    </v-container>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";
import { jwtDecode } from "jwt-decode";

const charlasRegistradas = ref([]);
const usuarioId = ref(null);
const router = useRouter();

// 📌 Obtener el `usuario_id` desde el token JWT
onMounted(async () => {
    try {
        const token = localStorage.getItem("token");
        if (!token) {
            alert("No estás autenticado ❌");
            router.push("/login");
            return;
        }

        const decoded = jwtDecode(token);
        console.log("🔍 Token decodificado:", decoded);

        // 📌 Obtener usuario_id desde el backend
        const responseUsuario = await axios.get(`http://127.0.0.1:5002/usuarios/email/${decoded.sub}`);
        usuarioId.value = responseUsuario.data.usuario_id;
        console.log("📌 Usuario ID obtenido:", usuarioId.value);

        // 📌 Obtener las charlas registradas por el usuario
        console.log("📡 Haciendo petición a /asistencias/usuario/", usuarioId.value);
        const responseCharlas = await axios.get(`http://127.0.0.1:5002/asistencias/usuario/${usuarioId.value}`);

        console.log("📌 Respuesta del backend (charlas registradas):", responseCharlas.data);

        if (!Array.isArray(responseCharlas.data) || responseCharlas.data.length === 0) {
            console.warn("⚠️ No hay charlas registradas.");
            charlasRegistradas.value = [];
            return;
        }

        // ✅ Asegurar que se asignen correctamente
        charlasRegistradas.value = responseCharlas.data;

        console.log("✅ Charlas registradas asignadas en Vue:", charlasRegistradas.value);

    } catch (error) {
        console.error("❌ Error al obtener datos:", error);
        alert("Hubo un problema al obtener las charlas ❌");
    }
});

// 📌 Función para verificar si la charla ya terminó
const charlaTerminada = (fechaFin) => {
    return new Date(fechaFin) < new Date();
};

// 📌 Función para redirigir a la evaluación
const evaluarCharla = (charlaId) => {
    router.push(`/evaluacion/${charlaId}`);
};

// 📌 Función para eliminar la eval de un charl
const eliminarEvaluacion = async (charlaId) => {
    try {
        await axios.delete(`http://127.0.0.1:5002/evaluaciones/usuario/${usuarioId.value}/charla/${charlaId}`);
        alert("✅ Evaluación eliminada correctamente.");
        // No eliminamos la charla de la lista porque la evaluación no borra la inscripción
    } catch (error) {
        console.error("❌ Error al eliminar evaluación:", error);
        alert("Error al eliminar la evaluación ❌");
    }
};


// 📌 Función para cerrar sesión
const logout = () => {
    localStorage.removeItem("token");
    alert("Sesión cerrada ✅");
    router.push("/login");
};
</script>
