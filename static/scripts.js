// DATA STRUCTURE -- FOR TESTING /////////////////////////////////////

var fuel_mix = {
  "Alameda": {"gas":20, "coal":20, "solar":20, "wind":20, "other":20},
  "Alpine": {"gas":20, "coal":20, "solar":20, "wind":20, "other":20},
  "Amador": {"gas":20, "coal":20, "solar":20, "wind":20, "other":20},
  "Butte": {"gas":20, "coal":20, "solar":20, "wind":20, "other":20},
  "Calaveras": {"gas":20, "coal":20, "solar":20, "wind":20, "other":20},
  "Colusa": {"gas":20, "coal":20, "solar":20, "wind":20, "other":20},
  "Contra Costa": {"gas":20, "coal":20, "solar":20, "wind":20, "other":20},
  "Del Norte": {"gas":20, "coal":20, "solar":20, "wind":20, "other":20},
  "El Dorado": {"gas":20, "coal":20, "solar":20, "wind":20, "other":20},
  "Fresno": {"gas":20, "coal":20, "solar":20, "wind":20, "other":20},
  "Glenn": {"gas":20, "coal":20, "solar":20, "wind":20, "other":20},
  "Humboldt": {"gas":20, "coal":20, "solar":20, "wind":20, "other":20},
  "Imperial": {"gas":20, "coal":20, "solar":20, "wind":20, "other":20},
  "Inyo": {"gas":20, "coal":20, "solar":20, "wind":20, "other":20},
  "Kern": {"gas":20, "coal":20, "solar":20, "wind":20, "other":20},
  "Kings": {"gas":20, "coal":20, "solar":20, "wind":20, "other":20},
  "Lake": {"gas":20, "coal":20, "solar":20, "wind":20, "other":20},
  "Lassen": {"gas":20, "coal":20, "solar":20, "wind":20, "other":20},
  "Los Angeles": {"gas":20, "coal":20, "solar":20, "wind":20, "other":20},
  "Madera": {"gas":20, "coal":20, "solar":20, "wind":20, "other":20},
  "Marin": {"gas":20, "coal":20, "solar":20, "wind":20, "other":20},
  "Mariposa": {"gas":20, "coal":20, "solar":20, "wind":20, "other":20},
  "Mendocino": {"gas":20, "coal":20, "solar":20, "wind":20, "other":20},
  "Merced": {"gas":20, "coal":20, "solar":20, "wind":20, "other":20},
  "Modoc": {"gas":20, "coal":20, "solar":20, "wind":20, "other":20},
  "Mono": {"gas":20, "coal":20, "solar":20, "wind":20, "other":20},
  "Monterey": {"gas":20, "coal":20, "solar":20, "wind":20, "other":20},
  "Napa": {"gas":20, "coal":20, "solar":20, "wind":20, "other":20},
  "Nevada": {"gas":20, "coal":20, "solar":20, "wind":20, "other":20},
  "Orange": {"gas":20, "coal":20, "solar":20, "wind":20, "other":20},
  "Placer": {"gas":20, "coal":20, "solar":20, "wind":20, "other":20},
  "Plumas": {"gas":20, "coal":20, "solar":20, "wind":20, "other":20},
  "Riverside": {"gas":20, "coal":20, "solar":20, "wind":20, "other":20},
  "Sacramento": {"gas":20, "coal":20, "solar":20, "wind":20, "other":20},
  "San Benito": {"gas":20, "coal":20, "solar":20, "wind":20, "other":20},
  "San Bernardino": {"gas":20, "coal":20, "solar":20, "wind":20, "other":20},
  "San Diego": {"gas":20, "coal":20, "solar":20, "wind":20, "other":20},
  "San Francisco": {"gas":20, "coal":20, "solar":20, "wind":20, "other":20},
  "San Joaquin": {"gas":20, "coal":20, "solar":20, "wind":20, "other":20},
  "San Luis Obispo": {"gas":20, "coal":20, "solar":20, "wind":20, "other":20},
  "San Mateo": {"gas":20, "coal":20, "solar":20, "wind":20, "other":20},
  "Santa Barbara": {"gas":20, "coal":20, "solar":20, "wind":20, "other":20},
  "Santa Clara": {"gas":20, "coal":20, "solar":20, "wind":20, "other":20},
  "Santa Cruz": {"gas":20, "coal":20, "solar":20, "wind":20, "other":20},
  "Shasta": {"gas":20, "coal":20, "solar":20, "wind":20, "other":20},
  "Sierra": {"gas":20, "coal":20, "solar":20, "wind":20, "other":20},
  "Siskiyou": {"gas":20, "coal":20, "solar":20, "wind":20, "other":20},
  "Solano": {"gas":20, "coal":20, "solar":20, "wind":20, "other":20},
  "Sonoma": {"gas":20, "coal":20, "solar":20, "wind":20, "other":20},
  "Stanislaus": {"gas":20, "coal":20, "solar":20, "wind":20, "other":20},
  "Sutter": {"gas":20, "coal":20, "solar":20, "wind":20, "other":20},
  "Tehama": {"gas":20, "coal":20, "solar":20, "wind":20, "other":20},
  "Trinity": {"gas":20, "coal":20, "solar":20, "wind":20, "other":20},
  "Tulare": {"gas":20, "coal":20, "solar":20, "wind":20, "other":20},
  "Tuolumne": {"gas":20, "coal":20, "solar":20, "wind":20, "other":20},
  "Ventura": {"gas":20, "coal":20, "solar":20, "wind":20, "other":20},
  "Yolo": {"gas":20, "coal":20, "solar":20, "wind":20, "other":20},
  "Yuba": {"gas":20, "coal":20, "solar":20, "wind":20, "other":20}
};



///////////////////////////////////////////////////////////////////////
//  SLIDERS, with src js script import in html DOM, before this js file


var set_slider_values = function(v1,v2,v3,v4,v5,county_name){

    var axis = d3.svg.axis().orient("top").ticks(5);

    d3.select('#slider1').call(d3.slider().axis(axis)
      .value(v1)
      .on("slide", function(evt, value1) {
        d3.select('#slider1text').text(value1);
        fuel_mix[county_name]["gas"] = value1;
      }
    ));

    d3.select('#slider2').call(d3.slider().axis(axis)
      .value(v2)
      .on("slide", function(evt, value2) {
        d3.select('#slider2text').text(value2);
        fuel_mix[county_name]["coal"] = value2;
      }
    ));

    d3.select('#slider3').call(d3.slider().axis(axis)
      .value(v3)
      .on("slide", function(evt, value3) {
        d3.select('#slider3text').text(value3);
        fuel_mix[county_name]["solar"] = value3;
      }
    ));

    d3.select('#slider4').call(d3.slider().axis(axis)
      .value(v4)
      .on("slide", function(evt, value4) {
        d3.select('#slider4text').text(value4);
        fuel_mix[county_name]["wind"] = value4;
      }
    ));

    d3.select('#slider5').call(d3.slider().axis(axis)
      .value(v5)
      .on("slide", function(evt, value5) {
        d3.select('#slider5text').text(value5);
        fuel_mix[county_name]["other"] = value5;
      }
    ));

    // show the starting values in the html
    d3.select('#slider1text').text(v1);
    d3.select('#slider2text').text(v2);
    d3.select('#slider3text').text(v3);
    d3.select('#slider4text').text(v4);
    d3.select('#slider5text').text(v5);
};



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

              // display the c3 donut, with county-specific data.
              make_donut();

              // display the d3 sliders, with county-specific data.
                // make visible
                  $('#slider-wrapper').css('visibility','visible');
                // get ride of old sliders & values.
                  $('#slider1').empty();
                  $('#slider2').empty();
                  $('#slider3').empty();
                  $('#slider4').empty();
                  $('#slider5').empty();
                // re-make sliders with new values
                  var value1 = fuel_mix[county_name]["gas"],
                      value2 = fuel_mix[county_name]["coal"],
                      value3 = fuel_mix[county_name]["solar"],
                      value4 = fuel_mix[county_name]["wind"],
                      value5 = fuel_mix[county_name]["other"];
                  set_slider_values(value1, value2, value3, value4, value5, county_name);

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
// DONUT CHART /////////////////////////////////////////////////////////////










  // C3 donut ////////////////////////////////////////////////////

      var make_donut = function(){
            var chart = c3.generate({
              data: {
                  columns: [
                      ['Natural gas', 30],
                      ['data2', 120],
                  ],
                  type : 'donut',
                  onclick: function (d, i) { console.log("onclick", d, i); },
                  onmouseover: function (d, i) { console.log("onmouseover", d, i); },
                  onmouseout: function (d, i) { console.log("onmouseout", d, i); }
              },
              donut: {
                  title: "Fuel Mix in County"
              },
              bindto: document.getElementById('fuel-donut')
            });

            setTimeout(function () {
                chart.load({
                    columns: [
                        ["setosa", 0.2, 0.2, 0.2, 0.2, 0.2, 0.4, 0.3, 0.2, 0.2, 0.1, 0.2, 0.2, 0.1, 0.1, 0.2, 0.4, 0.4, 0.3, 0.3, 0.3, 0.2, 0.4, 0.2, 0.5, 0.2, 0.2, 0.4, 0.2, 0.2, 0.2, 0.2, 0.4, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.2, 0.2, 0.3, 0.3, 0.2, 0.6, 0.4, 0.3, 0.2, 0.2, 0.2, 0.2],
                        ["versicolor", 1.4, 1.5, 1.5, 1.3, 1.5, 1.3, 1.6, 1.0, 1.3, 1.4, 1.0, 1.5, 1.0, 1.4, 1.3, 1.4, 1.5, 1.0, 1.5, 1.1, 1.8, 1.3, 1.5, 1.2, 1.3, 1.4, 1.4, 1.7, 1.5, 1.0, 1.1, 1.0, 1.2, 1.6, 1.5, 1.6, 1.5, 1.3, 1.3, 1.3, 1.2, 1.4, 1.2, 1.0, 1.3, 1.2, 1.3, 1.3, 1.1, 1.3],
                        ["virginica", 2.5, 1.9, 2.1, 1.8, 2.2, 2.1, 1.7, 1.8, 1.8, 2.5, 2.0, 1.9, 2.1, 2.0, 2.4, 2.3, 1.8, 2.2, 2.3, 1.5, 2.3, 2.0, 2.0, 1.8, 2.1, 1.8, 1.8, 1.8, 2.1, 1.6, 1.9, 2.0, 2.2, 1.5, 1.4, 2.3, 2.4, 1.8, 1.8, 2.1, 2.4, 2.3, 1.9, 2.3, 2.5, 2.3, 1.9, 2.0, 2.3, 1.8],
                    ]
                });
            }, 1500);

            setTimeout(function () {
                chart.unload({
                    ids: 'data1'
                });
                chart.unload({
                    ids: 'data2'
                });
            }, 2500);
      };

