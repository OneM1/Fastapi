# FastAPI Blog - Vue.js Frontend

A modern, responsive Vue.js frontend for the FastAPI blog backend.

## Features

- **Authentication**: User registration and login with JWT tokens
- **Post Management**: Create, read, update, and delete blog posts
- **Voting System**: Upvote and downvote posts
- **Search**: Search posts by title
- **Responsive Design**: Mobile-friendly interface

## Tech Stack

- Vue.js 3 with Composition API
- Vue Router for navigation
- Axios for API calls
- Vite for fast development and building

## Setup

### Prerequisites

- Node.js (v14 or higher)
- npm or yarn
- FastAPI backend running on port 8000

### Installation

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

### Building for Production

```bash
npm run build
```

The built files will be in the `dist` directory.

## API Configuration

The frontend is configured to proxy API requests to `http://localhost:8000`. 

If your backend is running on a different port or domain, update the proxy configuration in `vite.config.js`:

```javascript
server: {
  proxy: {
    '/api': {
      target: 'http://your-backend-url:port',
      changeOrigin: true,
      rewrite: (path) => path.replace(/^\/api/, '')
    }
  }
}
```

## Usage

### For Users

1. **Register**: Create a new account at `/register`
2. **Login**: Sign in at `/login`
3. **Browse Posts**: View all posts on the home page
4. **Create Post**: Click "Create Post" (requires authentication)
5. **Vote**: Use the up/down arrows to vote on posts
6. **View Post**: Click on any post to see full details
7. **Edit/Delete**: Post owners can edit or delete their posts

### Authentication

The app uses JWT tokens stored in localStorage. Tokens are automatically included in API requests via Axios interceptors.

Protected routes:
- `/create` - Create new post
- `/post/:id/edit` - Edit post

## Project Structure

```
frontend/
├── public/           # Static assets
├── src/
│   ├── components/   # Reusable Vue components
│   │   └── Navbar.vue
│   ├── router/       # Vue Router configuration
│   │   └── index.js
│   ├── services/     # API service layer
│   │   └── api.js
│   ├── views/        # Page components
│   │   ├── Home.vue
│   │   ├── Login.vue
│   │   ├── Register.vue
│   │   ├── CreatePost.vue
│   │   ├── EditPost.vue
│   │   └── PostDetail.vue
│   ├── App.vue       # Root component
│   ├── main.js       # Application entry point
│   └── style.css     # Global styles
├── index.html        # HTML entry point
├── vite.config.js    # Vite configuration
└── package.json      # Dependencies and scripts
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build locally

## Features Detail

### Home Page
- Lists all posts with pagination
- Search functionality
- Vote on posts
- Quick preview of post content

### Authentication
- Secure login/register forms
- Form validation
- Error handling
- Automatic redirect after login

### Post Management
- Rich post creation form
- Edit existing posts
- Delete posts (with confirmation)
- Draft/Published status toggle

### Voting
- Upvote/downvote posts
- Real-time vote count updates
- Authentication required for voting

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the [MIT License](LICENSE).
