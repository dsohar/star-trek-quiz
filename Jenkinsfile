pipeline {
    agent any
    environment {
        APP_NAME = 'star-trek-quiz'
        TAG = '2.0.${env.BUILD_NUMBER}'
    }
    stages {
        stage('Build Docker Image') {
            steps {
                echo "Building ${env.APP_NAME}"
                echo "Build Number: ${env.BUILD_NUMBER}"
                echo "Tag: ${env.TAG}"
                sh "docker build -t ${env.APP_NAME}:${env.TAG} ."
            }
        }
        stage('Push to DockerHub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-dsohar', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                    echo "Deploying with username ${env.USERNAME}"
                    sh "docker login -u ${env.USERNAME} -p ${env.PASSWORD}"
                    sh "docker tag ${env.APP_NAME}:${env.TAG} ${env.DOCKER_HUB_LOCATION}/${env.USERNAME}:${env.TAG}"
                }
            }
        }
    }
}