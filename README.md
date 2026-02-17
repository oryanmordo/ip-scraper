Design and implement a system, performing very basic OSINT (Open Source Intelligence) on a given IP Address. Meaning, this system will get an IP Address as an input, fetch multiple online API’s and aggregate the responses to a single response.



Specs



[] The system will expose an HTTP API that enables to pass a single IP Address as an input.

[] The system will return an HTTP response with JSON data at body.

[] Response JSON will consist of two parts:



a. Raw data - responses as it fetched from these 2 sources:

b. Metrics - how much time took to fetch each one of the 2 sources.



[] The system will cache responses for 10 seconds.



Documentation for API’s can be found here:



ip-api - https://ip-api.com/docs/api:json

ipinfo - https://ipinfo.io/developers/ipinfo-api



What you need to do?



Implement a component that will query the 2 API’s following the above specs.

Example:



For the example we will simulate this address as an input - 176.228.193.161.



Your system will get this request - http://127.0.0.1/176.228.193.161

To the response from the first api you will need to send this http://ip-api.com/json/176.228.193.161



Some tips:

[] metrics - in the total section: *if one fails all fails*

[] cache implementation - cache needs to support 10 seconds (be fast and efficient)

[] Build for scale - Now its only 2 APIs, but in the future it can be a lot of apis.



Must wins:

[] Output

[] Caching



Output example:



output = 
{
  "metrics": {
    "ip-api": {
      "status": "succsess",
      "time": "1"
    },
    "bgview": {
      "status": "succsess",
      "time": "2"
    },
    "total": {
      "status": "succsess",
      "time": "2"
    }
  },
  "raw_data": {
    "ip-api": {
      "response": "hello world"
    },
    "bgview": {
      "response": "hello world"
    }
  }
}