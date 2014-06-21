
import paramiko 

host = 'localhost'
user = 'demo'
pw = 'demo'
command = 'ls -la'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, username=user, password=pw)

print 'running remote command: %s' % command

stdin, stdout, stderr = ssh.exec_command(command)
stdin.close()
print '---- out ----'
print stdout.read()
print '---- error ----'
print stderr.read()

ssh.close()
print 'connection to %s closed' % host
