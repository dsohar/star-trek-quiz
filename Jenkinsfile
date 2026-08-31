pipeline {
    agent any
    environment {
        APP_NAME = 'star-trek-quiz'
    }
    stages {
        stage('Building and Scanning in Parallel') {
            parallel {
                stage('Build Docker Image') {
                    steps {
                        echo "Building ${env.APP_NAME}"
                        echo "Build Number: ${env.BUILD_NUMBER}"
                        echo "Tag: ${env.TAG}"
                        sh "docker build -t ${env.APP_NAME}:2.1.${env.BUILD_NUMBER} ."
                    }
                }
                stage('Scan') {
                    steps {
                        echo "Scanning ${env.APP_NAME}:2.1.${env.BUILD_NUMBER}"
                    }
                }
            }
        }
        stage('Push to DockerHub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-dsohar', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                    echo "Deploying with username ${env.USERNAME}"
                    sh "docker login -u ${env.USERNAME} -p ${env.PASSWORD}"
                    sh "docker tag ${env.APP_NAME}:2.1.${env.BUILD_NUMBER} ${env.USERNAME}/${env.APP_NAME}:2.1.${env.BUILD_NUMBER}"
                    sh "docker tag ${env.APP_NAME}:2.1.${env.BUILD_NUMBER} ${env.USERNAME}/${env.APP_NAME}:latest"
                    sh "docker push ${env.USERNAME}/${env.APP_NAME}:2.1.${env.BUILD_NUMBER}"
                    sh "docker push ${env.USERNAME}/${env.APP_NAME}:latest"
                }
            }
        }
    }
    post {
        failure {
            echo 'The pipeline failed!'
        }
        success {
            echo 'The pipeline finished successfully!'
        }
    }
}