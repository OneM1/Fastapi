<template>
  <div class="home">
    <div class="header">
      <h1>Posts</h1>
      <router-link v-if="isAuthenticated" to="/create" class="btn-create">
        Create Post
      </router-link>
    </div>

    <div class="search-bar">
      <input
        type="text"
        v-model="searchQuery"
        @input="handleSearch"
        placeholder="Search posts..."
      />
    </div>

    <div v-if="loading" class="loading">Loading posts...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    
    <div v-else class="posts-container">
      <div v-if="posts.length === 0" class="no-posts">
        No posts found. Create your first post!
      </div>
      
      <div v-for="post in posts" :key="post.id" class="post-card">
        <div class="post-header">
          <h3>
            <router-link :to="`/post/${post.id}`">{{ post.title }}</router-link>
          </h3>
          <span class="post-meta">
            by {{ post.owner.email }} • 
            {{ formatDate(post.created_at) }}
          </span>
        </div>
        
        <p class="post-content">{{ truncateContent(post.content) }}</p>
        
        <div class="post-footer">
          <div class="vote-section">
            <button 
              @click="handleVote(post.id, 1)"
              class="vote-btn"
              :class="{ active: post.userVoted }"
              :disabled="!isAuthenticated"
            >
              ▲
            </button>
            <span class="vote-count">{{ post.votes || 0 }}</span>
            <button 
              @click="handleVote(post.id, 0)"
              class="vote-btn"
              :disabled="!isAuthenticated"
            >
              ▼
            </button>
          </div>
          
          <router-link :to="`/post/${post.id}`" class="read-more">
            Read more
          </router-link>
        </div>
      </div>
    </div>

    <div v-if="posts.length > 0" class="pagination">
      <button 
        @click="loadMore" 
        :disabled="loadingMore"
        class="btn-load-more"
      >
        {{ loadingMore ? 'Loading...' : 'Load More' }}
      </button>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { postsAPI, voteAPI } from '../services/api'

export default {
  name: 'Home',
  setup() {
    const posts = ref([])
    const loading = ref(true)
    const loadingMore = ref(false)
    const error = ref('')
    const searchQuery = ref('')
    const skip = ref(0)
    const limit = 10

    const isAuthenticated = computed(() => !!localStorage.getItem('token'))

    const fetchPosts = async (append = false) => {
      try {
        if (append) {
          loadingMore.value = true
        } else {
          loading.value = true
        }
        
        const data = await postsAPI.getPosts(limit, skip.value, searchQuery.value)
        
        if (append) {
          posts.value = [...posts.value, ...data]
        } else {
          posts.value = data
        }
        
        error.value = ''
      } catch (err) {
        error.value = 'Failed to load posts'
      } finally {
        loading.value = false
        loadingMore.value = false
      }
    }

    const handleSearch = () => {
      skip.value = 0
      fetchPosts(false)
    }

    const loadMore = () => {
      skip.value += limit
      fetchPosts(true)
    }

    const handleVote = async (postId, dir) => {
      try {
        await voteAPI.vote(postId, dir)
        // Refresh posts to update vote count
        skip.value = 0
        await fetchPosts(false)
      } catch (err) {
        alert(err.response?.data?.detail || 'Vote failed')
      }
    }

    const truncateContent = (content) => {
      return content.length > 150 ? content.substring(0, 150) + '...' : content
    }

    const formatDate = (dateString) => {
      const date = new Date(dateString)
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      })
    }

    onMounted(() => {
      fetchPosts()
    })

    return {
      posts,
      loading,
      loadingMore,
      error,
      searchQuery,
      isAuthenticated,
      handleSearch,
      loadMore,
      handleVote,
      truncateContent,
      formatDate
    }
  }
}
</script>

<style scoped>
.home {
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

h1 {
  color: #333;
}

.btn-create {
  padding: 10px 20px;
  background: #42b983;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  font-weight: 500;
  transition: background 0.3s;
}

.btn-create:hover {
  background: #35a372;
}

.search-bar {
  margin-bottom: 30px;
}

.search-bar input {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
  box-sizing: border-box;
}

.search-bar input:focus {
  outline: none;
  border-color: #42b983;
}

.loading, .error, .no-posts {
  text-align: center;
  padding: 40px;
  color: #666;
}

.error {
  color: #e74c3c;
}

.posts-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.post-card {
  background: white;
  padding: 25px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s;
}

.post-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.post-header h3 {
  margin: 0 0 10px 0;
}

.post-header h3 a {
  color: #333;
  text-decoration: none;
}

.post-header h3 a:hover {
  color: #42b983;
}

.post-meta {
  color: #888;
  font-size: 14px;
}

.post-content {
  margin: 15px 0;
  color: #555;
  line-height: 1.6;
}

.post-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid #eee;
}

.vote-section {
  display: flex;
  align-items: center;
  gap: 10px;
}

.vote-btn {
  background: #f5f5f5;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
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

.vote-btn.active {
  background: #42b983;
  color: white;
}

.vote-count {
  font-weight: bold;
  color: #333;
  min-width: 30px;
  text-align: center;
}

.read-more {
  color: #42b983;
  text-decoration: none;
  font-weight: 500;
}

.read-more:hover {
  text-decoration: underline;
}

.pagination {
  text-align: center;
  margin-top: 30px;
}

.btn-load-more {
  padding: 12px 30px;
  background: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition: background 0.3s;
}

.btn-load-more:hover:not(:disabled) {
  background: #35a372;
}

.btn-load-more:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
