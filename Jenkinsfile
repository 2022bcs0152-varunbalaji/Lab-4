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
                            def status = sh(
                                script: """
                                docker run --rm --network $NETWORK_NAME curlimages/curl:latest sh -lc \
                                "code=\$(curl -s -o /dev/null -w '%{http_code}' http://$CONTAINER_NAME:8000/health 2>/dev/null || true); echo \${code:-000}"
                                """,
                                returnStdout: true
                            ).trim()
                            if (status != "200") {
                                echo "Healthcheck HTTP status: ${status}"
                                sleep 2
                            }
                            return (status == "200")
                        }
                    }
                }
            }
        }

        stage('Send Valid Inference Request') {
            steps {
                script {
                    def output = sh(
                        script: """
                        docker run --rm --network $NETWORK_NAME -v \"$WORKSPACE\":/work curlimages/curl:latest \
                        -s -o - -w '\\n%{http_code}' \
                        -X POST http://$CONTAINER_NAME:8000/predict \
                        -H "Content-Type: application/json" \
                        -d "\$(cat /work/tests/valid.json)"
                        """,
                        returnStdout: true
                    ).trim()

                    def splitIndex = output.lastIndexOf("\n")
                    def body
                    def status
                    if (splitIndex >= 0) {
                        body = output.substring(0, splitIndex)
                        status = output.substring(splitIndex + 1)
                    } else {
                        def literalSepIndex = output.lastIndexOf("\\\\n")
                        body = (literalSepIndex >= 0) ? output.substring(0, literalSepIndex) : output
                        status = (literalSepIndex >= 0) ? output.substring(literalSepIndex + 2) : ""
                    }

                    echo "Valid Response Status: ${status}"
                    echo "Valid Response Body: ${body}"

                    if (status != "200") {
                        error("Valid request did not return 200")
                    }

                    if (!body.contains('"wine_quality"')) {
                        error("wine_quality field missing in valid response")
                    }
                }
            }
        }

        stage('Send Invalid Request') {
            steps {
                script {
                    def status = sh(
                        script: """
                        docker run --rm --network $NETWORK_NAME -v \"$WORKSPACE\":/work curlimages/curl:latest \
                        -s -o /dev/null -w '%{http_code}' \
                        -X POST http://$CONTAINER_NAME:8000/predict \
                        -H "Content-Type: application/json" \
                        -d "\$(cat /work/tests/invalid.json)"
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