pipeline {
  agent {
    node {
      label 'rpi4'
    }

  }
  stages {
    stage('git clone') {
      steps {
        git(url: 'https://github.com/Ax-Projects/DealBot.git', branch: 'query-list')
      }
    }

    stage('run python script') {
      steps {
        pysh(script: 'main.py', returnStatus: true, returnStdout: true)
      }
    }

  }
}