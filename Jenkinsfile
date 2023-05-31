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
        git(url: 'https://github.com/Ax-Projects/DealBot.git', branch: 'dockerfile')
      }
    }

    stage('install requirements') {
      steps {
        pysh(script: 'pip install --no-cache-dir -r requirements.txt', returnStatus: true, returnStdout: true)
      }
    }

    stage('run python script') {
      steps {
        pysh(script: 'main.py', returnStatus: true, returnStdout: true)
      }
    }
  }
}