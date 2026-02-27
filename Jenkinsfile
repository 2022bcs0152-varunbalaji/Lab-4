pipeline {
    agent any

    environment {
        IMAGE_NAME = "svarunbalaji2022bcs0152/wine-api:latest"
        CONTAINER_NAME = "wine_test_container"
        PORT = "8000"
    }

    stages {

        stage('Pull Image') {
            steps {
                sh 'docker pull $IMAGE_NAME'
            }
        }

        stage('Run Container') {
            steps {
                sh '''
                docker rm -f $CONTAINER_NAME || true
                docker run -d --name $CONTAINER_NAME $IMAGE_NAME
                '''
            }
        }

        stage('Wait for Service Readiness') {
            steps {
                script {
                    timeout(time: 60, unit: 'SECONDS') {
                        waitUntil {
                            def status = sh(
                                script: "docker exec $CONTAINER_NAME curl -s -o /dev/null -w '%{http_code}' http://localhost:8000/docs",
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
                        script: "docker exec $CONTAINER_NAME curl -s -X POST http://localhost:8000/predict -H 'Content-Type: application/json' -d @tests/valid.json",
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
                        script: "docker exec $CONTAINER_NAME curl -s -o /dev/null -w '%{http_code}' -X POST http://localhost:8000/predict -H 'Content-Type: application/json' -d @tests/invalid.json",
                        returnStdout: true
                    ).trim()

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
            echo "Pipeline PASSED "
        }
        failure {
            echo "Pipeline FAILED "
        }
    }
}