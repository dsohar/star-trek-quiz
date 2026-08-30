pipeline {
    agent any
    environment {
        APP_NAME = 'star-trek-quiz'
    }
    stages {
        stage('Build') {
            steps {
                echo "Building ${env.APP_NAME}"
                echo "Build Number: ${env.BUILD_NUMBER}"
                sh docker build -t "${env.APP_NAME}:${env.BUILD_NUMBER}" .
            }
        }
        stage('Test') {
            steps {
                echo 'Testing...'
                // Test steps here
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying...'
                // Deploy steps here
            }
        }
    }
}