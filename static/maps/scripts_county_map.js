var county_name;

// UNIQUE CODING FOR COUNTY MAP/////////////////////////////////////

// get map data structure
    // triggered when the topojson map is created
    function get_map_data(for_state){
      // evt.preventDefault();
      console.log("get_map_data js function");

      var data = for_state;
      $.ajax('county-map-data', {
        type: 'POST',
        data: data,
        contentType: 'application/json',
        success: function(data, status, result){
          fuel_mix = JSON.parse(result.responseText);
          console.log(fuel_mix);
        }
      });
    }

    var fuel_mix = {};


// allow choice of different states from autocomplete box
   var auto = completely(document.getElementById('enter-state'), {
      fontSize : '24px',
      fontFamily : 'Arial',
      color:'#933',
   });
   auto.options = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"];
   auto.repaint();
   setTimeout(function() {
    auto.input.focus();
   },0);


// dict used for event listener.
  // user entered state, and listener then draws county topojson map.
    //  look for code after the topojson map is defined!!!

var state_name_to_abbv = {
  "Alabama": "AL",
  "Alaska": "AK",
  "Arizona": "AZ",
  "Arkansas": "AR",
  "California": "CA",
  "Colorado": "CO",
  "Connecticut": "CT",
  "Delaware": "DE",
  "Florida": "FL",
  "Georgia": "GA",
  "Hawaii": "HI",
  "Idaho": "ID",
  "Illinois": "IL",
  "Indiana": "IN",
  "Iowa": "IA",
  "Kansas": "KS",
  "Kentucky": "KY",
  "Louisiana": "LA",
  "Maine": "ME",
  "Maryland": "MD",
  "Massachusetts": "MA",
  "Michigan": "MI",
  "Minnesota": "MN",
  "Mississippi": "MS",
  "Missouri": "MO",
  "Montana": "MT",
  "Nebraska": "NE",
  "Nevada": "NV",
  "New Hampshire": "NH",
  "New Jersey": "NJ",
  "New Mexico": "NM",
  "New York": "NY",
  "North Carolina": "NC",
  "North Dakota": "ND",
  "Ohio": "OH",
  "Oklahoma": "OK",
  "Oregon": "OR",
  "Pennsylvania": "PA",
  "Rhode Island": "RI",
  "South Carolina": "SC",
  "South Dakota": "SD",
  "Tennessee": "TN",
  "Texas": "TX",
  "Utah": "UT",
  "Vermont": "VT",
  "Virginia": "VA",
  "Washington": "WA",
  "West Virginia": "WV",
  "Wisconsin": "WI",
  "Wyoming": "WY"
};


///////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////
//  SLIDERS, with src js script import in html DOM, before this js file


var set_slider_values = function(data_list,county_name){

    // make the sliders

    // var axis = d3.svg.axis().orient("bottom").ticks(5);

    var fuel_names = ["gas", "coal", "solar", "wind", "nuclear", "hydro", "other"],
        slider_elements = ["#slider0", "#slider1", "#slider2", "#slider3", "#slider4", "#slider5", "#slider6"];

    $.each(slider_elements, function(idx, slider_element){
        d3.select(slider_element).call(
          d3.slider()
          // .axis(axis)
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


var make_topojson_map_counties = function(for_state){

    get_map_data(for_state);

    // MAKE THE SVG

      // define variables, to use later.
      var width = (800),
          height = (500),
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
      var projection = d3.geo.albers()
          // .center([15,20])
          // .rotate
          // .scale(3000)
          // .translate([width / 2, height / 2]);
          .rotate([96, 0])
          // .center([-.6, 38.7])
          .parallels([29.5, 45.5])
          .scale(1070)
          .translate([width / 2, height / 2])
          .precision(.1);

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
      var file_path = "/static/maps/"+for_state+"_counties.json";
      d3.json(file_path, function(error, us) {
        // append another "g" DOM element to the already present (bigger) g? Making a child?
        g.append("g")
          // each new "g" has the property "id", as taken from the json object "CA_counties"?
          .on("mouseover", function() {
            d3.select(this).style("cursor","zoom-in");
          })
          .attr("id", "counties")
          // select all "path" properties from witin the svg object g,
          .selectAll("path")
          // and assign the topojson vector info to the "path" attr of the g object
            .data(topojson.feature(us, us.objects.State_counties).features)
          .enter().append("path")
            .attr("d", path)
            // add event listener
            .on("click", clicked);


        // to the g object, also add the path association with the borders.
        // unclear how it knows this is the borders
        g.append("path")
            .datum(topojson.mesh(us, us.objects.State_counties, function(a, b) { return a !== b; }))
            .attr("id", "county-borders")
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
                county_name = d.id;
                console.log(d.id);

              //get fuel_mix info, place into list.
                if (!fuel_mix[county_name]){
                  fuel_mix[county_name] = {};
                  fuel_mix[county_name]["gas"] = 0;
                  fuel_mix[county_name]["coal"] = 0;
                  fuel_mix[county_name]["solar"] = 0;
                  fuel_mix[county_name]["wind"] = 0;
                  fuel_mix[county_name]["nuclear"] = 0;
                  fuel_mix[county_name]["hydro"] = 0;
                  fuel_mix[county_name]["other"] = 0;
                };

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

              // input the scenario results.  Note: this div is hidden until after the scenario is run!
                  var exists = false;
                  try {
                      eval(scenario_result);
                      exists = true;
                  } catch(e) {
                      exists = false;
                  }
                  if (exists){
                    $('#display-results').attr("class",scenario_result[county_name][0]).text(scenario_result[county_name][1]);
                  }


            } else {
              x = width / (2.5);
              y = height / (2.5);
              k = 1;
              centered = null;
              $('#fuel-donut').empty();
              $('#slider-wrapper').css('visibility','hidden');

              // hide/remove the scenario results.  Note: the variable does not exist, until after the scenario is run!
              var exists = false;
              try {
                  eval(scenario_result);
                  exists = true;
              } catch(e) {
                  exists = false;
              }
              if (exists){
                $('#display-results').attr("class","none").empty();
              }

            }   // closes the else


            // bind all the clicked paths to the class .active
            g.selectAll("path")
                .classed("active", centered && function(d) { return d === centered; });

            g.transition()
                .duration(750)
                .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")scale(" + k + ")translate(" + -x + "," + -y + ")")
                .style("stroke-width", 1.5 / k + "px");
      }

};



//  event listener.  Takes the state entered by the user, and triggers the creation of the county map.
  function get_state_and_draw_map(evt){
    $('#topomap').empty();
    var state_name = $('#enter-state input').val();
    console.log(state_name);
    var entered_state_abbv = state_name_to_abbv[state_name];
    make_topojson_map_counties(entered_state_abbv);
    $('#instructions').css('visibility','visible');
  }

  $('#get-data-draw-map').on("click",get_state_and_draw_map);




////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////
// DONUT CHART /////////////////////////////////////////////////////////////

  var make_donut = function(data0){

    // MAKE THE IDEA OF THE SVG

        var width = 170,
            height = 170,
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


    // TODO:  add data labels to each arc in the donut.
          // var g = svg.append("g");

      //   g.append("text")
      // .attr("transform", function(d) { return "translate(" + arc.centroid(d) + ")"; })
      // .attr("dy", ".35em")
      // .style("text-anchor", "middle")
      // .text(function(d) { return d.data.age; })


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




////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////
  // SCENARIO RESULT -- EVENT HANDLING /////////////////////////////


function runScenario(evt){
  evt.preventDefault();
  console.log("runScenario js function");

  $.ajax('scenario-result', {
    type: 'POST',
    data: JSON.stringify(fuel_mix),
    contentType: 'application/json',
    success: function(data, status, result){
      scenario_result = JSON.parse(result.responseText);
      $('#instructions').empty();
      $('#display-results').css('visibility','visible');
      $('#see-results').css('visibility','visible');
      $('#display-results').attr("class",scenario_result[county_name][0]).text(scenario_result[county_name][1]);

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

