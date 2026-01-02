# FastAPI Task Manager API - Complete CI/CD Pipeline

A production-ready REST API built with FastAPI demonstrating modern DevOps practices with automated CI/CD pipeline.

## 🚀 Features

- ✅ **FastAPI** - Modern, fast Python web framework
- ✅ **Automated CI/CD** - GitHub Actions pipeline
- ✅ **Docker** - Containerized deployment
- ✅ **Comprehensive Testing** - 100% test coverage with pytest
- ✅ **Code Quality** - Automated linting with flake8
- ✅ **Security Scanning** - Trivy vulnerability scanning
- ✅ **Interactive API Docs** - Auto-generated Swagger UI
- ✅ **Health Checks** - Built-in monitoring endpoints

## 📚 API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔧 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root endpoint |
| GET | `/health` | Health check |
| GET | `/tasks` | Get all tasks |
| GET | `/tasks/{id}` | Get specific task |
| POST | `/tasks` | Create new task |
| PUT | `/tasks/{id}` | Update task |
| DELETE | `/tasks/{id}` | Delete task |
| GET | `/tasks/stats/summary` | Get statistics |

## 🏃 Quick Start

### Run Locally with Python:
```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload

# Access API at http://localhost:8000
# Docs at http://localhost:8000/docs
```

### Run with Docker:
```bash
# Build image
docker build -t fastapi-task-api .

# Run container
docker run -p 8000:8000 fastapi-task-api

# Access API at http://localhost:8000
```

### Run Tests:
```bash
# Run all tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=app --cov-report=term-missing
```

## 🔄 CI/CD Pipeline

The pipeline runs automatically on every push and includes:

1. **Lint Stage** - Code quality checks with flake8
2. **Test Stage** - Unit tests with coverage reporting
3. **Build Stage** - Docker image build and testing
4. **Security Stage** - Vulnerability scanning with Trivy

View pipeline status: [![CI Pipeline](https://github.com/YOUR_USERNAME/fastapi-task-api-ci/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_USERNAME/fastapi-task-api-ci/actions)

## 🧪 Testing the API
```bash
# Health check
curl http://localhost:8000/health

# Create a task
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"My First Task","description":"Complete DevOps project"}'

# Get all tasks
curl http://localhost:8000/tasks

# Get statistics
curl http://localhost:8000/tasks/stats/summary
```

## 🛠️ Tech Stack

- **Framework**: FastAPI 0.109+
- **Server**: Uvicorn
- **Testing**: pytest, httpx
- **Containerization**: Docker
- **CI/CD**: GitHub Actions
- **Code Quality**: flake8
- **Security**: Trivy

## 📊 Project Structure
```
fastapi-task-api-ci/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application
│   └── models.py        # Pydantic models
├── tests/
│   ├── __init__.py
│   └── test_api.py      # Comprehensive tests
├── .github/
│   └── workflows/
│       └── ci.yml       # CI/CD pipeline
├── Dockerfile           # Container configuration
├── requirements.txt     # Python dependencies
└── README.md
```

## 🎯 DevOps Best Practices Demonstrated

- ✅ Automated testing with high coverage
- ✅ Code quality enforcement
- ✅ Containerization with multi-stage builds
- ✅ Health check endpoints
- ✅ Security vulnerability scanning
- ✅ Pipeline caching for faster builds
- ✅ Comprehensive documentation

## 👨‍💻 Author

**Soumya Ranjan Pratap**
- Email: srpratap05@gmail.com
- LinkedIn: [linkedin.com/in/soumya-ranjan-pratap](https://linkedin.com/in/soumya-ranjan-pratap)
- GitHub: [github.com/soumya-ranjan-pratap](https://github.com/soumya-ranjan-pratap)

## 📝 License

This project is open source and available under the MIT License.