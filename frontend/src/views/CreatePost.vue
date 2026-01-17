<template>
  <div class="create-post-container">
    <div class="create-post-card">
      <h2>Create New Post</h2>
      
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
            Publish immediately
          </label>
        </div>
        
        <div v-if="error" class="error">{{ error }}</div>
        
        <div class="button-group">
          <button type="submit" class="btn-primary" :disabled="loading">
            {{ loading ? 'Creating...' : 'Create Post' }}
          </button>
          <router-link to="/" class="btn-secondary">Cancel</router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { postsAPI } from '../services/api'

export default {
  name: 'CreatePost',
  setup() {
    const router = useRouter()
    const title = ref('')
    const content = ref('')
    const published = ref(true)
    const error = ref('')
    const loading = ref(false)

    const handleSubmit = async () => {
      error.value = ''
      loading.value = true
      
      try {
        await postsAPI.createPost({
          title: title.value,
          content: content.value,
          published: published.value
        })
        
        router.push('/')
      } catch (err) {
        error.value = err.response?.data?.detail || 'Failed to create post'
      } finally {
        loading.value = false
      }
    }

    return {
      title,
      content,
      published,
      error,
      loading,
      handleSubmit
    }
  }
}
</script>

<style scoped>
.create-post-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.create-post-card {
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

.error {
  color: #e74c3c;
  padding: 10px;
  margin-bottom: 15px;
  background: #fef2f2;
  border-radius: 4px;
  font-size: 14px;
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
