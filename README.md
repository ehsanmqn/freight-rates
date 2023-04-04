# Xeneta Rates Task
I developed this Django project as part of the task assigned by Xenata. I chose to utilize Django as the Python framework for two primary reasons:
1. Django is more productive than other python frameworks
2. It is well-structured

## Used Technologies

 - Django
 - Django Rest Framework (DRF)

## Deployment

### Docker
The project includes a docker-compose file that specifies the necessary requirements for deploying the project using docker containers. To run the project with docker, navigate to the project root and execute the following command:
```bash
docker-compose up --build
```

### Manual
If you prefer to manually run the project, start PostgreSQL as instructed in the task. Next, modify the database host in settings.py to localhost. Finally, execute the following commands in the project root directory:
```bash 
pip install -r requirements.txt
python manage.py collectstatic
python manage.py runserver 0.0.0.0:8000
```

## Projects structure
Within this project, I implemented three models pertaining to the Price, Port, and Region entities. However, these models do not have any relevance to the current task since the tables they create within Django possess different names than those provided by the task. I included these models solely to provide a unit tests for models. The following sections outline several enhancements to the schema of the database provided by the task.

To implement the API required for this task, I utilized two distinct APIViews to provide 2 different APIs. Within this document, I will furnish detailed explanations for both of these Views. I opted against using GenericViews or ViewSets for this particular task, as APIView is better suited for simple APIs and allows for straightforward flexibility.

To retrieve data for the two APIs under the Price model, I utilized two primary SQL queries. The subsequent sections offer additional details and data regarding these queries.

## Usage
To access the APIs provided by this project, navigate to http://127.0.0.1:8000/ within your preferred browser. As Django is configured to operate in DEBUG mode, you will encounter a yellow "Page not found" page that specifies various routes offered by the project.

It is important to note that there is a critical aspect within the task specifications that must be taken into account:

The task mandates that the API must return a list with the average prices `for each day` on a route between port codes origin and destination. Moreover, the API should return a null value for `days` in which fewer than three prices exist (Including zero - which means no data exist in prices table). Based on these specifications, I determined that even if no prices or paths exist between two specified ports or regions, the API should still provide null data. This approach is correct from the perspective of the user, as when a user selects two locations and specifies a time frame, the backend must still provide null data for the designated time to the frontend to ensure proper plotting.

Within this project, I opted to furnish two distinct endpoints for the same task. Following I provide explanations regarding these endpoints.

### List Daily Average Price V1
The specified endpoint displays the average daily prices for a particular range of dates and designated ports or regions. A Swagger-like documentation page is available for each endpoint, including this one, which can be accessed via the following address:

```html
http://127.0.0.1:8000/api/v1/rates/?date_from=2016-01-01&date_to=2016-01-10&origin=CNSGH&destination=north_europe_main
```
This page includes instructions on how to utilize the endpoint and input data into it.

To ensure appropriateness, I modified the endpoint's response structure to include three distinct keys: code, message, and result. Here's an example response you can expect from this endpoint:

```json
{
    "code": 200,
    "message": "Operation successful",
    "result": [
        {
            "day": "2016-01-01",
            "average_price": 1112
        },
        {
            "day": "2016-01-02",
            "average_price": 1112
        },
        {
            "day": "2016-01-03",
            "average_price": null
        }
    ]
}
```

### List Daily Average Price V2
This endpoint also displays the average daily prices for a particular range of dates and designated ports or regions, similar to the first endpoint. However, it's the second version of this API and utilizes a distinct query structure.

use follwoing address to access the second endpoint API:
```html
http://127.0.0.1:8000/api/v2/rates/?date_from=2016-01-01&date_to=2016-01-10&origin=CNSGH&destination=north_europe_main
```

The difference between these two APIs is that the initial endpoint incorporates two distinct SQL queries within its neighboring serializer (ListDailyAveragePriceInputSerializerV1) to authenticate the Origin and Destination codes. This enables us to deliver the appropriate response to the user if the codes or slugs are not present in the database. 

Conversely, the List Daily Average Price V2 API does not verify the Origin and Destination codes and slugs in the database. Instead, it returns null for complete days based on the user-provided start and end dates. Here's an example response for a similar scenario from the second endpoint:

Here's an example request parameters and 2 responses for this scenario:

```html
?date_from=2017-01-10&date_to=2017-01-11&origin=CNSGH&destination=lmnop
```

List Daily Average Price V1 response:

```json
{
    "destination": [
        "Invalid destination port symbol."
    ]
}
```

List Daily Average Price V2 response:

```json
{
    "code": 200,
    "message": "Operation successful",
    "result": [
        {
            "day": "2017-01-10",
            "average_price": null
        },
        {
            "day": "2017-01-11",
            "average_price": null
        }
    ]
}
```

## Spent time
As requested in the task instructions, I am providing the time I spent on this task. I spent approximately 2 hours working on the core components and some tests for both models. It took an additional hour to add the remaining tests. However, the most challenging aspect of this task was figuring out how to provide the data as per the database structure and considering all edge cases. Therefore, it took me some time (2 or 3 hour) to update my queries, find special cases and test against them, and ensure that the data was provided accurately. 
Overall, I spent 1 day on this task because it was important for me alot.

## How I did it
In this section, I will provide some details about the process I followed to complete the task. Specifically, I will focus on the queries, which I found to be the most challenging aspect of this project.

The updated API (API V2) now considers the port/region geohierarchy problem. This means that it is now able to take into account the fact that ports and regions are organized into a hierarchical structure, and that a port or region may be a child of another port or region.

To handle this problem, I have updated the query to include two common table expressions (CTEs) that generate the lists of origin and destination codes based on the input regions:

```sql
WITH geohierarchy AS (
    WITH RECURSIVE cte AS (
        SELECT l.slug FROM regions l WHERE l.slug IN ('{0}', '{1}')
        UNION
        SELECT r.slug FROM regions r
        INNER JOIN cte ON cte.slug = r.parent_slug
    )
    SELECT * FROM cte
),
daily_average_prices AS (
    SELECT prices.day, 
        CASE
            WHEN COUNT(prices.price) >= 3 THEN COALESCE(ROUND(AVG(prices.price)), NULL)
        END AS average_price
    FROM prices
    JOIN ports orig_port ON prices.orig_code = orig_port.code
    JOIN ports dest_port ON prices.dest_code = dest_port.code
    WHERE (prices.orig_code = '{0}' OR orig_port.parent_slug IN (SELECT slug FROM geohierarchy))
        AND (prices.dest_code = '{1}' OR dest_port.parent_slug IN (SELECT slug FROM geohierarchy))
    GROUP BY prices.day
)
SELECT DATE(dates.day) AS day, dap.average_price
FROM (
    SELECT generate_series('{2}'::date, '{3}'::date, '1 day') AS day
) AS dates
LEFT JOIN LATERAL (
    SELECT dap.average_price FROM daily_average_prices dap WHERE dap.day = dates.day
) dap ON true;
```

These CTEs use a recursive query to traverse the hierarchical structure of the ports and regions table and generate a list of all ports that are children (directly or indirectly) of the input origin and destination regions.
This updated query now takes into account the hierarchical structure of the data and generates the correct list of origin and destination codes to filter for.

## Improvement to the schema
Currently, the `ports` table contains a `parent_slug` column that references the `regions` table. 
However, the `regions` table also contains a `parent_slug` column that references itself. This creates 
a circular reference that can be difficult to manage. To improve the structure of the database, consider 
normalizing the data so that each table only references other tables in a one-to-many relationship.

Following is a normalized version for the regions:

```sql
region_id (primary key)
region_name
parent_region_id (foreign key references region_id)
```

A normalized table for ports with the following columns:
```sql
port_id (primary key)
port_code
port_name
region_id (foreign key references region_id)
```

A normalized table for prices with the following columns:
```sql
price_id (primary key)
orig_port_id (foreign key references port_id)
dest_port_id (foreign key references port_id)
price_day
price_amount
```
By normalizing the tables in this way, we can eliminate the circular reference between the "regions" 
and "ports" tables. We can also simplify the structure of the "prices" table by using foreign keys to 
reference the "ports" table.

Note that this is just one example of how the tables could be normalized, and the specific details of 
the normalization process will depend on the requirements of the application and the relationships 
between the data entities.

## Tests
For this small project, I created a total of 30 tests. It's worth noting that the tables generated by Django based on the models are not the same as those provided in the project's database.
While these models were not directly applicable to the project's purpose, I added them to the project to write tests for them as a way to showcase my ability to create effective tests for models.

In addition to the model tests, I also wrote 15 tests for `ListDailyAveragePriceV1` to demonstrate my proficiency in creating unit tests for views.

In order to run tests, the best way is to run the provided database using docker, change the `settings.py` database configuration, then run the following command insode the project directory.

```shell
python manage.py makemigrations
python manage.py migrate
python manage.py test
```

Following cases considered during unit tests and manual tests:
1. Test with invalid values for origins and destinations - For example, passing in empty strings, strings with special characters or symbols, or strings that do not correspond to any valid ports or regions.  (PASSED)
2. Test with invalid date ranges - For example, passing in an end date that is earlier than the start date, or passing in dates that are outside the range of valid dates for the database. (PASSED)
3. Test with multiple origins and destinations - The query should be able to handle scenarios where multiple origins and destinations are specified. (NOT APPLICABLE: At the moment the query only accept one origin, and one destination. Providing more origins, and destinations, the serializer only consider the last one. However, by some changes in serializer and corresponding query it is possible to support multiple origins and destination. I did not have this as not requested in the task specification)
4. Test with different combinations of valid and invalid origins and destinations. (PASSED)
5. Test with missing data - For example, the query should be able to handle scenarios where there is no price data available for a given origin-destination pair or a specific date. Test with different combinations of missing data. (PASSED - Sample scenarion: date_from=2016-01-01&date_to=2016-01-10&origin=china_main&destination=north_europe_main)
6. Test with large datasets - The query should be able to handle large datasets efficiently without causing performance issues or timeouts. Test with datasets that contain a large number of ports, regions, and price data. (NOT APPLICABLE - No database for this scenario provided)
7. Test with special characters in the input data - For example, test with origins or destinations that have special characters or symbols in their names or codes. (PASSED)
8. Test with non-existent origins or destinations - Test with origins or destinations that do not exist in the database. (PASSED)
9. Test with duplicate data - Test with scenarios where there are duplicate entries in the database for ports, regions, or prices. (PASSED)
10. Test with null values - Test with scenarios where there are null values in the database for ports, regions, or prices. (Tested only with 2 regions that have null parent slugs)
11. Test with overlapping date ranges - Test with scenarios where the date range specified in the query overlaps with other date ranges in the database. (PASSED)
## End
Feel free to visit my [Github profile](https://github.com/ehsanmqn) where I have shared a few projects to check out.

Happy coding :tada: :tada: :tada: 