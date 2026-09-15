## Introduction

The [Tenancy Services](https://www.tenancy.govt.nz/about-tenancy-services/data-and-statistics/rental-bond-data/) website provides detailed quarterly data on rental bonds within New Zealand.

The files provided are for 'private-sector' bonds. The data is reported by geographic location, dwelling type and number of beds, together with statistics on weekly rent figures.

| Field                                 | Type           | Categorical | Calculated | Description
| ------------------------------------- | -------------- | ----------- | ---------- | -----------
| ```TimeFrame```                       | ```date```     |             |            | Period end date specified in ISO-8602 format. The dataset is reported by quarter.
| ```Location Id```                     | ```int```      | ```yes```   |            | SA2-2019 location code.
| ```Dwelling Type```                   | ```string```   | ```yes```   |            | The type of dwelling.
| ```Number Of Beds```                  | ```int```      |             |            | Number of bedrooms.
| ```Total Bonds```                     | ```int```      |             |            | Number of bonds lodged at some point in the period.  Note random rounding is applied to this value.
| ```Active Bonds```                    | ```int```      |             |            | Total number of bonds active at the end of the period.  Note random rounding is applied to this value.
| ```Closed Bonds```                    | ```float```    |             |            | Number of bonds closed at some point in the period.  Note random rounding is applied to this value.
| ```Median Rent```                     | ```float```    |             |            | Median weekly rent; weekly rent of the bond that is at the 50th percentile of bonds lodged in the period. 
| ```Geometric Mean Rent```             | ```float```    |             |            | The geometric mean is calculated by multiplying values together and taking the nth root of the result. When a variable is log-normally distributed (a common distribution for variables that must be greater than 0) the geometric mean will closely approximate the median.
| ```Upper Quartile Rent```             | ```float```    |             |            | Synthetic Upper Quartile Weekly Rent.  This is defined as ```exp(lmean + qnorm(0.75) * lsd)``` and is a reasonable estimate of the upper quartile.
| ```Lower Quartile Rent```             | ```float```    |             |            | Synthetic Lower Quartile Weekly Rent.  This is defined as ```exp(lmean + qnorm(0.25) * lsd)``` and is a reasonable estimate of the lower quartile.
| ```Log Std Dev Weekly Rent```         | ```float```    |             | ```yes```  | Sample standard deviation of natural logarithm weekly rent of bonds lodged within the period.

## Data Recorded for New Zealand

Tenancy Services is a part of the [Ministry of Business, Innovation & Employment](https://www.mbie.govt.nz/), which provides a [Market Rent API](https://portal.api.business.govt.nz/api/market-rent) that interfaces directly with Tenancy Services bond database.

## In the case of the New Zealand Dataset, and other clarifications

### ```Dwelling Type```
Categories bonds into different types of Dwellings.

 - ```Apartment```
 - ```Boarding House```
 - ```Flat```
 - ```House```
 - ```Room```
 - ```ALL```
 
 (ALL is for statistics across all Dwelling Types. In most cases if the dwelling type is not entere din a bond lodgement the dwelling is assumed to be a house).

### ```Number Of Beds```

Can take the values: 1, 2, 3, 4, 5+, NA (NA means Not Available)

### ```Log Std Dev Weekly Rent``` 

it should be noted that the log normal distribution is a better fit for market rent than the standard normal distribution. In addition the values for rent tend to cluster around multiples of $10 so that the trend, over time, for the lower and upper quartiles and median can remain flat for significant periods of time.  Because of this ```Geometric Mean Rent``` and ```Log Std Dev``` are more useful than the mean and std for modelling and the "Synthetic" (lower quartile and upper quartile) statistics, which are estimates of the lower quartile and upper quartile derived from the log normal distribution, are better behaved indicators of change.

Note however, the synthetic lower quartile (slq) tends to slightly underestimate the lower quartile (lq) while the synthetic upper quartile (suq) slightly over estimates the upper quartile (uq). 

One side effect of using the ```Log Std Dev``` is that for statistical areas that have; one or less bond lodgment, identically valued bond lodgments; then the calculated ```Log Std Dev``` value will be undefined, as a result of 0 variance in the sample population when it should be 0.

## Privacy Protection

Privacy is protected by the following mechanisms:

 - Suppression: Any summary statistics where the number of bonds lodged in the period is less than 5 are suppressed

 - Random rounding: All (unsuppressed) counts (nlodged, nClosed ,nCurr) are also randomly rounded to a number divisible by three as follows:

   - If the values is already a multiple of three it is unchanged, otherwise:

   - it is rounded to the nearest multiple of three with a probability of two-thirds (applied approximately two-thirds of the time)

   - it is rounded to the second closest multiple of three with a probability of one-third (applied approximately one-third of the time).

The random rounding protects against the recalculation of small counts from differencing large counts and retains almost all of the statistical properties of the table by adding only a little noise to the larger counts.  Note also that each value in a table is rounded independently, including the totals. This means that the marginal totals can differ slightly from the corresponding sum of the rows or columns, i.e. if the columns or rows in a table are added, they will not always equal the total given. 

## Sources:

[Tenancy Services Rental Bond Data](https://www.tenancy.govt.nz/about-tenancy-services/data-and-statistics/rental-bond-data/)

[MBIE API portal](https://portal.api.business.govt.nz/)

[SA22019 generalised by StatsNZ](https://datafinder.stats.govt.nz/layer/98970-statistical-area-2-2019-generalised/)
