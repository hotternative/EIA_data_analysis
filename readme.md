
Parsing of Short-Term Energy Outlook of EIA

##Data Download and Parse
### parse.py

####`first_run()` 
creates csv files from stratch. The csv files are submitted in `ep/csv/`

#### `update(year, month, download)` 
is created to make it easy to run for 
new forecast updates when they are published.

It updates all csv files (as provided in the submission)
with a new EIA file, identified by year and month. The `download` param is a 
boolean:
* set to True to download the file from EIA 
* set to False to find and used a file already downloaded into `./resources/`


Note:
Original Excel files were downloaded into `resources/` 
but not included in the submission due to their big size. 

### utils.py
A collection of util functions assisting the downloading and parsing.

### config.py
A collection of configurations for the downloading and parsing.


##Analysis
### `analyze.py`
A collection of demo analysis.
#### `analyze_all()`
produces the raw error (actual - prediction) in USD (dollar) values as well 
as in percentage changes (actual / prediction - 1), at 12 time horizons: 1-month ahead, 2-months ahead, and so on, up to 12-
months. The results are saved in `ep/error_csv/`.

#### `analysis_demo1(interest, time_horizon)`
Plot out the raw forecast error in percentage for 
a given interest and a given time horizon.

I run this demo against WTI on the 1 month time horizon. 
The plot result is submitted as `WTI_1M_Error_percentage.png`. 

Having examined the plot, it seems there is no apparent overall bias between 
the forecast and the actual price.

It can be seen, however, there is a period of positive bias during the 2008 Financial Crisis 
where the actual price is significantly lower than the prediction  

There is no apparent trend of the variance of the error. It could be because 
there has been no significant change to the underlying model used for prediction. 
However, on this point, it's necessary to run other interests on other time horizons to be more conclusive.

The highest absolute percentage error occured during the COVID pandamic, 
probably as a result of high volotility at that time. 
   
    
#### `analysis_demo2(interest)`
Find the mean absolute error for each time horizon for a given interest.

I run this demo against WTI on the 1 month time horizon.
The the mean absolute error increases as the time horizon increases. 
This follows common sense that the further future we predict, the less accurate it becomes.

 
 
 
 







 

