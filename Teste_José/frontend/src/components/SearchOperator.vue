<template>
    <div>
      <input v-model="searchTerm" placeholder="Buscar operadora..." @keyup.enter="buscar">
      <button @click="buscar">Buscar</button>
      <ul>
        <li v-for="(item, index) in results" :key="index">{{ item.Nome }}</li>
      </ul>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    data() {
      return {
        searchTerm: "",
        results: []
      };
    },
    methods: {
      async buscar() {
        try {
          const response = await axios.get(`http://127.0.0.1:8000/buscar?termo=${this.searchTerm}`);
          this.results = response.data;
        } catch (error) {
          console.error("Erro na busca", error);
        }
      }
    }
  };
  </script>
  
  <style scoped>
  input { margin-right: 10px; }
  </style>
  