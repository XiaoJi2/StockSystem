$(function() {
    var barOptions = {
        series: {
            lines: {
                show: true,
                lineWidth: 2,
                fill: true,
                fillColor: {
                    colors: [{
                        opacity: 0.0
                    }, {
                        opacity: 0.0
                    }]
                }
            }
        },
        xaxis: {
            tickDecimals: 0
        },
        colors: ["#1ab394"],
        grid: {
            color: "#999999",
            hoverable: true,
            clickable: true,
            tickColor: "#D4D4D4",
            borderWidth:0
        },
        legend: {
            show: false
        },
        tooltip: true,
        tooltipOpts: {
            content: "x: %x, y: %y"
        }
    };
    console.log(111)
     $(function() {
         console.log(111)
            $.ajax({
                url:"{{ url('App:getlianbanhight') }}",
                type: 'get',
                data:{},
                success:function(result){
                    console.log(result)
                }})
         console.log(111)
        });
    var barData = {
        label: "bar",
        resultData: [],

        data: [
            [1, 34],
            [2, 25],
            [3, 19],
            [4, 34],
            [5, 32],
            [6, 44]
        ]
    };
    $.plot($("#flot-line-chart"), [barData], barOptions);

});