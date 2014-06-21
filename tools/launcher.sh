#!/bin/sh
JAVA_HOME=/opt/java CATALINA_OPTS="-DJENKINS_HOME=/opt/jenkins -Xmx512m" /home/jenkins/tomcat/apache-tomcat-7.0.39/bin/catalina.sh start