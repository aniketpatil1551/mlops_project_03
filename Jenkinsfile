pipeline {
    agent any

    triggers {
        githubPush()  // This triggers the pipeline on GitHub push event
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm  // Checkout source code from GitHub
            }
        }

        stage('Show Git Commit Info') {
            steps {
                sh '''
                echo "📦 Getting latest commit info..."

                # Show commit hash
                echo "🔢 Commit Hash:"
                git log -1 --pretty=format:'%H'

                # Show author
                echo "👤 Author:"
                git log -1 --pretty=format:'%an <%ae>'

                # Show commit message
                echo "📝 Commit Message:"
                git log -1 --pretty=format:'%s'

                # Show full commit message body
                echo "🧾 Full Commit Body:"
                git log -1 --pretty=format:'%B'

                # Show list of changed files (A = Added, M = Modified, D = Deleted)
                echo "📄 Files Changed in Commit:"
                git diff-tree --no-commit-id --name-status -r HEAD
                '''
            }
        }
    }
}
