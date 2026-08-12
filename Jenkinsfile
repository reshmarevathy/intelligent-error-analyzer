pipeline {
    agent any

    stages {
        stage('Backend Check') {
            steps {
                sh 'python3 -m pip install -r backend/requirements.txt'
                sh 'python3 -m py_compile backend/main.py'
            }
        }

        stage('Frontend Build') {
            steps {
                sh 'cd frontend && npm install'
                sh 'cd frontend && npm run build'
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t intelligent-error-analyzer-backend backend'
                sh 'docker build -t intelligent-error-analyzer-frontend frontend'
            }
        }
    }
}