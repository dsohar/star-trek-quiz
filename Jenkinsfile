@Library('my-shared-library') _

pipeline {
    agent any
    environment {
        APP_NAME = 'star-trek-quiz'
        MAJOR_VERSION = 2.1
    }
    stages {
        stage('Building and Scanning in Parallel') {
            parallel {
                stage('Build Docker Image') {
                    steps {
                        script {
                            dockerLibrary.buildDockerImage('main')
                        }
                    }
                }
                stage('Scan Docker Image') {
                    steps {
                        script {
                            codeQuality.sonarCreateProject(env.APP_NAME)
                        }
                    }
                }
            }
        }
        stage('Push to DockerHub') {
            steps {
                script{
                    dockerLibrary.pushToDockerHub()
                }
            }
        }
        stage('Run Docker Image') {
            steps {
                script {
                    dockerLibrary.runDockerImage()
                }
            }
        }
        stage('Health Check') {
            steps {
                script{
                    starTrekQuizLibrary.healthCheck()
                }
            }
        }
    }
    post {
        always {
            script {
                dockerLibrary.removeDockerImage()
            }
        }

        failure {
            script {
                generalLibrary.failureMessage()
            }
        }

        success {
            script {
                generalLibrary.successMessage()
            }
        }
    }
}