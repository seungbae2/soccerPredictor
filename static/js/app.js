$('select').on('change', function() {
    //alert( this.value );
    renderData(event_data, this.value);
});

var event_data = [];
var svgWidth = 1024;
var svgHeight = 436;

var margin = {
  top: 20,
  right: 40,
  bottom: 80,
  left: 100
};

var width = svgWidth - margin.left - margin.right;
var height = svgHeight - margin.top - margin.bottom;
var svg = d3.select(".chart").append("svg")
    .attr("width", svgWidth)
    .attr("height", svgHeight);

d3.json("static/data/result.json").then((data, error) => {
    if (error) throw error;
    //console.log(data);
    event_data = data;
    
    renderData(event_data, "all");
});
function drawCircle(objSvg, period){

    d3.selectAll("circle").remove();

    objSvg.append("g").selectAll("circle")
        .data(event_data)
        .enter()
        .filter(function(d){
            if(period == 0){
                if(d.event == "Goal"){
                    return true;
                }else if(d.event == "Shot"){
                    return true;
                }else if(d.event == "Hit"){
                    return true;
                }else if(d.event == "Penalty"){
                    return true;
                }else if(d.event == "Blockd Shot"){
                    return true;
                }else{
                    return false;
                }
            }else{
                if(d.period == period) {
                    if(d.event == "Goal"){
                        return true;
                    }else if(d.event == "Shot"){
                        return true;
                    }else if(d.event == "Hit"){
                        return true;
                    }else if(d.event == "Penalty"){
                        return true;
                    }else if(d.event == "Blockd Shot"){
                        return true;
                    }else{
                        return false;
                    }
                }else{
                    return false;
                } 
            }
        })
        .append("circle")
        .style("fill-opacity", "0.75")
        .style("stroke", "black")
        .style("fill", function(d){
            var color;
            if(d.event == "Goal"){
                color = "green";
            }else if(d.event == "Shot"){
                color = "blue";
            }else if(d.event == "Hit"){
                color = "red";
            }else if(d.event == "Penalty"){
                color = "gray";
            }else if(d.event == "Blockd Shot"){
                color = "red";
            }
            return color;
        })
        .attr("cx", d => 5*(d.x))
        .attr("cy", d => 4.3*(d.y))
        .attr("r",10)
        .on('mouseover', tip.show)
        .on('mouseout', tip.hide);

    return objSvg;
}

function renderData(event_data,selectData){
    //console.log(event_data);

    tip = d3.tip().attr('class', 'd3-tip').html(function(d) { 
        return (`Event: ${d.event}<br>Team: ${d.name}<br>${d.description}`);
    })

    svg.call(tip);

    if(selectData == "all"){
        drawCircle(svg, 0)
    }else if(selectData == "1st"){
        drawCircle(svg, 1)
    }else if(selectData == "2nd"){
        drawCircle(svg, 2)
    }else if(selectData == "3rd"){
        drawCircle(svg, 3)
    }else if(selectData == "ot"){
        drawCircle(svg, 4)
    }

}

d3.json("static/data/game_stat.json").then(function(data){
    var bufferData = data;
    /////////////Shots & Goals////////////////
    var goal_trace = {
        x: [data.home_team, data.away_team],
        y: [data.home_data.goals, data.away_data.goals],
        type: "bar",
        name: "Goals",
        marker: {
            color: "navyblue"
        }
    };

    var shot_trace = {
        x: [data.home_team, data.away_team],
        y: [data.home_data.shots - data.home_data.goals, data.away_data.shots - data.away_data.goals],
        type: "bar",
        name: "Shots",
        marker: {
            color: "lightgray"
        }
    };
    var shot_goal_data = [goal_trace, shot_trace];

    var goal_shot_layout = {
        title: "Total Shots & Goals per Team",
        xaxis: { title: "Team"},
        yaxis: { title: "Count"},
        barmode: "stack"
    };

    Plotly.newPlot("shot_goal", shot_goal_data, goal_shot_layout);

    ///////////////////Face-Off %//////////////

    //console.log(bufferData);
    //console.log(bufferData.home_data.faceOffWinPercentage);
    var faceoff_trace = {
        labels: [bufferData.home_team, bufferData.away_team],
        values: [bufferData.home_data.faceOffWinPercentage, bufferData.away_data.faceOffWinPercentage],
        type: 'pie',
        marker: {
            colors: ['navyblue', 'lightgray']
        }
    };

    var faceoff_data = [faceoff_trace];
    var faceoff_layout = {
        title: "Face-Off Win Percentage",
        legend: {
            x:2,
            y:.9
        }
    };

    Plotly.newPlot("face_off", faceoff_data, faceoff_layout);

    ////////////////////Hits///////////////////////////
    var home_hit_trace = {
        x: [bufferData.home_team],
        y: [bufferData.home_data.hits],
        type: "bar",
        name: bufferData.home_team,
        marker: {
            color: 'navyblue'
        }
    };

    var away_hit_trace = {
        x: [bufferData.away_team],
        y: [bufferData.away_data.hits],
        name: bufferData.away_team,
        type: "bar",
        marker: {
            color: 'lightgray'
        }
    };
    var hit_data = [home_hit_trace, away_hit_trace];
    var hit_layout = {
        title: "Total Hits per Team",
        xaxis: { title: "Team",
        showticklabels: false},
        yaxis: { title: "Number of Hits"}

    };

    Plotly.newPlot("hit", hit_data, hit_layout);
    
});