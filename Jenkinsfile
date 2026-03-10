pipeline {
    agent any
    
    environment {
        BACKEND_IMAGE = "ghcr.io/alaerhazouani/student-task-manager-backend"
        FRONTEND_IMAGE = "ghcr.io/alaerhazouani/student-task-manager-frontend"
        DB_IMAGE = "ghcr.io/alaerhazouani/student-task-manager-db"
        CREDS = credentials('ghcr-token')
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Test') {
            steps {
                sh 'cd backend && pip3 install -r requirements.txt && python3 -m pytest tests/'
            }
        }
        stage('Build') {
            steps {
                sh "docker build -t ${BACKEND_IMAGE}:${BUILD_NUMBER} ./backend"
                sh "docker build -t ${FRONTEND_IMAGE}:${BUILD_NUMBER} ./frontend"
                sh "docker build -t ${DB_IMAGE}:${BUILD_NUMBER} ./database"
            }
        }
        stage('Push') {
            steps {
                sh '''echo $CREDS_PSW | docker login ghcr.io -u $CREDS_USR --password-stdin'''
                sh "docker push ${BACKEND_IMAGE}:${BUILD_NUMBER}"
                sh "docker push ${FRONTEND_IMAGE}:${BUILD_NUMBER}"
                sh "docker push ${DB_IMAGE}:${BUILD_NUMBER}"
            }
        }
        stage('Deploy') {
            steps {
                sshagent(['server-ssh-key']) {
                    sh """ssh -o StrictHostKeyChecking=no ubuntu@84.8.216.164 '
                        cd /home/ubuntu/app &&
                        sed -i "s|:latest|:${BUILD_NUMBER}|g" docker-compose.prod.yml &&
                        docker compose -f docker-compose.prod.yml pull &&
                        docker compose -f docker-compose.prod.yml up -d
                    '"""
                }
            }
        }
    }
    
    post {
        success {
            echo 'Pipeline succeeded !'
        }
        failure {
            echo 'Pipeline failed !'
        }
    }
}   