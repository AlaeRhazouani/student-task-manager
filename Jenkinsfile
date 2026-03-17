pipeline {
    agent any
    
    environment {
        BACKEND_IMAGE = "ghcr.io/alaerhazouani/student-task-manager-backend"
        FRONTEND_IMAGE = "ghcr.io/alaerhazouani/student-task-manager-frontend"
        DB_IMAGE = "ghcr.io/alaerhazouani/student-task-manager-db"
        CREDS = credentials('ghcr-token')
        DISCORD_WEBHOOK = credentials('discord-webhook')
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
                sh "docker build --no-cache -t ${BACKEND_IMAGE}:${BUILD_NUMBER} ./backend"
                sh "docker build --no-cache -t  ${FRONTEND_IMAGE}:${BUILD_NUMBER} ./frontend"
                sh "docker build --no-cache -t ${DB_IMAGE}:${BUILD_NUMBER} ./database"
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
                        BUILD_NUMBER=${BUILD_NUMBER} docker compose -f docker-compose.prod.yml pull &&
                        BUILD_NUMBER=${BUILD_NUMBER} docker compose -f docker-compose.prod.yml up -d --force-recreate
                    '"""
                }
            }
        }
        stage('Health Check') {
            steps {
                sleep 5
                sh 'curl -f  http://84.8.216.164:3000/health'
                sh 'curl -f  http://84.8.216.164:5000/health'
            }
            post {
                failure {
                    script {
                        int prevBuild = BUILD_NUMBER.toInteger() - 1
                        sshagent(['server-ssh-key']) {
                            sh """ssh -o StrictHostKeyChecking=no ubuntu@84.8.216.164 '
                            cd /home/ubuntu/app &&
                            BUILD_NUMBER=${prevBuild} docker compose -f docker-compose.prod.yml pull &&
                            BUILD_NUMBER=${prevBuild} docker compose -f docker-compose.prod.yml up -d --force-recreate
                            '"""
                        }
                    }
                    
                }
            }
        }
    }
    
    post {
        success {
            sh 'curl -X POST $DISCORD_WEBHOOK -H "Content-Type: application/json" -d \'{"content":" Deploy succeeded! Build #\'$BUILD_NUMBER\'"}\''
        }
        failure {
            sh 'curl -X POST $DISCORD_WEBHOOK -H "Content-Type: application/json" -d \'{"content":" Build #\'$BUILD_NUMBER\' FAILED!"}\''
        }
    }
}   