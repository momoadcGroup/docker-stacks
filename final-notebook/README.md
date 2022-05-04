# Final Touches For the PySpark on Openshift Notebooks

This repo consists the final touches to make the pyspark notebook be production ready and available to use by users. 

The dockerfile includes:

- packages needed for the communication with the kubernetes api
- spark related extensions (git, juplab-3, proxy)
- additional extensions for Qol