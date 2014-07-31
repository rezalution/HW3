function showData(data){
    $('#cal-heatmap').empty();
    var calendar = new CalHeatMap();
    calendar.init({
        data: data,
        start: new Date(2013, 3),
        id : "graph_k",
        domain : "month",
        subDomain : "x_day",
        range : 6,
        cellsize: 15,
        cellpadding: 3,
        cellradius: 5,
        domainGutter: 15,
        scale: [2, 4, 6, 8],
        itemName: ["hours", "hours"],
        cellLabel: {
            empty: "0 hours",
            filled: "{count} {name} {date}"
        },
        scaleLabel: {
            lower: "{min} {name}",
            inner: "{down} {up} {name}",
            upper: "{max} {name}"
        },
    });
    $('#cal-heatmap').html(data.name)
    $('.graph-legend').empty();


    $('#cal-heatmap2').empty();
    var cal = new CalHeatMap();
    cal.init({
        data: data,
        start: new Date(2013, 9),
        id : "graph_k",
        domain : "month",
        subDomain : "x_day",
        range : 6,
        cellsize: 15,
        cellpadding: 3,
        cellradius: 5,
        domainGutter: 15,
        scale: [2, 4, 6, 8],
        itemName: ["hours", "hours"],
        cellLabel: {
            empty: "0 hours",
            filled: "{count} {name} {date}"
        },
        scaleLabel: {
            lower: "{min} {name}",
            inner: "{down} {up} {name}",
            upper: "{max} {name}"
        },
    });
    $('#cal-heatmap2').html(data.name)
}

function errorData(){
    location.href="http://localhost:12080/cal"
    // alert('error');
}

function completeData(){
    $("#dialog-modal").dialog("close");
    $('#floatingBarsG').css("display", "none");
}

function handleClick(e) {
    $('#floatingBarsG').toggle();
    $("#dialog-modal" ).dialog({
        height: 140,
        width: 200,
        modal: true
    });

// setTimeout(function(){   //テスト用の3秒待つ処理
    $.ajax('/cal', {
        type: 'GET',
        cache : false,
        data: {
            fmt: 'json'
        },
        success: showData,
        error: errorData,
        complete : completeData                          
    });
// },1300);   //テスト用の3秒待つ処理
}

$(document).ready(function(){
//    $('#floatingBarsG').toggle();
//     $("#dialog-modal" ).dialog({
//         height: 140,
//         width: 200,
//         modal: true
//     });

// // setTimeout(function(){   //テスト用の3秒待つ処理
//     $.ajax('/cal', {
//         type: 'GET',
//         cache : false,
//         data: {
//             fmt: 'json'
//         },
//         success: showData,
//         error: errorData,
//         complete : completeData                          
//     });

    $('#getitButton').on('click', handleClick);
});

// 合計の時間表示
function showSumData(data){
    var YMT = "FY13 Your Meeting Time is " + data.allgokei + " hours."
    $('p.ymt').text(YMT)
}

$(document).ready(function(){
    $.ajax('/cal', {
        type: 'GET',
        cache : false,
        data: {
            fmt: 'jsonsum'
        },
        success: showSumData,
    });
});
