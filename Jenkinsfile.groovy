#!/usr/bin/env groovy Jenkinsfile

pipeline {
    agent any
    stages {
        stage('Example') {
            steps { 
                echo 'Hello World'
            }
        }
    }
}