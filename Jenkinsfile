pipeline {
    agent any
    
    environment {
        BACKEND_IMAGE = "ghcr.io/alaerhazouani/student-task-manager-backend"
        FRONTEND_IMAGE = "ghcr.io/alaerhazouani/student-task-manager-frontend"
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
            }
        }
        stage('Push') {
            steps {
                sh '''echo $CREDS_PSW | docker login ghcr.io -u $CREDS_USR --password-stdin'''
                sh "docker push ${BACKEND_IMAGE}:${BUILD_NUMBER}"
                sh "docker push ${FRONTEND_IMAGE}:${BUILD_NUMBER}"
            }
        }
        stage('Deploy') {
            steps {
                sshagent(['server-ssh-key']) {
                    sh '''ssh -o StrictHostKeyChecking=no ubuntu@84.8.216.164 "
                        cd /home/ubuntu/app &&
                        docker compose pull &&
                        docker compose up -d
                    "'''
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