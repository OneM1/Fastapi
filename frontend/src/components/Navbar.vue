<template>
  <nav class="navbar">
    <div class="nav-container">
      <router-link to="/" class="logo">
        <span class="logo-icon">📝</span>
        FastAPI Blog
      </router-link>
      
      <div class="nav-menu">
        <router-link to="/" class="nav-link">Home</router-link>
        
        <template v-if="isAuthenticated">
          <router-link to="/create" class="nav-link">Create Post</router-link>
          <button @click="handleLogout" class="btn-logout">Logout</button>
        </template>
        
        <template v-else>
          <router-link to="/login" class="nav-link">Login</router-link>
          <router-link to="/register" class="nav-link btn-register">Register</router-link>
        </template>
      </div>
    </div>
  </nav>
</template>

<script>
import { computed } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'Navbar',
  setup() {
    const router = useRouter()
    const isAuthenticated = computed(() => !!localStorage.getItem('token'))

    const handleLogout = () => {
      localStorage.removeItem('token')
      router.push('/login')
    }

    return {
      isAuthenticated,
      handleLogout
    }
  }
}
</script>

<style scoped>
.navbar {
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 15px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-size: 24px;
  font-weight: bold;
  color: #42b983;
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 10px;
}

.logo-icon {
  font-size: 28px;
}

.nav-menu {
  display: flex;
  align-items: center;
  gap: 20px;
}

.nav-link {
  color: #555;
  text-decoration: none;
  font-weight: 500;
  padding: 8px 16px;
  border-radius: 4px;
  transition: all 0.3s;
}

.nav-link:hover {
  color: #42b983;
  background: #f5f5f5;
}

.nav-link.router-link-active {
  color: #42b983;
}

.btn-register {
  background: #42b983;
  color: white !important;
}

.btn-register:hover {
  background: #35a372;
}

.btn-logout {
  background: #e74c3c;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.3s;
}

.btn-logout:hover {
  background: #c0392b;
}

@media (max-width: 768px) {
  .nav-container {
    flex-direction: column;
    gap: 15px;
  }
  
  .nav-menu {
    flex-wrap: wrap;
    justify-content: center;
  }
}
</style>
