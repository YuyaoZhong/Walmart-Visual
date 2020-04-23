function getJSON(url) {
  var resp;
  var xmlHttp;

  resp = "";
  xmlHttp = new XMLHttpRequest();

  if (xmlHttp != null) {
    xmlHttp.open("GET", url, false);
    xmlHttp.send(null);
    resp = JSON.parse(xmlHttp.responseText);
  }

  return resp;
}

function getdata(productID) {
  var js;
  const url = "http://127.0.0.1:5000/product-data/" + productID;

  js = getJSON(url);
  //   document.getElementById("result").innerHTML = JSON.stringify(js);
  //   console.log(js);
  return js;
}

function gettimeseries(productID) {
  var js;
  const url = "http://127.0.0.1:5000/product-data-time-series/" + productID;

  js = getJSON(url);
  //   document.getElementById("result").innerHTML = JSON.stringify(js);
  //   console.log(js);
  return js;
}

function getinfo(productID) {
  var js;
  const url = "http://127.0.0.1:5000/product-info/" + productID;
  js = getJSON(url);

  return js;
}

// function getitems() {
//   let result = getdata(75663300);
//   //   console.log(result);
//   let labels = result.map(function (e) {
//     return e.price;
//   });

//   console.log(labels);
//   var data = result.map(function (e) {
//     return e.onlineStockLevel;
//   });
//   console.log(data);
// }

var config = {
  // type: "line",
  data: {
    labels: [],
    datasets: [
      {
        label: "Product Price",
        backgroundColor: window.chartColors.red,
        borderColor: window.chartColors.red,
        data: [],
        price: [],
        type: "line",
        steppedLine: true,
        fill: false,
      },
    ],
  },
  options: {
    responsive: true,
    title: {
      display: true,
      text: "Select Your Product",
      fontSize: 20,
    },
    tooltips: {
      mode: "index",
      intersect: false,
      callbacks: {
        afterLabel: function (tooltipItem, data) {
          return (
            "Price: $" +
            data.datasets[tooltipItem.datasetIndex].price[tooltipItem.index]
          );
        },
      },
    },
    hover: {
      mode: "nearest",
      intersect: true,
    },
    scales: {
      xAxes: [
        {
          type: "time",
          // time: {
          //   unit: "minute",
          // },

          time: { timezone: "America/NewYork" },
          distribution: "series",
          display: true,
          offset: true,
          ticks: {
            major: {
              enabled: true,
              fontStyle: "bold",
            },
            source: "data",
            autoSkip: true,
            autoSkipPadding: 75,
            maxRotation: 0,
          },
          scaleLabel: {
            display: true,
            labelString: "Time History",
          },
        },
      ],
      yAxes: [
        {
          display: true,
          ticks: {
            beginAtZero: true,
            callback: function (value) {
              if (value % 1 === 0) {
                return value;
              }
            },
          },
          scaleLabel: {
            display: true,
            labelString: "Price",
          },
        },
      ],
    },
  },
};

window.onload = function () {
  var ctx = document.getElementById("chart1").getContext("2d");
  window.myLine = new Chart(ctx, config);
};

function getValue(selectObject) {
  var value = selectObject.value;
  let result = getdata(value);
  let info = getinfo(value);
  let timeseries = gettimeseries(value);
  //   console.log(info);
  let labels = result.map(function (e) {
    return e.scrapetime;
  });

  let data = result.map(function (e) {
    return e.price;
  });

  // config.data.labels = labels;
  config.data.datasets[0].data = timeseries;
  config.data.datasets[0].price = data;
  config.options.title.text = info[0].name;
  document.getElementById("productLink").setAttribute("href", info[0].href);
  document
    .getElementById("productImage")
    .setAttribute("src", info[0].imagehref);

  window.myLine.update();
}

// async function getdata(productID) {
//   const url = "http://127.0.0.1:5000/product-data/" + productID;

//   var response = await fetch(url);
//   var result = await response.json();
//   document.getElementById("result").innerHTML = JSON.stringify(result);
//   //   console.log(result);

//   //   var labels = result.map(function (e) {
//   //     return e.price;
//   //   });

//   //   console.log(labels);
//   //   var data = result.map(function (e) {
//   //     return e.onlineStockLevel;
//   //   });
//   //   console.log(data);
//   return result;
// }
