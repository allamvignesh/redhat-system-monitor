let ram_used = Array(10).fill(0)
let ram_free = Array(10).fill(0)
let ram_buff = Array(10).fill(0)
let tot = 0
let storageFreePercent = 0

setInterval(() => {
	fetch(`http://127.0.0.1:5000/getsysteminfo`)
    .then(res => res.json())
    .then(res => {
        tot = res.ram_info.total
        ram_used.shift()
        ram_free.shift()
        addData(ramchart, "used", Number(res.ram_info.used))
        addData(ramchart, "free", Number(res.ram_info.free))
        addData(ramchart, "buff", Number(res.ram_info.buff))

        storageFreePercent = Number(res.disk_info[0]["Use%"].replace("%", ""))
        storageChart.data.datasets[0].data = [100-storageFreePercent, storageFreePercent]
        storageChart.update()
    })

}, 500);

const ctx = document.getElementById('ramChart');
const ramchart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: ram_used,
        datasets: [{
            label: "used",
            data: ram_used,
            borderColor: "#fe4a49",
            // pointStyle: false,
        },
        {
            label: "free",
            data: ram_free,
            borderColor: "#2ab7ca ",
            pointStyle: false,
        },
        {
            label: "buff",
            data: ram_buff,
            borderColor: "#fed766",
            pointStyle: false,
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true,
            }
        }
    }
});

function addData(chart, label, newData) {
    chart.data.datasets.forEach((dataset) => {
        if (dataset.label == label)
            dataset.data.push(newData);
    });
    chart.update();
}

const pie = document.getElementById("storageChart")
const storageChart = new Chart(pie, {
    type: 'pie',
    data: {
        labels: [
            'Free',
            'Used'
          ],
          datasets: [{
            label: 'My First Dataset',
            data: [storageFreePercent, 100-storageFreePercent],
            backgroundColor: [
              'rgb(255, 99, 132)',
              'rgb(255, 205, 86)'
            ],
            hoverOffset: 4
          }]
    }
})
