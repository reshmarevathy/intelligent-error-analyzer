pipeline {
    agent any

    stages {

        stage('Backend Check') {
            steps {
                bat 'python -m pip install -r backend\\requirements.txt'
                bat 'python -m py_compile backend\\main.py'
            }
        }

        stage('Frontend Build') {
            steps {
                bat 'cd frontend && npm install'
                bat 'cd frontend && npm run build'
            }
        }

        stage('Docker Build') {
            steps {
                bat 'docker build -t intelligent-error-analyzer-backend backend'
                bat 'docker build -t intelligent-error-analyzer-frontend frontend'
            }
        }
    }
}