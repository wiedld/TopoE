// DATA STRUCTURE -- FOR TESTING /////////////////////////////////////

var fuel_mix = {
  "Alameda": {"gas":16, "coal":14, "solar":14, "wind":14, "nuclear": 14, "hydro":14, "other":14},
  "Alpine": {"gas":16, "coal":14, "solar":14, "wind":14, "nuclear": 14, "hydro":14, "other":14},
  "Amador": {"gas":16, "coal":14, "solar":14, "wind":14, "nuclear": 14, "hydro":14, "other":14},
  "Butte": {"gas":16, "coal":14, "solar":14, "wind":14, "nuclear": 14, "hydro":14, "other":14},
  "Calaveras": {"gas":16, "coal":14, "solar":14, "wind":14, "nuclear": 14, "hydro":14, "other":14},
  "Colusa": {"gas":16, "coal":14, "solar":14, "wind":14, "nuclear": 14, "hydro":14, "other":14},
  "Contra Costa": {"gas":16, "coal":14, "solar":14, "wind":14, "nuclear": 14, "hydro":14, "other":14},
  "Del Norte": {"gas":16, "coal":14, "solar":14, "wind":14, "nuclear": 14, "hydro":14, "other":14},
  "El Dorado": {"gas":16, "coal":14, "solar":14, "wind":14, "nuclear": 14, "hydro":14, "other":14},
  "Fresno": {"gas":16, "coal":14, "solar":14, "wind":14, "nuclear": 14, "hydro":14, "other":14},
  "Glenn": {"gas":16, "coal":14, "solar":14, "wind":14, "nuclear": 14, "hydro":14, "other":14},
  "Humboldt": {"gas":16, "coal":14, "solar":14, "wind":14, "nuclear": 14, "hydro":14, "other":14},
  "Imperial": {"gas":16, "coal":14, "solar":14, "wind":14, "nuclear": 14, "hydro":14, "other":14},
  "Inyo": {"gas":16, "coal":14, "solar":14, "wind":14, "nuclear": 14, "hydro":14, "other":14},
  "Kern": {"gas":16, "coal":14, "solar":14, "wind":14, "nuclear": 14, "hydro":14, "other":14},
  "Kings": {"gas":16, "coal":14, "solar":14, "wind":14, "nuclear": 14, "hydro":14, "other":14},
  "Lake": {"gas":16, "coal":14, "solar":14, "wind":14, "nuclear": 14, "hydro":14, "other":14},
  "Lassen": {"gas":16, "coal":14, "solar":14, "wind":14, "nuclear": 14, "hydro":14, "other":14},
  "Los Angeles": {"gas":16, "coal":14, "solar":14, "wind":14, "nuclear": 14, "hydro":14, "other":14},
  "Madera": {"gas":16, "coal":14, "solar":14, "wind":14, "nuclear": 14, "hydro":14, "other":14},
  "Marin": {"gas":16, "coal":14, "solar":14, "wind":14, "nuclear": 14, "hydro":14, "other":14},
  "Mariposa": {"gas":16, "coal":14, "solar":14, "wind":14, "nuclear": 14, "hydro":14, "other":14},
  "Mendocino": {"gas":16, "coal":14, "solar":14, "wind":14, "nuclear": 14, "hydro":14, "other":14},
  "Merced": {"gas":16, "coal":14, "solar":14, "wind":14, "nuclear": 14, "hydro":14, "other":14},
  "Modoc": {"gas":16, "coal":14, "solar":14, "wind":14, "nuclear": 14, "hydro":14, "other":14},
  "Mono": {"gas":16, "coal":14, "solar":14, "wind":14, "nuclear": 14, "hydro":14, "other":14},
  "Monterey": {"gas":16, "coal":14, "solar":14, "wind":14, "nuclear": 14, "hydro":14, "other":14},
  "Napa": {"gas":16, "coal":14, "solar":14, "wind":14, "nuclear": 14, "hydro":14, "other":14},
  "Nevada": {"gas":16, "coal":14, "solar":14, "wind":14, "nuclear": 14, "hydro":14, "other":14},
  "Orange": {"gas":16, "coal":14, "solar":14, "wind":14, "nuclear": 14, "hydro":14, "other":14},
  "Placer": {"gas":16, "coal":14, "solar":14, "wind":14, "nuclear": 14, "hydro":14, "other":14},
  "Plumas": {"gas":16, "coal":14, "solar":14, "wind":14, "nuclear": 14, "hydro":14, "other":14},
  "Riverside": {"gas":16, "coal":14, "solar":14, "wind":14, "nuclear": 14, "hydro":14, "other":14},
  "Sacramento": {"gas":16, "coal":14, "solar":14, "wind":14, "nuclear": 14, "hydro":14, "other":14},
  "San Benito": {"gas":16, "coal":14, "solar":14, "wind":14, "nuclear": 14, "hydro":14, "other":14},
  "San Bernardino": {"gas":16, "coal":14, "solar":14, "wind":14, "nuclear": 14, "hydro":14, "other":14},
  "San Diego": {"gas":16, "coal":14, "solar":14, "wind":14, "nuclear": 14, "hydro":14, "other":14},
  "San Francisco": {"gas":16, "coal":14, "solar":14, "wind":14, "nuclear": 14, "hydro":14, "other":14},
  "San Joaquin": {"gas":16, "coal":14, "solar":14, "wind":14, "nuclear": 14, "hydro":14, "other":14},
  "San Luis Obispo": {"gas":16, "coal":14, "solar":14, "wind":14, "nuclear": 14, "hydro":14, "other":14},
  "San Mateo": {"gas":16, "coal":14, "solar":14, "wind":14, "nuclear": 14, "hydro":14, "other":14},
  "Santa Barbara": {"gas":16, "coal":14, "solar":14, "wind":14, "nuclear": 14, "hydro":14, "other":14},
  "Santa Clara": {"gas":16, "coal":14, "solar":14, "wind":14, "nuclear": 14, "hydro":14, "other":14},
  "Santa Cruz": {"gas":16, "coal":14, "solar":14, "wind":14, "nuclear": 14, "hydro":14, "other":14},
  "Shasta": {"gas":16, "coal":14, "solar":14, "wind":14, "nuclear": 14, "hydro":14, "other":14},
  "Sierra": {"gas":16, "coal":14, "solar":14, "wind":14, "nuclear": 14, "hydro":14, "other":14},
  "Siskiyou": {"gas":16, "coal":14, "solar":14, "wind":14, "nuclear": 14, "hydro":14, "other":14},
  "Solano": {"gas":16, "coal":14, "solar":14, "wind":14, "nuclear": 14, "hydro":14, "other":14},
  "Sonoma": {"gas":16, "coal":14, "solar":14, "wind":14, "nuclear": 14, "hydro":14, "other":14},
  "Stanislaus": {"gas":16, "coal":14, "solar":14, "wind":14, "nuclear": 14, "hydro":14, "other":14},
  "Sutter": {"gas":16, "coal":14, "solar":14, "wind":14, "nuclear": 14, "hydro":14, "other":14},
  "Tehama": {"gas":16, "coal":14, "solar":14, "wind":14, "nuclear": 14, "hydro":14, "other":14},
  "Trinity": {"gas":16, "coal":14, "solar":14, "wind":14, "nuclear": 14, "hydro":14, "other":14},
  "Tulare": {"gas":16, "coal":14, "solar":14, "wind":14, "nuclear": 14, "hydro":14, "other":14},
  "Tuolumne": {"gas":16, "coal":14, "solar":14, "wind":14, "nuclear": 14, "hydro":14, "other":14},
  "Ventura": {"gas":16, "coal":14, "solar":14, "wind":14, "nuclear": 14, "hydro":14, "other":14},
  "Yolo": {"gas":16, "coal":14, "solar":14, "wind":14, "nuclear": 14, "hydro":14, "other":14},
  "Yuba": {"gas":16, "coal":14, "solar":14, "wind":14, "nuclear": 14, "hydro":14, "other":14}
};


///////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////
//  SLIDERS, with src js script import in html DOM, before this js file


var set_slider_values = function(data_list,county_name){

    // make the sliders

    var axis = d3.svg.axis().orient("top").ticks(5);

    var fuel_names = ["gas", "coal", "solar", "wind", "nuclear", "hydro", "other"],
        slider_elements = ["#slider0", "#slider1", "#slider2", "#slider3", "#slider4", "#slider5", "#slider6"];

    $.each(slider_elements, function(idx, slider_element){
        d3.select(slider_element).call(d3.slider().axis(axis)
          .value(data_list[idx])
          .on("slide", function(evt, value){
            slide_event(value, fuel_names[idx], idx);
            }
          )
        );
    });


    // show the starting values in the html
    for (var i = 0; i<7; i++){
      d3.select('#slider'+i+'text').text(data_list[i]);
    }

    // what happens when the sliders are changed by the user.
    var slide_event = function(value, fuel_type, index){
        value = Math.round(value);
        // update_percentages() for all fuels, to sum to 100%
        data_list = update_percentages(value,index);
        // change values in the html label of the slider
        d3.select('#slider'+index+'text').text(value);
        // changle values in the fuel_mix dict
        fuel_mix[county_name][fuel_type] = value;
        //update the donut
        $('#fuel-donut').empty();
        make_donut(data_list);
    };

    // PERCENTAGES - changed with user input via sliders, and impacts the data structure (updates the dict) as well as changes the donut (make_donut(data_list)).
    var update_percentages = function(value,index){
      // update percentages based on 100
      data_list [index] = value;
      return data_list;
    };


};



//////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////
// TOPOJSON -- COUNTY MAP  ///////////////////////////////////////////////

    // MAKE THE SVG

      // define variables, to use later.
      var width = (960),
          height = (750),
          centered;

      // creates the svg object and adds to the body in the DOM.
      var svg = d3.select("#topomap").append("svg")
          .attr("width", width)
          .attr("height", height);

      // adds a rect to the svg, and adds an event listener
      svg.append("rect")
          .attr("class", "background")
          .attr("width", width)
          .attr("height", height)
          .on("click", clicked);


  // MAKE AN IDEA OF A MAP

      // "projection" -- how to display this svg vector data.
      //  geo.albersUSA is like a dictionary of how to translate geojson vector numbers?
      var projection = d3.geo.albersUsa()
          .scale(1070)
          .translate([width / 2, height / 2]);

      // d3.geo.path maps geocoordinates to svg.
      // .projection() links the projection var to the geo.path
      var path = d3.geo.path()
          .projection(projection);
      // so when we later refer to "path" attr, we have a path dict which matches the project dict from geo.albersUsa?


      // adds a DOM object "g" to the svg. and assigns to var g
      // we can now add to the svg by referring to g
      var g = svg.append("g");


  // GIVE THE MAP DATA TO DRAW

      // take the json data
      d3.json("/static/counties.json", function(error, us) {
        // append another "g" DOM element to the already present (bigger) g? Making a child?
        g.append("g")
          // each new "g" has the property "id", as taken from the json object "CA_counties"?
          .attr("id", "CA_counties")
          // select all "path" properties from witin the svg object g,
          .selectAll("path")
          // and assign the topojson vector info to the "path" attr of the g object
            .data(topojson.feature(us, us.objects.CA_counties).features)
          .enter().append("path")
            .attr("d", path)
            // add event listener
            .on("click", clicked);


        // to the g object, also add the path association with the borders.
        // unclear how it knows this is the borders
        g.append("path")
            .datum(topojson.mesh(us, us.objects.CA_counties, function(a, b) { return a !== b; }))
            .attr("id", "CA_countie-borders")
            .attr("d", path);
      });



    //JS INTERACTIVITY

      // js function.  for moving the clicked county to the center
      function clicked(d) {

        var x, y, k;

            // if clicking on a county (d)
            if (d && centered !== d) {
              var centroid = path.centroid(d);
              x = centroid[0];
              y = centroid[1];
              k = 4;
              centered = d;

              // get the id of the county, which == county name, and should match db info!!!
                var county_name = d.id;
                console.log(d.id);

              //get fuel_mix info, place into list.
                var v0 = fuel_mix[county_name]["gas"],
                    v1 = fuel_mix[county_name]["coal"],
                    v2 = fuel_mix[county_name]["solar"],
                    v3 = fuel_mix[county_name]["wind"],
                    v4 = fuel_mix[county_name]["nuclear"],
                    v5 = fuel_mix[county_name]["hydro"],
                    v6 = fuel_mix[county_name]["other"];
                var data_list = [v0,v1,v2,v3,v4,v5,v6];

              // display the c3 donut, with county-specific data.
                //  empty old
                  $('#fuel-donut').empty();
                //  make new
                  make_donut(data_list);

              // display the d3 sliders, with county-specific data.
                // make visible
                  $('#slider-wrapper').css('visibility','visible');
                // get ride of old sliders & values.
                  $('#slider0').empty();
                  $('#slider1').empty();
                  $('#slider2').empty();
                  $('#slider3').empty();
                  $('#slider4').empty();
                  $('#slider5').empty();
                  $('#slider6').empty();
                // re-make sliders with new values
                  set_slider_values(data_list, county_name);

            } else {
              x = width / (2.5);
              y = height / (2.5);
              k = 1;
              centered = null;
              $('#fuel-donut').empty();
              $('#slider-wrapper').css('visibility','hidden');
            }

            // bind all the clicked paths to the class .active
            g.selectAll("path")
                .classed("active", centered && function(d) { return d === centered; });

            g.transition()
                .duration(750)
                .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")scale(" + k + ")translate(" + -x + "," + -y + ")")
                .style("stroke-width", 1.5 / k + "px");
      }



////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////
// DONUT CHART /////////////////////////////////////////////////////////////

  var make_donut = function(data0){

    // MAKE THE IDEA OF THE SVG

        var width = 960/2,
            height = 500/2,
            outerRadius = Math.min(width, height) * .5 - 10,
            innerRadius = outerRadius * .6;


    // MAKE THE DATA, to feed into the svg
        var n = 7,
            data;


    // MAKE THE STYLE:  color, shape (arc), and divide arc into data sections(pie)
    // note:  arc not added to svg yet!
        var color = d3.scale.category10();
        var arc = d3.svg.arc();
        var pie = d3.layout.pie()
            .sort(null);


    // ADD SVG TO THE BODY
        var svg = d3.select("#fuel-donut").append("svg")
            .attr("width", width)
            .attr("height", height);


    // ADD DATA TO EACH ARC
        svg.selectAll(".arc")
            .data(arcs(data0))
          // ADD ARC TO THE SVG
          .enter().append("g")
            .attr("class", "arc")
            .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")")

          // MAKE THE VISUAL PATH be the color(i) and data(d)
          .append("path")
            .attr("fill", function(d, i) { return color(i); })
            .attr("d", arc);

    // TODO:  add data labels to each arc in the donut.
        // svg.append("text")
        //       .attr("transform", "translate(" + arc.centroid(d) + ")")
        //       .attr("dy", ".35em")
        //       .style("text-anchor", "middle")
        //       .text("test");


    // ARCS function
        function arcs(data0) {
          // defines the arc based on pie of data0.
          var arcs0 = pie(data0),
              i = -1,
              arc;
          // set the color of arc0 (for data0)
          while (++i < n) {
            arc = arcs0[i];
            arc.innerRadius = innerRadius;
            arc.outerRadius = outerRadius;
          }
          return arcs0;
        }


  };




//////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////
  // EVENT HANDLING //////////////////////////////////////////////


function runScenario(evt){
  evt.preventDefault();
  console.log("runScenario js function");

  $.ajax('scenario-result', {
    type: 'POST',
    data: JSON.stringify(fuel_mix),
    contentType: 'application/json',
    success: function(data, status, result){
      var scenario_result = JSON.parse(result.responseText);
      console.log(scenario_result);
    }
  });

}


$('#submit').on("click", runScenario);



//////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////
  // C3 donut ////////////////////////////////////////////////////


  // TODO:  take the interact "mouseover" functionality of the c3 donut below, and add to the d3 element used above.

      // var make_donut = function(){
      //       var chart = c3.generate({
      //         data: {
      //             columns: [
      //                 ['Natural gas', 30],
      //                 ['data2', 120],
      //             ],
      //             type : 'donut',
      //             onclick: function (d, i) { console.log("onclick", d, i); },
      //             onmouseover: function (d, i) { console.log("onmouseover", d, i); },
      //             onmouseout: function (d, i) { console.log("onmouseout", d, i); }
      //         },
      //         donut: {
      //             title: "Fuel Mix in County"
      //         },
      //         bindto: document.getElementById('fuel-donut')
      //       });

      //       setTimeout(function () {
      //           chart.load({
      //               columns: [
      //                   ["setosa", 0.2, 0.2, 0.2, 0.2, 0.2, 0.4, 0.3, 0.2, 0.2, 0.1, 0.2, 0.2, 0.1, 0.1, 0.2, 0.4, 0.4, 0.3, 0.3, 0.3, 0.2, 0.4, 0.2, 0.5, 0.2, 0.2, 0.4, 0.2, 0.2, 0.2, 0.2, 0.4, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.2, 0.2, 0.3, 0.3, 0.2, 0.6, 0.4, 0.3, 0.2, 0.2, 0.2, 0.2],
      //                   ["versicolor", 1.4, 1.5, 1.5, 1.3, 1.5, 1.3, 1.6, 1.0, 1.3, 1.4, 1.0, 1.5, 1.0, 1.4, 1.3, 1.4, 1.5, 1.0, 1.5, 1.1, 1.8, 1.3, 1.5, 1.2, 1.3, 1.4, 1.4, 1.7, 1.5, 1.0, 1.1, 1.0, 1.2, 1.6, 1.5, 1.6, 1.5, 1.3, 1.3, 1.3, 1.2, 1.4, 1.2, 1.0, 1.3, 1.2, 1.3, 1.3, 1.1, 1.3],
      //                   ["virginica", 2.5, 1.9, 2.1, 1.8, 2.2, 2.1, 1.7, 1.8, 1.8, 2.5, 2.0, 1.9, 2.1, 2.0, 2.4, 2.3, 1.8, 2.2, 2.3, 1.5, 2.3, 2.0, 2.0, 1.8, 2.1, 1.8, 1.8, 1.8, 2.1, 1.6, 1.9, 2.0, 2.2, 1.5, 1.4, 2.3, 2.4, 1.8, 1.8, 2.1, 2.4, 2.3, 1.9, 2.3, 2.5, 2.3, 1.9, 2.0, 2.3, 1.8],
      //               ]
      //           });
      //       }, 1500);

      //       setTimeout(function () {
      //           chart.unload({
      //               ids: 'data1'
      //           });
      //           chart.unload({
      //               ids: 'data2'
      //           });
      //       }, 2500);
      // };

