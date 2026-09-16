## Data Dictionary for Cleaned Tenancy Services Rental Bond Datasets

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
| ```Geometric Mean Rent```             | ```float```    |             |            | The geometric mean is calculated by multiplying values together and taking the nth root of the result. When a variable is log-normally distributed (a common distribution for variables that must be greater than 0) the geometric mean will closely approximate the median.
| ```Log Std Dev Weekly Rent```         | ```float```    |             | ```yes```  | Sample standard deviation of natural logarithm weekly rent of bonds lodged within the period.
| ```TA2019```                          | ```str```      | ```yes```   | ```yes```  | TA2019 Name value, mapped to by SA2-2019 codes
| ```WARD2019```                        | ```list[str]```|             | ```yes```  | WARD2019 Name values, mapped to by SA2-2019 codes

## Cleaning Decisions

### Location ID
```Location Id``` was retained because it is required for geolocating the data. ```Location Id``` entries
may appear as ```-99``` or ```NULL```.

#

#### ```-99```

It is assumed that this is some sort of Market Rent API error code that was returned by the
Tenancy Services Database. This can be asserted by plotting the frequency of occurences over time and noticing
the jump in frequency during  periods of [data migration](https://www.tenancy.govt.nz/about-tenancy-services/data-and-statistics/rental-bond-data/).

![error-code-occurences-over-time](../../../../data/figures/99-code-occurences-over-time.png)

#

#### ```NULL```

The best assumption is that these are anonymised lodgings with Tenancy Services mentioned In the [privacy statement](./bonds_dict.md) given by MBIE.

#

#### Conclusion
These rows were removed as they represent a very small proportion of the data, and imputation may be difficult due
to the amount of SA2-2019 codes that exist.

#

### Missing Rental Statistics

#### ```Log Std Dev Weekly Rent```
The most commonly missing rental statistic is ```Log Std Dev Weekly Rent```.

This occurs for a series of reasons:

 - If location id is missing
   - ```Log Std Dev Weekly Rent``` will not be calculated. *more on this later*

 - Otherwise if there is no variation in the rental statistics
   - This is quite common, as rental prices tend to cluster towards whole numbers of 5 and 10.
   It is also common for locations-dwelling type pairs with very few bonds lodged and with too little variation. ```Log Std Dev Weekly Rent``` will be missing, even though it should be ```0```. *note: The naming suggests that
   the standard deviation is calculated before taking the natural log, with zero variance that would give undefined anyway.*

 - Finally if no weekly rent statistics are present in the database.
   - *This is only conjecture, but all three of these conditions coverall cases completely*

### Missing Statistics Over Time

plotting occurrences of missing statistics over time produces the following figure.

![](../../../../data/figures/reported-statistics-over-time.png)

It is inperceivable on this graph however note that there is no variation between each statistic. ```Log Std Dev Weekly Rent``` is always 0 in the cases that these statistics are missing or identical with no variation.

#### Takeaway

```Geometric Mean Rent```, ```Upper Quartile Rent```, ```Lower Quartile Rent```, ```Median Rent```, and```Log Std Dev Weekly Rent``` are all missing at random.

#### Imputation

missing values of ```Log Std Dev Weekly Rent``` and ```Geometric Mean Rent``` where chosen to be imputed and retained in the cleaned dataset. The other statistical values are to be left out to prevent overly reinforcing bias in the data

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
