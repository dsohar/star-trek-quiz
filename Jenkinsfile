@Library('my-shared-library') _

def APP_NAME = "star-trek-quiz"
def REPO = "dsohar"  // Replace with your DockerHub username
def APP_IMAGE = "docker.io/${REPO}/${appname}"
def APP_TAG = "2.2.${env.BUILD_NUMBER}"


podTemplate(cloud: 'kubernetes', containers: [
    containerTemplate(
        name: 'jnlp', 
        image: 'jenkins/inbound-agent:latest'
    ),
     containerTemplate(
        name: 'docker', 
        image: 'docker:26-dind', // Use the latest stable DinD image
        privileged: true,      // Essential for Docker daemon to run
        args: '--storage-driver=vfs' // VFS is safest for K8s, though slower
    ),
    containerTemplate(
        name: 'sonarqube',
        image: 'sonarsource/sonar-scanner-cli:latest'
    ),
    containerTemplate(
        name: 'deployer', 
        image: 'elevy99927/k8s-deployer:latest', 
        command: 'cat', 
        ttyEnabled: true
    ),
], 
volumes: [
    emptyDirVolume(mountPath: '/var/lib/docker', memory: false) // Q: Why do we need this volume?
    ]) {
    node(POD_LABEL) {
        stage('chackout') {
            container('jnlp') {
            sh '/usr/bin/git config --global http.sslVerify false'
	    checkout scm
          }
        } // end chackout

        stage('Building and Scanning in Parallel') {
            parallel(
                'Build Docker Image': {
                    stage('Build Docker Image') {
                        container('docker') {
                            echo "Building Docker image..."

                            dockerImage = docker.build(
                                "${APP_IMAGE}:${APP_TAG}",
                                "."
                            )
                            dockerImageLatest = docker.build(
                                "${APP_IMAGE}:latest",
                                "."
                            )
                        }
                    }
                },

                'Scan Docker Image': {
                    stage('Scan Code') {
                        container('sonarqube') {
                            echo "Scanning..."
                            script {
                                codeQuality.sonarCreateProject(env.APP_NAME)
                            }
                            script {
                                codeQuality.sonarLocalScan()
                            }
                        }
                    }
                }
            )
        }

        stage('Push to DockerHub') {
            container('docker') {
              script {
                docker.withRegistry('https://index.docker.io/v1/', 'dockerhub-creds') {
                    dockerImage.push()
                    dockerImageLatest.push()
                }
              }
            }
        } //end push

        stage('Deploy') {
            sh "echo helm template hello-newapp ./chart > hello-newapp.yaml"
        }
    }
}
