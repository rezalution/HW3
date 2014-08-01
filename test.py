import subprocess

proc = subprocess.Popen("php /calEvents.php", shell=True, stdout=subprocess.PIPE)
script_response = proc.stdout.read()