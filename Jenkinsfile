
pipeline {
    agent any

    options {
        disableConcurrentBuilds()
    }

    environment {
        IMAGE_NAME = "kishorebandaru002/multibranch-flask-app"
        GIT_USER   = "Kishorebandaru002"
        GIT_EMAIL  = "Kishorebandaru002@gmail.com"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build and Push Image') {
            when { branch 'main' }
            steps {
                script {
                    // Tag each build uniquely
                    env.IMAGE_TAG = "build-${BUILD_NUMBER}"

                    withCredentials([
                        usernamePassword(
                            credentialsId: 'dockerhub-cred',
                            usernameVariable: 'DOCKER_USER',
                            passwordVariable: 'DOCKER_PASS'
                        )
                    ]) {
                        sh """
                            set -e
                            docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                            echo "${DOCKER_PASS}" | docker login -u "${DOCKER_USER}" --password-stdin
                            docker push ${IMAGE_NAME}:${IMAGE_TAG}
                        """
                    }
                }
            }
        }

        stage('Update K8s Manifest') {
            when { branch 'main' }
            steps {
                script {
                    withCredentials([
                        usernamePassword(
                            credentialsId: 'github-cred',
                            usernameVariable: 'GIT_USERNAME',
                            passwordVariable: 'GIT_TOKEN'
                        )
                    ]) {
                        sh """
                            set -e
                            git config user.name "${GIT_USER}"
                            git config user.email "${GIT_EMAIL}"

                            git fetch origin
                            git checkout main
                            git reset --hard origin/main

                            # Update only the image line in the deployment manifest
                            sed -i 's|^\\s*image:\\s*.*$|        image: ${IMAGE_NAME}:${IMAGE_TAG}|' k8s/deployment.yml

                            git add k8s/deployment.yml
                            git diff --cached --quiet || git commit -m "Updated image to ${IMAGE_TAG}"
                            git push https://${GIT_USERNAME}:${GIT_TOKEN}@github.com/Kishorebandaru002/Multi-Branch-Prod.git main
                        """
                    }
                }
            }
        }
    }
}


