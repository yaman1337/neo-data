# Near Earth Objects (NEO) Data Compilation

This repository contains compiled data of Near Earth Objects (NEOs) using two NASA APIs. The data is saved in a JSON format for easy access and analysis, preventing the need to make repeated API requests and avoiding rate limits.

## Data Sources

1. **NEO Information**  
   Retrieved from the [NASA NEO API](https://api.nasa.gov/neo/rest/v1/neo/browse).  
   URL: `https://api.nasa.gov/neo/rest/v1/neo/browse?page={page}&size=20&api_key={apiKey}`  
   This API provides general information about each NEO.

2. **Orbital Data**  
   Retrieved from the [NASA JPL Small-Body Database API](https://ssd-api.jpl.nasa.gov/doc/sbdb.html).  
   URL: `https://ssd-api.jpl.nasa.gov/sbdb.api?sstr={neoId}`  
   This API provides detailed orbital parameters for each NEO, using `neoId` as the search parameter.

## JSON Structure

The data from both APIs is compiled into a JSON object with the following structure:

```json
[
  {
    "neoInfo": {
      // NEO data from NASA NEO API
    },
    "orbitalData": {
      // Orbital data from JPL Small-Body Database API
    }
  }
]
