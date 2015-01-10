Data Science Essentials Challenge (Fall 2014)
=============================================

Problem 1: SmartFly
------
You have been contacted by a new online travel service called SmartFly. SmartFly’s business is providing its customers with timely travel information and notifications about flights, hotels, destination weather, traffic getting to the airport, and anything else that can help make the travel experience smoother. Their product team has come up with the idea of using the flight data that they have been collecting to predict whether customers’ flights will be delayed so that they can respond proactively. They’ve now contacted you to help them test out the viability of the idea.

SmartFly has only been operating for a short while, so their data set only goes back to late last year. As a test of the viability of the idea, they’d like you to use the data they have thus far collected to predict all flight delays for early next year, January 1st through January 31st, with the accuracy to be verified against the actual flights, once they happen. The goal is to proactively offer vouchers to users booked on flights that are very likely to be delayed, that can be used to purchase services at the connecting airport. Because there is a cost associated with offering the vouchers, SmartFly has asked that you give the list of delayed flights sorted in order from most likely to be delayed to least likely to be delayed. For the purposes of this challenge, a flight is considered delayed if and only if its actual departure time is after its scheduled departure time, i.e. a positive departure delay.

SmartFly Data
The SmartFly historic data set and flight plans for January can be downloaded here. The total data size is 685MB with 7.3 million historic records and 0.5 million scheduled flights. Each record is comma-delimited and has the following fields:

Unique flight ID
Year
Month (1–12)
Day of month (1–31)
Day of week (1–7)
Scheduled departure time (HHMM)
Scheduled arrival time (HHMM)
Airline
Flight number
Tail number
Plane model
Seat configuration
Departure delay (minutes)
Origin airport
Destination airport
Distance travelled (miles)
Taxi time in (minutes)
Taxi time out (minutes)
Whether the flight was cancelled
Cancellation code
The flight plan data has the same fields as the historic data, but some fields in the flight plans data do not contain values.

SmartFly Deliverables
The predictions for delay probabilities for all scheduled flights must be placed into a file called problem1.csv, with a single unique flight ID per line. The IDs must be in order of most likely to be delayed to least likely to be delayed, i.e. the first line of the file should contain the ID of the flight that is most likely to be delayed, and the last line should contain the ID of the flight that is least likely to be delayed. A flight that is canceled is not considered delayed for the purposes of this challenge.
