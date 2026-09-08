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
    emptyDirVolume(mountPath: '/var/lib/docker', memory: false)
    ]) {
    node(POD_LABEL) {
        stage('chackout') {
            container('jnlp') {
            sh '/usr/bin/git config --global http.sslVerify false'
	    checkout scm
          }
        } // end chackout

        stage('Build Docker Image') {
            container('docker') {
                script {
                    dockerImage = docker.build(
                        "${APP_IMAGE}:${APP_TAG}",
                        "."
                    )

                    // Confirm that the image now exists
                    sh "docker image inspect ${APP_IMAGE}:${APP_TAG}"
                }
            }
        }

        stage('Trivy Image Scan') {
            script {
                def imageArchive = "${APP_NAME}-${env.BUILD_NUMBER}.tar"

                try {
                    container('docker') {
                        sh """
                            docker save \
                                ${APP_IMAGE}:${APP_TAG} \
                                -o ${imageArchive}
                        """
                    }

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
        // stage('SonarCube Scan') {
        //     container('deployer') {
        //         script {
        //             codeQuality.sonarCreateProject(APP_NAME)
        //         }
        //     }
        //     container('jnlp') {
        //         script {
        //             codeQuality.sonarLocalScan()
        //         }
        //     }
        // }
        stage('Push to DockerHub') {
            container('docker') {
                docker.withRegistry('https://index.docker.io/v1/', 'dockerhub-creds') {
                    dockerImage.push()
                    dockerImage.push('latest')
                }
            }
        } //end push

        stage('Deploy with HELM') {
            container('deployer') {
                sh """
                    helm lint ./helmchart

                    helm upgrade --install ${APP_NAME} ./helmchart \
                        --namespace default \
                        --set image.repository=${REPO} \
                        --set image.tag=${APP_TAG} \
                        --wait \
                        --timeout 5m

                    kubectl get deployments
                    kubectl get pods
                    kubectl get services
                """
            }
        }
    }
}
