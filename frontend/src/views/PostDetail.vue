<template>
  <div class="post-detail-container">
    <div v-if="loading" class="loading">Loading post...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    
    <div v-else-if="post" class="post-detail-card">
      <div class="post-header">
        <h1>{{ post.title }}</h1>
        <div class="post-meta">
          <span>by {{ post.owner?.email }}</span>
          <span>{{ formatDate(post.created_at) }}</span>
          <span class="status" :class="{ published: post.published }">
            {{ post.published ? 'Published' : 'Draft' }}
          </span>
        </div>
      </div>
      
      <div class="post-content">
        {{ post.content }}
      </div>
      
      <div class="post-footer">
        <div class="vote-section">
          <button 
            @click="handleVote(1)"
            class="vote-btn"
            :disabled="!isAuthenticated"
          >
            ▲
          </button>
          <span class="vote-count">{{ post.votes || 0 }} votes</span>
          <button 
            @click="handleVote(0)"
            class="vote-btn"
            :disabled="!isAuthenticated"
          >
            ▼
          </button>
        </div>
        
        <div v-if="voteError" class="error-message">{{ voteError }}</div>
        
        <div class="action-buttons">
          <router-link 
            v-if="canEdit"
            :to="`/post/${post.id}/edit`" 
            class="btn-edit"
          >
            Edit
          </router-link>
          <button 
            v-if="canEdit"
            @click="handleDelete" 
            :class="['btn-delete', { 'confirm-delete': showDeleteConfirm }]"
            :disabled="deleting"
          >
            {{ showDeleteConfirm ? 'Click again to confirm' : (deleting ? 'Deleting...' : 'Delete') }}
          </button>
          <button 
            v-if="canEdit && showDeleteConfirm"
            @click="showDeleteConfirm = false" 
            class="btn-cancel"
          >
            Cancel
          </button>
          <router-link to="/" class="btn-back">Back to Posts</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { postsAPI, voteAPI } from '../services/api'
import { jwtDecode } from 'jwt-decode'

export default {
  name: 'PostDetail',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const post = ref(null)
    const loading = ref(true)
    const deleting = ref(false)
    const error = ref('')
    const voteError = ref('')
    const showDeleteConfirm = ref(false)

    const isAuthenticated = computed(() => !!localStorage.getItem('token'))
    
    // Note: Client-side JWT decoding is only for UI convenience
    // The backend always validates tokens on each request for actual authorization
    const canEdit = computed(() => {
      if (!isAuthenticated.value || !post.value) return false
      
      try {
        const token = localStorage.getItem('token')
        const decoded = jwtDecode(token)
        return decoded.user_id === post.value.owner_id
      } catch {
        return false
      }
    })

    const fetchPost = async () => {
      try {
        loading.value = true
        const data = await postsAPI.getPost(route.params.id)
        post.value = data
        error.value = ''
      } catch (err) {
        error.value = err.response?.data?.detail || 'Failed to load post'
      } finally {
        loading.value = false
      }
    }

    const handleVote = async (dir) => {
      try {
        await voteAPI.vote(post.value.id, dir)
        await fetchPost() // Refresh post to update vote count
        voteError.value = ''
      } catch (err) {
        voteError.value = err.response?.data?.detail || 'Vote failed'
        setTimeout(() => {
          voteError.value = ''
        }, 3000)
      }
    }

    const handleDelete = async () => {
      if (!showDeleteConfirm.value) {
        showDeleteConfirm.value = true
        return
      }
      
      try {
        deleting.value = true
        await postsAPI.deletePost(post.value.id)
        router.push('/')
      } catch (err) {
        error.value = err.response?.data?.detail || 'Failed to delete post'
      } finally {
        deleting.value = false
        showDeleteConfirm.value = false
      }
    }

    const formatDate = (dateString) => {
      const date = new Date(dateString)
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }

    onMounted(() => {
      fetchPost()
    })

    return {
      post,
      loading,
      deleting,
      error,
      voteError,
      showDeleteConfirm,
      isAuthenticated,
      canEdit,
      handleVote,
      handleDelete,
      formatDate
    }
  }
}
</script>

<style scoped>
.post-detail-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
}

.loading, .error {
  text-align: center;
  padding: 40px;
  color: #666;
}

.error {
  color: #e74c3c;
}

.post-detail-card {
  background: white;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.post-header {
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #eee;
}

.post-header h1 {
  margin: 0 0 15px 0;
  color: #333;
}

.post-meta {
  display: flex;
  gap: 15px;
  color: #888;
  font-size: 14px;
}

.status {
  padding: 3px 10px;
  border-radius: 12px;
  background: #f5f5f5;
  font-size: 12px;
}

.status.published {
  background: #d4edda;
  color: #155724;
}

.post-content {
  font-size: 16px;
  line-height: 1.8;
  color: #555;
  white-space: pre-wrap;
  margin-bottom: 30px;
}

.post-footer {
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.vote-section {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
}

.error-message {
  color: #e74c3c;
  padding: 10px;
  margin: 10px 0;
  background: #fef2f2;
  border-radius: 4px;
  font-size: 14px;
}

.vote-btn {
  background: #f5f5f5;
  border: none;
  padding: 8px 15px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 18px;
  transition: all 0.3s;
}

.vote-btn:hover:not(:disabled) {
  background: #42b983;
  color: white;
}

.vote-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.vote-count {
  font-weight: bold;
  color: #333;
  min-width: 80px;
}

.action-buttons {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.btn-edit,
.btn-delete,
.btn-back {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
  text-decoration: none;
  display: inline-block;
}

.btn-edit {
  background: #42b983;
  color: white;
}

.btn-edit:hover {
  background: #35a372;
}

.btn-delete {
  background: #e74c3c;
  color: white;
}

.btn-delete:hover:not(:disabled) {
  background: #c0392b;
}

.btn-delete.confirm-delete {
  background: #c0392b;
  animation: pulse 0.5s ease-in-out;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

.btn-delete:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-cancel {
  background: #95a5a6;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-cancel:hover {
  background: #7f8c8d;
}

.btn-back {
  background: #f5f5f5;
  color: #666;
}

.btn-back:hover {
  background: #e5e5e5;
}
</style>
