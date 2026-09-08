@Library('my-shared-library') _

def APP_NAME = "star-trek-quiz"
def REPO = "dsohar"  // Replace with your DockerHub username
def APP_IMAGE = "docker.io/${REPO}/${APP_NAME}"
def APP_TAG = "2.2.${env.BUILD_NUMBER}"
def dockerImage


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
    // containerTemplate(
    //     name: 'sonarqube',
    //     image: 'sonarqube:latest'
    // ),
    containerTemplate(
        name: 'deployer', 
        image: 'dsohar/devops-toolbox:latest', 
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
                        }
                    }
                },
                'Trivy Scan': {
                    stage('Trivy Image Scan') {
                        script {
                            def imageArchive = "${APP_NAME}-${env.BUILD_NUMBER}.tar"

                            try {
                                // The image exists inside the DinD Docker daemon.
                                container('docker') {
                                    sh """
                                        docker save \
                                            ${APP_IMAGE}:${APP_TAG} \
                                            -o ${imageArchive}
                                    """
                                }

                                // All containers in the Jenkins pod share the workspace,
                                // so the deployer container can read the archive.
                                container('deployer') {
                                    sh """
                                        trivy image \
                                            --input ${imageArchive} \
                                            --severity HIGH,CRITICAL \
                                            --no-progress \
                                            --exit-code 0
                                    """
                                }
                            } finally {
                                sh "rm -f ${imageArchive}"
                            }
                        }
                    }
                }
            )
        }

        stage('Push to DockerHub') {
            container('docker') {
                docker.withRegistry('https://index.docker.io/v1/', 'dockerhub-creds') {
                    dockerImage.push()
                    dockerImage.push('latest')
                }
            }
        } //end push

        stage('Deploy') {
            sh "helm template ${APP_NAME} ./chart > ${APP_NAME}.yaml"
        }
    }
}
