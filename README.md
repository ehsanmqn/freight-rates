# Xeneta Rates Task
I developed this Django project as part of the task assigned by Xenata. I chose to utilize Django as the Python framework for two primary reasons:
1. Django is more productive than other python frameworks
2. It is well-structured

## Used Technologies

 - Django
 - Django Rest Framework (DRF)

## Deployment

The project includes a docker-compose file that specifies the necessary requirements for deploying the project using a docker. To run the project with docker, navigate to the project root and execute the following command:
```bash
docker-compose up --build
```

If you prefer to manually run the project, start PostgreSQL as instructed in the task. Next, modify the database host in settings.py to localhost. Finally, execute the following commands in the project root directory:
```bash 
pip install -r requirements.txt
python manage.py collectstatic
python manage.py runserver 0.0.0.0:8000
```

## Projects structure
Within this project, I implemented three models pertaining to the Price, Port, and Region entities. However, these models do not have any relevance to the current task since the tables they create within Django possess different names than those provided by the task. I included these models solely to provide a unit tests for models. The following sections outline several enhancements to the schema of the database provided by the task.

To implement the two API required for this task, I utilized two distinct APIViews. Within this document, I will furnish detailed explanations for both of these Views. I opted against using GenericViews or ViewSets for this particular task, as APIView is better suited for simple APIs and allows for straightforward flexibility.

To retrieve data for the two APIs under the Price model, I utilized two primary SQL queries. The subsequent sections offer additional details and data regarding these queries.

## Usage
To access the APIs provided by this project, navigate to http://127.0.0.1:8000/ within your preferred browser. As Django is configured to operate in DEBUG mode, you will encounter a yellow "Page not found" page that specifies various routes offered by the project.

Within this project, I opted to furnish two distinct endpoints for the same task. However, it is important to note that there is a critical aspect within the task specifications that must be taken into account:

The task mandates that the API must return a list with the average prices `for each day` on a route between port codes origin and destination. Moreover, the API should return a null value for `days` in which fewer than three prices exist (Including zero - which means no data exist in prices table). Based on these specifications, I determined that even if no prices or paths exist between two specified ports or regions, the API should still provide null data. This approach is correct from the perspective of the user, as when a user selects two locations and specifies a time frame, the backend must still provide null data for the designated time to the frontend to ensure proper plotting.

Following I provide explanations regarding these endpoints.

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

The initial endpoint incorporates two distinct SQL queries within its neighboring serializer (ListDailyAveragePriceInputSerializerV1) to authenticate the Origin and Destination codes. This enables us to deliver the appropriate response to the user if the codes or slugs are not present in the database. Here's an example response for this scenario:

```html
http://127.0.0.1:8000/api/v1/rates/?date_from=2016-01-10&date_to=2016-01-11&origin=asd&destination=sdfg
```
```json
{
    "origin": [
        "Invalid origin port symbol."
    ],
    "destination": [
        "Invalid destination port symbol."
    ]
}
```

Conversely, the List Daily Average Price V2 API does not verify the Origin and Destination codes and slugs in the database. Instead, it returns null for complete days based on the user-provided start and end dates. Here's an example response for a similar scenario from the second endpoint:

```json
{
    "code": 200,
    "message": "Operation successful",
    "result": [
        {
            "day": "2016-01-01",
            "average_price": null
        },
        {
            "day": "2016-01-02",
            "average_price": null
        },
        {
            "day": "2016-01-03",
            "average_price": null
        },
        {
            "day": "2016-01-04",
            "average_price": null
        }
    ]
}
```

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
## Spent time
As requested in the task instructions, I am providing the time I spent on this task. I spent approximately 2 hours working on the core components and some tests for both models. It took an additional hour to add the remaining tests. However, the most challenging aspect of this task was figuring out how to provide the data as per the database structure and considering all edge cases. Therefore, it took me some time (2 or 3 hour) to update my queries, find special cases and test against them, and ensure that the data was provided accurately. 

## How I did it
In this section, I will provide some details about the process I followed to complete the task. Specifically, I will focus on the queries, which I found to be the most challenging aspect of this project.

Initially, I used the following query to retrieve the data. However, the issue with this query is that it doesn't include days where there are no prices for the two designated locations.

```sql
SELECT day, CASE WHEN COUNT(*) < 3 THEN NULL ELSE AVG(price) END AS average_price 
FROM prices 
WHERE orig_code IN origin_codes 
AND dest_code IN destination_codes
AND day BETWEEN from_date AND to_date 
GROUP BY day
```

I made some modifications to the query to address this problem, and the resulting query was similar to the following. To resolve the previous issue, I generated a time table and used a LEFT JOIN with prices.

```sql
SELECT DATE(dates.day) AS day, COALESCE(AVG(prices.price), NULL) AS average_price 
FROM (SELECT generate_series(from_date::date, to_date::date, '1 day') AS day) AS dates 
LEFT JOIN prices ON prices.orig_code IN origin_codes 
AND prices.dest_code IN destination_codes 
AND DATE(prices.day) = dates.day 
WHERE dates.day BETWEEN from_date::date AND to_date::date 
GROUP BY dates.day 
HAVING COUNT(prices.price) >= 3 OR COUNT(prices.price) = 0 
```

The previous query does not take into account paths with only 1 or 2 prices, nor does it consider the parent_slugs column. As a result, I had to modify the query further, and the following query resolved these issues.

```sql
WITH  origin_codes AS (
    SELECT code FROM ports
    RIGHT JOIN regions ON regions.slug = ports.parent_slug
    WHERE regions.parent_slug = '{0}' 
        OR ports.parent_slug = '{0}' 
        OR ports.code = '{0}'
), dest_codes AS (
    SELECT code FROM ports
    RIGHT JOIN regions ON regions.slug = ports.parent_slug
    WHERE regions.parent_slug = '{1}' 
        OR ports.parent_slug = '{1}' 
        OR ports.code = '{1}'
  )
SELECT DATE(dates.day) AS day, 
CASE 
    WHEN COUNT(prices.price) >= 3 THEN COALESCE(ROUND(AVG(prices.price)), NULL)
END AS average_price
FROM (
    SELECT generate_series('{2}'::date, '{3}'::date, '1 day') AS day
) AS dates
LEFT JOIN prices ON prices.orig_code IN (SELECT code FROM origin_codes)
                AND prices.dest_code IN (SELECT code FROM dest_codes)
                AND DATE(prices.day) = dates.day
WHERE dates.day BETWEEN '{2}'::date AND '{3}'::date
GROUP BY dates.day
```

Currently, I'm using the above SQL query inside the Price model. However, I made some optimizations to improve the query's readability and functionality. The optimized version of above query is as follows (I haven't pushed the project with the following query in my code due I did edge tests based on the above query.)

```sql
WITH origin_codes AS (
  SELECT code FROM ports
  RIGHT JOIN regions ON regions.slug = ports.parent_slug
  WHERE regions.parent_slug = '{0}' 
      OR ports.parent_slug = '{0}' 
      OR ports.code = '{0}'
), dest_codes AS (
  SELECT code FROM ports
  RIGHT JOIN regions ON regions.slug = ports.parent_slug
  WHERE regions.parent_slug = '{1}' 
      OR ports.parent_slug = '{1}' 
      OR ports.code = '{1}'
), date_range AS (
  SELECT day::date
  FROM generate_series('{2}'::date, '{3}'::date, '1 day') AS day
)
SELECT d.day, 
  CASE 
      WHEN COUNT(p.price) >= 3 THEN COALESCE(ROUND(AVG(p.price)), NULL)
      ELSE NULL
  END AS average_price
FROM date_range AS d
LEFT JOIN prices p ON p.orig_code IN (SELECT code FROM origin_codes)
                  AND p.dest_code IN (SELECT code FROM dest_codes)
                  AND p.day = d.day
WHERE d.day BETWEEN '{2}'::date AND '{3}'::date
GROUP BY d.day;
```

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

## End
Feel free to visit my [Github profile](https://github.com/ehsanmqn) where I have shared a few projects to check out.

Happy coding :tada: :tada: :tada: 