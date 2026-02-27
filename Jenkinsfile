pipeline {
    agent any

    environment {
        IMAGE_NAME = "svarunbalaji2022bcs0152/wine-api:latest"
        CONTAINER_NAME = "wine_test_container"
        NETWORK_NAME = "lab7net"
    }

    stages {

        stage('Pull Image') {
            steps {
                sh 'docker pull $IMAGE_NAME'
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
                            def status = sh(
                                script: """
                                docker run --rm --network $NETWORK_NAME curlimages/curl:latest \
                                -s -o /dev/null -w '%{http_code}' \
                                http://$CONTAINER_NAME:8000/docs
                                """,
                                returnStdout: true
                            ).trim()

                            return (status == "200")
                        }
                    }
                }
            }
        }

        stage('Send Valid Inference Request') {
            steps {
                script {
                    def response = sh(
                        script: """
                        docker run --rm --network $NETWORK_NAME curlimages/curl:latest \
                        -s -X POST http://$CONTAINER_NAME:8000/predict \
                        -H "Content-Type: application/json" \
                        -d '{"fixed acidity":7.4,"volatile acidity":0.7,"citric acid":0,"residual sugar":1.9,"chlorides":0.076,"free sulfur dioxide":11,"total sulfur dioxide":34,"density":0.9978,"pH":3.51,"sulphates":0.56,"alcohol":9.4}'
                        """,
                        returnStdout: true
                    ).trim()

                    echo "Valid Response: ${response}"

                    if (!response.contains("prediction")) {
                        error("Prediction field missing in valid response")
                    }
                }
            }
        }

        stage('Send Invalid Request') {
            steps {
                script {
                    def status = sh(
                        script: """
                        docker run --rm --network $NETWORK_NAME curlimages/curl:latest \
                        -s -o /dev/null -w '%{http_code}' \
                        -X POST http://$CONTAINER_NAME:8000/predict \
                        -H "Content-Type: application/json" \
                        -d '{"invalid":123}'
                        """,
                        returnStdout: true
                    ).trim()

                    echo "Invalid Request Status: ${status}"

                    if (status == "200") {
                        error("Invalid request should not return 200")
                    }
                }
            }
        }

        stage('Stop Container') {
            steps {
                sh '''
                docker stop $CONTAINER_NAME || true
                docker rm $CONTAINER_NAME || true
                '''
            }
        }
    }

    post {
        success {
            echo "Pipeline PASSED  - Inference API is valid"
        }
        failure {
            echo "Pipeline FAILED - Inference validation failed"
        }
    }
}