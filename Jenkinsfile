pipeline {
    agent any

    environment {
        IMAGE_NAME = "svarunbalaji2022bcs0152/wine-api:latest"
        CONTAINER_NAME = "wine_test_container"
        NETWORK_NAME = "lab7net"
    }

    stages {

        stage('Build Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME .'
            }
        }

        stage('Create Network') {
            steps {
                sh 'docker network create $NETWORK_NAME || true'
            }
        }

        stage('Run Container') {
            steps {
                sh '''
                docker rm -f $CONTAINER_NAME || true
                docker run -d --network $NETWORK_NAME --name $CONTAINER_NAME $IMAGE_NAME
                '''
            }
        }

        stage('Wait for Service Readiness') {
            steps {
                script {
                    timeout(time: 60, unit: 'SECONDS') {
                        waitUntil {
                            def rc = sh(
                                script: 'docker run --rm --network $NETWORK_NAME curlimages/curl:latest -sf -o /dev/null http://$CONTAINER_NAME:8000/health',
                                returnStatus: true
                            )
                            if (rc != 0) {
                                echo "Healthcheck not ready yet (rc=${rc}), retrying..."
                                sleep 2
                            }
                            return (rc == 0)
                        }
                    }
                }
            }
        }

        stage('Send Valid Inference Request') {
            steps {
                script {
                    def response = sh(
                        script: '''
                        docker run --rm --user root --network $NETWORK_NAME \
                        -v "$WORKSPACE":/work \
                        curlimages/curl:latest \
                        -s -X POST http://$CONTAINER_NAME:8000/predict \
                        -H "Content-Type: application/json" \
                        -d @/work/tests/valid.json
                        ''',
                        returnStdout: true
                    ).trim()

                    echo "Valid Response: ${response}"

                    if (!response.contains('"wine_quality"')) {
                        error("wine_quality field missing in valid response")
                    }
                }
            }
        }

        stage('Send Invalid Request') {
            steps {
                script {
                    def rc = sh(
                        script: '''
                        docker run --rm --user root --network $NETWORK_NAME \
                        -v "$WORKSPACE":/work \
                        curlimages/curl:latest \
                        -s -f -o /dev/null \
                        -X POST http://$CONTAINER_NAME:8000/predict \
                        -H "Content-Type: application/json" \
                        -d @/work/tests/invalid.json
                        ''',
                        returnStatus: true
                    )

                    echo "Invalid Request exit code: ${rc}"

                    if (rc == 0) {
                        error("Invalid request should not succeed")
                    }
                }
            }
        }
    }

    post {
        always {
            sh '''
            docker stop $CONTAINER_NAME || true
            docker rm -f $CONTAINER_NAME || true
            '''
        }
        success {
            echo "Pipeline PASSED  - Inference API is valid"
        }
        failure {
            echo "Pipeline FAILED - Inference validation failed"
        }
    }
}