pipeline {
    agent any

    environment {
        JIRA_URL = "https://lokedaasa-1766131983831.atlassian.net"
        ISSUE_KEY = "HDFC Banking"
    }

    stages {
        stage('Build') {
            steps {
                echo 'Build successful'
            }
        }

        stage('Close Jira Ticket') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'jira-creds',
                    usernameVariable: 'JIRA_USER',
                    passwordVariable: 'JIRA_TOKEN'
                )]) {
                    sh """
                    curl -X POST \
                    --url ${JIRA_URL}/rest/api/3/issue/${ISSUE_KEY}/transitions \
                    --user ${JIRA_USER}:${JIRA_TOKEN} \
                    -H "Content-Type: application/json" \
                    --data '{
                      "transition": {
                        "id": "31"
                      }
                    }'
                    """
                }
            }
        }
    }
}
