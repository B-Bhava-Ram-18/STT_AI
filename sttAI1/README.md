# Box Office Bombs Data Pipeline

Course page: https://nipunbatra.github.io/stt-ai-26/lectures.html

## Assignment Overview

This project builds an end-to-end data pipeline for collecting, cleaning, validating, enriching, and analyzing data about major box-office failures.

The pipeline scrapes movie data from Wikipedia, validates and cleans the raw values using Pydantic, enriches each movie with metadata from the OMDb API, performs consistency checks between sources, categorizes movies by financial loss, and exports a final analysis-ready CSV dataset.

## Problem Statement

The goal was to create a structured dataset from messy real-world web data. The source table contains movie titles, release years, production budgets, and estimated losses, but the raw data includes issues such as:

- Footnotes and reference markers
- Special symbols such as streaming/currently-playing markers
- Currency symbols
- Budget and loss ranges
- Nested Wikipedia table headers
- Missing or unavailable API metadata

## Technologies Used

- **Python**: Main programming language
- **requests**: Fetching Wikipedia pages and OMDb API responses
- **BeautifulSoup**: Parsing HTML and extracting table data
- **Pydantic**: Data validation and field-level cleaning
- **Pandas**: DataFrame creation, analysis, and CSV export
- **OMDb API**: Movie metadata enrichment

## Pipeline Steps

### 1. Web Scraping

The Wikipedia page for the biggest box-office bombs is fetched using `requests`.

BeautifulSoup is then used to parse the HTML and locate the main movie table. The pipeline extracts:

- Raw movie title
- Raw release year
- Raw production budget
- Raw estimated loss

Each movie record is initially stored as a dictionary.

### 2. Data Validation And Cleaning

A Pydantic model named `MovieData` is used to convert messy scraped data into clean typed fields:

- `title`: cleaned movie title
- `year`: integer release year
- `budget_millions`: production budget as a float
- `loss_millions`: estimated loss as a float

The validators handle:

- Removing footnotes such as `[nb 2]`
- Removing special symbols such as `§` and `†`
- Removing currency symbols
- Converting ranges such as `$100-160` into an average value
- Converting year strings into integers

### 3. OMDb API Enrichment

For each validated movie, the OMDb API is queried using the movie title and year.

The following fields are added:

- Plot
- Metascore
- IMDb rating
- Director
- Language
- OMDb year

If a movie is not found or a field is returned as `N/A`, the pipeline stores `None` instead of dropping the row.

### 4. Data Consistency Check

The Wikipedia year is compared with the OMDb year.

Each row receives one of three statuses:

- **Verified**: Wikipedia and OMDb years match within a tolerance of plus or minus 1 year
- **Mismatch**: The years differ by more than 1 year
- **Not Found**: OMDb did not return a valid year

### 5. Final Dataset Creation

The enriched data is converted into a final Pandas DataFrame and exported as:

```text
box_office_failures.csv
```

The final dataset contains:

- Title
- Year
- Director
- Language
- Budget_Millions
- Loss_Millions
- Loss_Category
- IMDb_Rating
- Metascore
- Match_Status

## Loss Categories

Movies are categorized based on estimated financial loss:

- **Catastrophic**: Loss greater than or equal to $100M
- **Severe**: Loss between $50M and $100M
- **Moderate**: Loss less than $50M

## Results

The notebook produced the following results:

- Total movies scraped: **139**
- Successfully validated records: **139**
- Failed validations: **0**
- Verified OMDb matches: **137**
- OMDb records not found: **2**

Loss category distribution:

- Severe: **85 movies**
- Catastrophic: **46 movies**
- Moderate: **8 movies**

Summary statistics:

- Average production budget: approximately **$129.55M**
- Average estimated loss: approximately **$91.92M**
- Maximum estimated loss: **$218M**

The movie with the highest estimated loss in the dataset was **The Marvels**, with an estimated loss of approximately **$218M**.

## Key Learnings

This project demonstrates practical data engineering skills required before applying AI or machine learning techniques:

- Collecting data from web sources
- Parsing HTML tables
- Handling noisy and inconsistent real-world data
- Validating data using schemas
- Working with external APIs
- Handling missing API responses gracefully
- Performing source consistency checks
- Creating clean analysis-ready datasets

## Possible Improvements

Future improvements could include:

- Moving the OMDb API key to an environment variable
- Adding retry logic and timeout handling for API requests
- Caching OMDb responses to avoid repeated API calls
- Writing unit tests for parsing and validation functions
- Saving both raw and cleaned datasets for better reproducibility
- Adding visualizations for budget, loss, rating, and category trends

## Interview Summary

This project is an end-to-end data pipeline that transforms unstructured web data into a clean, enriched, and analysis-ready dataset. It combines web scraping, data validation, API integration, consistency checking, and exploratory analysis using Python tools commonly used in AI and data workflows.
