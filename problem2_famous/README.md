Data Science Essentials Challenge (Fall 2014)
=============================================

(Source https://university.cloudera.com/user/digital_content/download/78451cf1-1988-3a78-be96-19b27546e011)

Problem 2: Almost Famous
-------
Congratulations! You have just published your first book on data science, advanced analytics, and predictive modeling. You’ve decided to use your skills as a data scientist to create and optimize a website promoting your book, and you have started several ad campaigns on a popular search engine in order to drive traffic to your site.

Almost Famous Data set
-------
There are three actions that visitors can take once they arrive at the site: they can order a copy of your book (which earns you $4), they can sign up for your data science email newsletter (which earns you $0.40-per-signup), or they can click on one or more ads you have placed on your site for data science training materials ($0.10 per ad-click). You are logging each event that visitors do on your website, including the keyword and the ID of the ad campaign that brought your visitor to the website and any subsequent actions (adclick, signup, or order) that they performed during their visit. These events are written in JSON format and are available [here](data/).

Along with your ad campaigns, you are running a pair of simultaneous A/B tests on the site. The first pair (experiment one vs. experiment two) tests two different color schemes for the site: a blue one and a green one. The second pair (experiment three vs. experiment four) tests two different promotional blurbs for your book: one from Josh Wills, and one from Sean Owen. Visitors to the site are diverted into the experiments independently using a per-experiment hashing function on a cookie that is placed on the visitor’s browser, so you can assume that visitors will always be in the same experiment no matter how many times they come back to the site. There are no preexisting expectations that either experiment in either pair is more likely to be effective than the other.

Almost Famous Deliverables
-------
Using your skills in data munging and statistical analysis, answer the following questions about the performance of your site using the log data as your source of truth.

1. Your advertisers have notified you that there is a bot network which has been plaguing your site. You can find a representative sample of logs from bot activity in the spam.log file. Calculate the number of distinct visitors (not distinct visits) who are bots in the logs. Exclude all events from those bot users from your answers to all of the following questions.
1. What is the overall clickthrough rate of the ads (ad clicks per visit)?
1. Which combination of query string and campaign had the highest mean value of orders per visitor? 
For each combination of query string and campaign, what is the standard deviation of the number of orders? (You should calculate n x m standard deviations, where n is the number of query strings, and m is the number of campaigns.)
1. Compute the overall newsletter signup rate (defined as the number of users who signed up to the newsletter divided by the total number of users) for each of the experiments. 
Use a G-test to compare the performance of experiment one vs. experiment two and experiment three vs. experiment four overall.
How many full days of data, starting from the first day, are required to determine that the newsletter signup rate for experiment one is better than experiment two at the 99% confidence level? For example, if you can claim that experiment one is better with 99% confidence using only the first day’s data (9/15/14) and half the second day’s data (9/16/14), then 2 full days are required.
1. Given the revenue-per-action values above for buying a copy of the book, signing up for the newsletter, and clicking on an ad, calculate the mean revenue earned per visit for each experiment.
Using a z-test, determine how many full days of data, starting from the first full day, are needed to confirm that experiment four earns more revenue than experiment three at the 99% confidence level. For example, if you can claim that experiment four is better with 99% confidence using only half the first day’s data (9/15/14), then one full day is required.

The answers to the questions asked in the five parts of the problem must be placed in a file called problem2.json with the following contents:

	{
	    "1": {
	        "number_of_distinct_visitors_that_are_bots": <# bots>
	    },
	    "2": {
	        "overall_as_click_through_rate": <# Ad clicks/Visit: 0.0-1.0>
	    },
	    "3": {
		"highest_mean_value": {
	            "campaign": "<Campaign>",
	            "query_string": "<Query String>"
		},
		"standard_deviations": [
	            {
	                "campaign": "<Campaign>",
	                "query_string": "<Query String>",
	                "standard_deviation": <Stddev>
	            },
	            ...
	            {
	                "campaign": "<Campaign>",
	                "query_string": "<Query String>",
	                "standard_deviation": <Stddev>
	            }
	        ]
	    },
	    "4": {
	        "overall_signup_rate": {
			"experiment1": <Rate>,
			"experiment2": <Rate>,
			"experiment3": <Rate>,
			"experiment4": <Rate>
	        },
	        "performance_of_experiment_1_versus_2": <Performance>,
	        "performance_of_experiment_3_versus_4": <Performance>,
	        "number_of_full_days_for_confidence": <# Days>
	    },
	    "5": {
	        "mean_revenue_per_visit": {
			"experiment1": <Mean Revenue>,
			"experiment2": <Mean Revenue>,
			"experiment3": <Mean Revenue>,
			"experiment4": <Mean Revenue>
	        },
	        "number_of_full_days_for_confidence": <# Days>
	    }
	}

The values marked with angular brackets (<...>) must be replaced with your answers to the challenge problem questions. (The angular brackets must be removed/replaced as well.) The resulting file must be a valid JSON document.


:arrow_right: Solution abstract: [docs/solution_abstract_famous.pdf](docs/solution_abstract_famous.pdf)

:arrow_right: Solution file: [out/problem2.json](out/problem2.json)

:arrow_right: Source code: [src](src)


Generate Deliverables
-------

Pack the solution files for upload with

	cd /tmp
	git clone https://github.com/comsysto/ds_challenge_fall2014.git
	cd ds_challenge_fall2014/
	grep ":arrow_right:" problem2_famous/README.md | cut -d' ' -f2- > tmp && mv tmp problem2_famous/README.md
	tar -zcf problem2_famous.tar.gz problem2_famous/README.md problem2_famous/docs/*.pdf problem2_famous/out/problem2.json problem2_famous/src
	cd ..
	rm -rf ds_challenge_fall2014


Solution requirements / Used software
-------



