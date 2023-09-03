setInterval(() => {
	fetch(`http://127.0.0.1:5000/getsysteminfo`)
    .then(res => res.json())
    .then(res => {
        ram = document.getElementById("ram")
        ram.innerText = res.ram_info.free
    })

}, 500);