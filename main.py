from flask import Flask, request, jsonify

"""
    Commands to run:
        cat /etc/os-release
        uname -r
        hostname
        lscpu
        df -h
        free -h
        ifconfig
"""

app = Flask(__name__)

@app.route("/getsysteminfo")
def getSystemInfo():

    from subprocess import run

    os = eval(run(['cat', '/etc/os-release'], capture_output=True, text=True).stdout.split("\n")[0].split("=")[1])
    kernel = run(['uname', '-r'], capture_output=True, text=True).stdout.strip()
    hostname = run(['hostname'], capture_output=True, text=True).stdout.strip()

    c = run(['lscpu'], capture_output=True, text=True).stdout.split("\n")
    cpu = ""
    for i in c:
        if "Model name" in i:
            cpu = i.split("  ")[-1]
            break

    disk_info = run(['df', '-h'], capture_output=True, text=True).stdout.split("\n")
    labels = disk_info.pop(0).split(" ")
    labels = list(filter(None, labels))
    labels[-1] = labels[-2] + " " + labels.pop()
    for k, i in enumerate(disk_info[:-1]):
        fs = {}
        for ind, j in enumerate(list(filter(None, i.split(" ")))):
            fs[labels[ind]] = j
        disk_info[k] = fs
    disk_info.pop()
    
    for i, j in enumerate(disk_info):
        if j["Mounted on"] == "/":
            disk_info.insert(0, disk_info.pop(i))

    ram_memory = list(filter(None, run(['free'], capture_output=True, text=True).stdout.split("\n")[1].split(" ")))
    ram_info = {"used": ram_memory[2], "free": ram_memory[3], "buff": ram_memory[5], "total": ram_memory[1]}

    networks = [list(filter(None, i.split(" "))) for i in run(['ifconfig'], capture_output=True, text=True).stdout.split("\n\n")[:-1]]

    for ind, i in enumerate(networks):
        d = {}
        for j in range(0, len(i)-1, 2):
            if j == 0:
                d["interface"] = i[j]
            else:
                d[i[j]] = i[j+1]
        networks[ind] = d


    data = {
            "os":os,
            "kernel":kernel,
            "hostname":hostname,
            "cpu":cpu,
            "disk_info":disk_info,
            "ram_info": ram_info,
            "networks_info": networks
            }
    extra = request.args.get('extra')
    if extra:
        data['extra'] = extra
    
    response = jsonify(data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response, 200

if __name__ == "__main__":
    app.run(debug=True)
