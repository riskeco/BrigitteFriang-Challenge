function sidebarButton(tabNumber){
  //Sidebar button home default
  $(".link-sidebar-active").removeClass("link-sidebar-active");
  $(".wrapper-link-active").removeClass("wrapper-link-active");
  $(".link-sidebar#"+tabNumber).addClass("link-sidebar-active");
  $(".link-sidebar#"+tabNumber).parent().addClass("wrapper-link-active");
  $(".main-content").hide();
  $(".tab-"+tabNumber).show();
}

$(".link-sidebar").hover(
    function(){
        $(this).addClass("shadow");
    }, function(){
        $(this).removeClass("shadow");
    }
);

$(".box").attr({"data-content":"Libre","data-placement":"right","data-trigger":"hover"});
$(".box-active").attr({"data-content":"Occupé","data-placement":"right","data-trigger":"hover"});

$(".box").popover();
$(".box-active").popover();

$(".wrapper-link").click(function(){
      document.location.href="/4e9033c6eacf38dc2a5df7a14526bec1/"+$(this).attr("id");
    }
);

$(".side-title").click(function(e){
        e.preventDefault();
        $(".side-title-active").removeClass("side-title-active");
        $(".side-title-active").removeClass("side-title-active");
        $(this).addClass("side-title-active");       
    }
);

Chart.defaults.RoundedDoughnut    = Chart.helpers.clone(Chart.defaults.doughnut);
Chart.controllers.RoundedDoughnut = Chart.controllers.doughnut.extend({
    draw: function(ease) {
        var ctx           = this.chart.ctx;
        var easingDecimal = ease || 1;
        var arcs          = this.getMeta().data;
        Chart.helpers.each(arcs, function(arc, i) {
            arc.transition(easingDecimal).draw();

            var pArc   = arcs[i === 0 ? arcs.length - 1 : i - 1];
            var pColor = pArc._view.backgroundColor;

            var vm         = arc._view;
            var radius     = (vm.outerRadius + vm.innerRadius) / 2;
            var thickness  = (vm.outerRadius - vm.innerRadius) / 2;
            var startAngle = Math.PI - vm.startAngle - Math.PI / 2;
            var angle      = Math.PI - vm.endAngle - Math.PI / 2;

            ctx.save();
            ctx.translate(vm.x, vm.y);

            ctx.fillStyle = i === 0 ? vm.backgroundColor : pColor;
            ctx.beginPath();
            ctx.arc(radius * Math.sin(startAngle), radius * Math.cos(startAngle), thickness, 0, 2 * Math.PI);
            ctx.fill();

            ctx.fillStyle = vm.backgroundColor;
            ctx.beginPath();
            ctx.arc(radius * Math.sin(angle), radius * Math.cos(angle), thickness, 0, 2 * Math.PI);
            ctx.fill();

            ctx.restore();
        });
    }
});

Chart.pluginService.register({
    beforeDraw: function(chart) {
      if (chart.config.options.elements.center) {
        // Get ctx from string
        var ctx = chart.chart.ctx;

        // Get options from the center object in options
        var centerConfig = chart.config.options.elements.center;
        var fontStyle = centerConfig.fontStyle || 'Futura Medium';
        var txt = centerConfig.text;
        var color = centerConfig.color || '#000';
        var maxFontSize = centerConfig.maxFontSize || 75;
        var sidePadding = centerConfig.sidePadding || 20;
        var sidePaddingCalculated = (sidePadding / 100) * (chart.innerRadius * 2)
        // Start with a base font of 30px
        ctx.font = "30px " + fontStyle;

        // Get the width of the string and also the width of the element minus 10 to give it 5px side padding
        var stringWidth = ctx.measureText(txt).width;
        var elementWidth = (chart.innerRadius * 2) - sidePaddingCalculated;

        // Find out how much the font can grow in width.
        var widthRatio = elementWidth / stringWidth;
        var newFontSize = Math.floor(30 * widthRatio);
        var elementHeight = (chart.innerRadius * 2);

        // Pick a new font size so it will not be larger than the height of label.
        var fontSizeToUse = Math.min(newFontSize, elementHeight, maxFontSize);
        var minFontSize = centerConfig.minFontSize;
        var lineHeight = centerConfig.lineHeight || 25;
        var wrapText = false;

        if (minFontSize === undefined) {
          minFontSize = 20;
        }

        if (minFontSize && fontSizeToUse < minFontSize) {
          fontSizeToUse = minFontSize;
          wrapText = true;
        }

        // Set font settings to draw it correctly.
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        var centerX = ((chart.chartArea.left + chart.chartArea.right) / 2);
        var centerY = ((chart.chartArea.top + chart.chartArea.bottom) / 2);
        ctx.font = fontSizeToUse + "px " + fontStyle;
        ctx.fillStyle = color;

        if (!wrapText) {
          ctx.fillText(txt, centerX, centerY);
          return;
        }

        var words = txt.split(' ');
        var line = '';
        var lines = [];

        // Break words up into multiple lines if necessary
        for (var n = 0; n < words.length; n++) {
          var testLine = line + words[n] + ' ';
          var metrics = ctx.measureText(testLine);
          var testWidth = metrics.width;
          if (testWidth > elementWidth && n > 0) {
            lines.push(line);
            line = words[n] + ' ';
          } else {
            line = testLine;
          }
        }

        // Move the center up depending on line height and number of lines
        centerY -= (lines.length / 2) * lineHeight;

        for (var n = 0; n < lines.length; n++) {
          ctx.fillText(lines[n], centerX, centerY);
          centerY += lineHeight;
        }
        //Draw text in center
        ctx.fillText(line, centerX, centerY);
      }
    }
  });

$(document).ready(function(){
  try{
  var ctx = document.getElementById('myChart').getContext('2d');
  var myChart = new Chart(ctx, {
      type: 'RoundedDoughnut',
      data: {
          datasets: [{
              data: [47, 47-100],
              backgroundColor: [
                  '#5FB054',
                  '#FFE8CA'
              ],
              borderWidth:0,
              label:'dataset 1'
          }]
      },
      options:{
          cutoutPercentage: 90,
          elements: {
              center: {
                text: '47%',
                color: '#FFFFFF', // Default is #000000
                fontStyle: 'Arial', // Default is Arial
                sidePadding: 40, // Default is 20 (as a percentage)
                minFontSize: 25, // Default is 20 (in px), set to false and text will not wrap.
                lineHeight: 50 // Default is 25 (in px), used for when text wraps
              }
            }
      }
  });
  }catch(error){
    console.log(error);
  }
  
  try{
    var ctx2 = document.getElementById("myChart2");
    var myLineChart = new Chart(ctx2, {
      type: 'line',
      data: {
        labels: ["6h", "7h", "8h", "9h", "10h", "11h", "12h", "13h", "14h", "15h", "16h", "17h", "18h", "19h", "20h", "21h", "22h", "23h", "00h"],
        datasets: [{
          label: "$",
          lineTension: 0.3,
          backgroundColor: "rgba(255, 214, 122, 0.05)",
          borderColor: "rgba(255, 214, 122, 1)",
          pointRadius: 3,
          pointBackgroundColor: "rgba(255, 214, 122, 1)",
          pointBorderColor: "rgba(255, 214, 122, 1)",
          pointHoverRadius: 3,
          pointHoverBackgroundColor: "rgba(255, 214, 122, 1)",
          pointHoverBorderColor: "rgba(255, 214, 122, 1)",
          pointHitRadius: 10,
          pointBorderWidth: 2,
          data: [10, 200, 400, 500, 800, 850, 900, 950, 920, 700, 600, 300, 100, 50, 40, 30, 20, 5, 5],
        }],
      },
      options: {
        maintainAspectRatio: false,
        layout: {
          padding: {
            left: 10,
            right: 25,
            top: 25,
            bottom: 0
          }
        },
        scales: {
          xAxes: [{
            time: {
              unit: '$'
            },
            gridLines: {
              display: false,
              drawBorder: false
            },
            ticks: {
              maxTicksLimit: 15
            }
          }],
          yAxes: [{
            ticks: {
              maxTicksLimit: 5,
              padding: 10
            },
            gridLines: {
              color: "rgba(255, 214, 122, 0.05)",
              zeroLineColor: "rgba(255, 214, 122, 0.05)",
              drawBorder: false,
              borderDash: [2],
              zeroLineBorderDash: [2]
            }
          }],
        },
        legend: {
          display: false
        },
        tooltips: {
          backgroundColor: "rgb(255,255,255)",
          bodyFontColor: "#858796",
          titleMarginBottom: 10,
          titleFontColor: '#6e707e',
          titleFontSize: 14,
          borderColor: '#dddfeb',
          borderWidth: 1,
          xPadding: 15,
          yPadding: 15,
          displayColors: false,
          intersect: false,
          mode: 'index',
          caretPadding: 10
        }
      }
    });
  }catch(error){
    console.log(error);
  }
});