import axios from 'axios'

const api = axios.create({
  baseURL: '/api'
})

// Add token to requests if available
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Auth API
export const authAPI = {
  login: async (credentials) => {
    const formData = new FormData()
    formData.append('username', credentials.email)
    formData.append('password', credentials.password)
    const response = await api.post('/login', formData)
    return response.data
  },
  
  register: async (userData) => {
    const response = await api.post('/users/', userData)
    return response.data
  }
}

// Posts API
export const postsAPI = {
  getPosts: async (limit = 10, skip = 0, search = '') => {
    const response = await api.get('/posts/', {
      params: { limit, skip, search }
    })
    return response.data
  },
  
  getPost: async (id) => {
    const response = await api.get(`/posts/${id}`)
    return response.data
  },
  
  createPost: async (postData) => {
    const response = await api.post('/posts/', postData)
    return response.data
  },
  
  updatePost: async (id, postData) => {
    const response = await api.put(`/posts/${id}`, postData)
    return response.data
  },
  
  deletePost: async (id) => {
    const response = await api.delete(`/posts/${id}`)
    return response.data
  }
}

// Vote API
export const voteAPI = {
  vote: async (postId, dir) => {
    const response = await api.post('/vote/', {
      post_id: postId,
      dir: dir
    })
    return response.data
  }
}

export default api
