pipeline {
  agent {
    node {
      label 'rpi4'
    }
    // environment {
    //     WORKSPACE = ''
    // }

  }
  stages {
    stage('git clone') {
      steps {
        git(url: 'https://github.com/Ax-Projects/DealBot.git', branch: 'query-list')
      }
    }

    stage('install requirements') {
      steps {
        sh """
        
        """
        pysh(script: 'pip install -r requirements.txt', returnStatus: true, returnStdout: true)
      }
    }

    stage('run python script') {
      steps {
        pysh(script: 'main.py', returnStatus: true, returnStdout: true)
      }
    }
  }
}