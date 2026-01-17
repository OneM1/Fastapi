<template>
  <div class="edit-post-container">
    <div v-if="loading" class="loading">Loading post...</div>
    <div v-else-if="loadError" class="error">{{ loadError }}</div>
    
    <div v-else class="edit-post-card">
      <h2>Edit Post</h2>
      
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="title">Title</label>
          <input
            type="text"
            id="title"
            v-model="title"
            required
            placeholder="Enter post title"
          />
        </div>
        
        <div class="form-group">
          <label for="content">Content</label>
          <textarea
            id="content"
            v-model="content"
            required
            rows="10"
            placeholder="Write your post content..."
          ></textarea>
        </div>
        
        <div class="form-group checkbox-group">
          <label>
            <input
              type="checkbox"
              v-model="published"
            />
            Published
          </label>
        </div>
        
        <div v-if="error" class="error">{{ error }}</div>
        
        <div class="button-group">
          <button type="submit" class="btn-primary" :disabled="saving">
            {{ saving ? 'Saving...' : 'Save Changes' }}
          </button>
          <router-link :to="`/post/${$route.params.id}`" class="btn-secondary">
            Cancel
          </router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { postsAPI } from '../services/api'

export default {
  name: 'EditPost',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const title = ref('')
    const content = ref('')
    const published = ref(true)
    const loading = ref(true)
    const saving = ref(false)
    const loadError = ref('')
    const error = ref('')

    const fetchPost = async () => {
      try {
        loading.value = true
        const data = await postsAPI.getPost(route.params.id)
        title.value = data.title
        content.value = data.content
        published.value = data.published
        loadError.value = ''
      } catch (err) {
        loadError.value = err.response?.data?.detail || 'Failed to load post'
      } finally {
        loading.value = false
      }
    }

    const handleSubmit = async () => {
      error.value = ''
      saving.value = true
      
      try {
        await postsAPI.updatePost(route.params.id, {
          title: title.value,
          content: content.value,
          published: published.value
        })
        
        router.push(`/post/${route.params.id}`)
      } catch (err) {
        error.value = err.response?.data?.detail || 'Failed to update post'
      } finally {
        saving.value = false
      }
    }

    onMounted(() => {
      fetchPost()
    })

    return {
      title,
      content,
      published,
      loading,
      saving,
      loadError,
      error,
      handleSubmit
    }
  }
}
</script>

<style scoped>
.edit-post-container {
  max-width: 800px;
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

.edit-post-card {
  background: white;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

h2 {
  margin-bottom: 30px;
  color: #333;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 5px;
  color: #555;
  font-weight: 500;
}

input[type="text"],
textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  box-sizing: border-box;
  font-family: inherit;
}

input:focus,
textarea:focus {
  outline: none;
  border-color: #42b983;
}

.checkbox-group label {
  display: flex;
  align-items: center;
  font-weight: normal;
  cursor: pointer;
}

.checkbox-group input[type="checkbox"] {
  width: auto;
  margin-right: 8px;
  cursor: pointer;
}

.button-group {
  display: flex;
  gap: 10px;
}

.btn-primary,
.btn-secondary {
  padding: 12px 24px;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
  text-decoration: none;
  display: inline-block;
  text-align: center;
}

.btn-primary {
  background: #42b983;
  color: white;
  flex: 1;
}

.btn-primary:hover:not(:disabled) {
  background: #35a372;
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-secondary {
  background: #f5f5f5;
  color: #666;
  padding: 12px 24px;
}

.btn-secondary:hover {
  background: #e5e5e5;
}
</style>
