Data Science Essentials Challenge (Fall 2014)
=============================================

(Source https://university.cloudera.com/user/digital_content/download/78451cf1-1988-3a78-be96-19b27546e011)

Problem 3: WINKLR
-------
Winklr is a curiously popular social network for fans of the sitcom Happy Days. Users can post photos, write messages, and most importantly, follow each other’s posts and content. This helps users keep up with new content from their favorite users on the site.

To help its users discover new people to follow on the site, Winklr is building a new machine learning system, called the Fonz, to predict who a given user might like to follow.

WINKLR Data
-------
Phase one of the Fonz project is underway. The engineers can export the entire user graph as tuples. For example, the tuple “user1,user2” means that user1 follows user2. (user2 does not necessarily follow user1 in this case.)

Furthermore, an engineer has examined users who click frequently on other users who they do not already follow. She has created a data set with a large number of “user1,user2” tuples, where user1 has clicked frequently on user2’s content but does not yet follow user2.

You have joined the Fonz project to implement Phase two, which improves on this result. Given the user graph and the list of frequent-click tuples [here](data/), you will select a subset of those frequent-click tuples that look most promising. These tuples must be the “user1,user2” tuples where you believe user1 is mostly likely to want to follow user2, given the information in the user graph.

You have been asked to select 70,000 tuples. These tuples will be used in an email campaign, inviting the targeted users to follow the users you recommend.

WINKLR Deliverables
-------
The 70,000 most liking pairs must be placed in a CSV file called problem3.csv, with one “user1,user2” pair on each line (without quotes). The pairs must be in order of most likely to want to connect to least likely to want to connect, i.e. the first line of the file should contain the pair of IDs that are most likely to want to connect, and the last line should contain the pair of IDs that are least likely (of the 70,00 selected) to want to connect.

Solution Abstract:
-------
Explain your methodology including approach, assumptions, software and algorithms used, testing and validation techniques applied, model selection criteria, and total time spent.

:arrow_right: Solution abstract: [docs/solution_abstract_winklr.pdf](docs/solution_abstract_winklr.pdf)

:arrow_right: Solution file: [out/problem3.csv](out/problem3.csv)

:arrow_right: Source code: [src](src)


Generate Deliverables
-------

Pack the solution files for upload with

	helpers/pack problem3_winklr

Solution requirements / Used software
-------


