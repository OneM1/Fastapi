# FastAPI Blog Application

A full-stack blog application with a FastAPI backend and Vue.js frontend.

## Features

### Backend (FastAPI)
- RESTful API with FastAPI
- JWT-based authentication
- PostgreSQL database with SQLModel ORM
- User management (CRUD operations)
- Post management (CRUD operations)
- Voting system (upvote/downvote)
- Database migrations with Alembic

### Frontend (Vue.js)
- Modern Vue.js 3 with Composition API
- Responsive design
- User authentication (register/login)
- Post management interface
- Voting functionality
- Search posts
- Real-time updates

## Project Structure

```
.
├── app/                    # FastAPI backend
│   ├── routers/           # API route handlers
│   │   ├── auth.py       # Authentication endpoints
│   │   ├── post.py       # Post endpoints
│   │   ├── user.py       # User endpoints
│   │   └── vote.py       # Voting endpoints
│   ├── main.py           # FastAPI app initialization
│   ├── models.py         # Database models
│   ├── schemes.py        # Pydantic schemas
│   ├── database.py       # Database connection
│   ├── config.py         # Configuration settings
│   ├── auth2.py          # JWT authentication logic
│   └── utils.py          # Utility functions
├── frontend/             # Vue.js frontend
│   ├── src/
│   │   ├── components/   # Vue components
│   │   ├── views/        # Page views
│   │   ├── router/       # Router configuration
│   │   └── services/     # API services
│   └── ...
├── alembic/              # Database migrations
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js 14+
- PostgreSQL database
- pip and npm

### Backend Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd Fastapi
```

2. Create a virtual environment:
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory with the following:
```
DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
DATABASE_NAME=fastapi_db
DATABASE_USERNAME=your_username_here
DATABASE_PASSWORD=your_password_here
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

5. Run database migrations:
```bash
alembic upgrade head
```

6. Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

API documentation: `http://localhost:8000/docs`

### Frontend Setup

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

## API Endpoints

### Authentication
- `POST /login` - User login

### Users
- `POST /users/` - Create user (register)
- `GET /users/` - Get all users
- `GET /users/{id}` - Get user by ID
- `PUT /users/{id}` - Update user
- `DELETE /users/{id}` - Delete user

### Posts
- `GET /posts/` - Get all posts (with pagination and search)
- `POST /posts/` - Create post (authenticated)
- `GET /posts/{id}` - Get post by ID
- `PUT /posts/{id}` - Update post (authenticated, owner only)
- `DELETE /posts/{id}` - Delete post (authenticated, owner only)

### Votes
- `POST /vote/` - Vote on a post (authenticated)
  - `dir: 1` to upvote
  - `dir: 0` to remove vote/downvote

## Usage

1. Start the backend server (port 8000)
2. Start the frontend server (port 5173)
3. Open `http://localhost:5173` in your browser
4. Register a new account
5. Create, view, and vote on posts!

## Development

### Backend
- Framework: FastAPI
- ORM: SQLModel
- Database: PostgreSQL
- Authentication: JWT (PyJWT)
- Password Hashing: bcrypt

### Frontend
- Framework: Vue.js 3
- Build Tool: Vite
- HTTP Client: Axios
- Routing: Vue Router
- State: Composition API (ref, computed)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Branch Protection

This repository uses branch protection rules to maintain code quality and prevent accidental changes. Please see [BRANCH_PROTECTION.md](BRANCH_PROTECTION.md) for details on:
- How branch protection is configured
- How to apply protection rules
- Working with protected branches
- Creating pull requests

## License

This project is open source and available under the MIT License.
