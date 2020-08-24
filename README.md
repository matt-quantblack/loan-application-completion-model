# Loan Application Modelling System (LAMS)

This application takes a list of loan application data and produces a ranked list of customers, 
who did not complete a loan application, that are more likely to complete the loan application on follow up.


This is achieved by analysing the supplied data, building clustering, logistic regression and random forest machine 
learning models in an automated process and then predicting the best customers to chase to complete their application. 

## Getting Started

Simply pull the project from this repository to your local computer:
```
https://github.com/matt-quantblack/loan-application-completion-model
```

### Prerequisites

A python interpreter is required.

The requirements.txt file contains all the required packages.


### Installing

After downloading the project install the dependencies ideally in a virtual environment.

```
pip install -r requirements.txt
```
Run the application (Will launch a web browser for the GUI)
```
python app.py
```

## Deployment

This system has not been built for deployment. The system is intended to run on a single machine
for a single user.

Please install a web server if deploying as a web app.

## Built With

* [Flask](https://flask.palletsprojects.com/en/1.1.x/) 

## Contributing

This is a university project and contributions will not be accepted

## Authors

* **Matthew Bailey** 

## License

This project is licensed under the MIT License 

## Acknowledgments

The other team members involved with research, documentation and the installation package

* Ben Burke - User docs
* Jamie Resasco - Research
* Rusty O'Hara - Installer and Installation docs