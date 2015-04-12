# TopoE
<br>

<p>Learn more about the developer: <a href="https://www.linkedin.com/in/denisewiedl">www.linkedin.com/in/denisewiedl</a></p>
<br>

<p>If you flip a light switch at this moment, what type of power would you be using? TopoE answers this for users in California. Across the United States, TopoE brings visibility into the geographic relevancy of a state or county's fuel mix (gas, coal, solar, wind and nuclear). The app also provides a scenario calculator to help bring awareness to energy policy by simulating different policy decisions.</p>
<br>

<h5>Current Fuel Mix in California</h5>
<p>(CAISO electric grid API and web scraper, sci-kit Linear Regression, d3.js)</p>

<p><img src="https://raw.githubusercontent.com/wiedld/TopoE/master/static/img/CA_CurrentFuelMix.png" alt="CurrentFuelMix" style="max-width:75%; padding: 20px; border: 1px solid #DDD;"></p>
<br>

<h5>Fuel Mix per State/County, with Scenario result</h5>
<p>(EIA open data, pandas, decision tree, d3.js objects w/ cached data tied to AJAX callbacks)</p>

<p><img src="https://raw.githubusercontent.com/wiedld/TopoE/master/static/img/Counties_FuelMix_Scenario.png" alt="CurrentFuelMix" style="box-sizing: border-box; width:75%; padding: 20px; border: 1px solid #DDD;"></p>
<br>


<h3>Technologies</h3>

<p>TopoE is built upon open data provided by the federal government (EIA) and the California electric grid (CAISO). Technologies include python (flask, pandas), javascript (D3, AJAX, JQuery), SQLAlchemy and a PostGres database, a tasks package (web scraping, CAISO api) to be triggered by cron or celery, a calculations package used by the flask router (pandas data munging, binary decision tree, machine learning), HTML5, CSS, jinja.</p>
<br>

<h5>Calculating Scenarios with a BDT</h5>

<p>Binary decision trees are a quick way to assess several conditions, in order to reach the conclusion (the leaves). For the "Run Scenario" feature, the fuel mix is compared (at each node level) to a predetermined threshold for the fuel mix in order to determine the outcome.</p> 

<p>The left and right child nodes correspond to below or above each threshold (respectively), for each part of the fuel mix. Node iteration occurs through recursion, with the final leaf being return up through each recursive function (bubbling up the stack) in order to be the final result returned.</p>

<p>The binary decision tree is easily expanded upon with additional conditions, as necessary, and returns both the outcome and the alert state (for css class).</p>

<p>(Below is an example of a Scenario ran with excess solar, without smart inverters.)</p>
<p><img src="https://raw.githubusercontent.com/wiedld/TopoE/master/static/img/Counties_ChangeFuelMix.png" alt="CurrentFuelMix" style="box-sizing: border-box; width:75%; padding: 20px; border: 1px solid #DDD;"></p>
<br>

<h5>Basic Machine Learning</h5>

<p>The current fuel mix for California is based upon a combination of realtime data (obtained via web scraping), historic data (obtained via API or uploaded from csv), and machine learning (scikit linear regression).</p>

<p>There are three data points available every 5-10 minutes in realtime via the California electric grid (CAISO): the amount of solar, the amount of wind, and the total amount of power needed (system demand). The remaining fuel mixture was calculated using a two-layer linear regression model.</p>

<p>Hourly historic data is available for hydro and nuclear, and had a realtime % predicted based upon the current solar, wind, and system demand. Natural gas, coal, and the remaining fuels were predicted based upon the available governmental dataset which are based upon the monthly production history.</p>

<p>Prior to production release, the linear regression models may be updated using additional variables with likely correlation, (e.g. fuel pricing, LMP, etc), which are available on a 5 minute to hourly basis from CAISO.</p>
<br>

<h5>Open Data, Web scrapers, and API</h5>

<p>Data is a central feature of this web application. Obtaining, storing, rapid data munging, and selective choice of data structures - these are the essential considerations in the software architecture.</p>

<p>The source of this data is a combination of federally available datasets from the Energy Information Administration (EIA), and the California electric grid (CAISO). Raw data formats were csv, zipped xmls from API calls, and web scraped elements. Persistent data was stored in a sqlite3 database (to be upgraded to PostGreSQL for deployment), with fast retrieval via raw SQL(scrubbed inputs) instead of an ORM query, and then pandas dateframes for rapid munging.</p>

<p>Two packages were created, in order to keep a clear seperation of functional modules - a feature which makes for easier code navigation and maintenance. A tasks package to the modules which obtain data and/or update the database, and a calculations package for programs which perform data munging and calculations.</p>
<br>
