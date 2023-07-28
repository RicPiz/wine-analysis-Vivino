# wine-analysis-Vivino
This project is partitioned into three key phases: scraping the Vivino website for data extraction, data analysis through Data Analysis and Machine Learning techniques, and development of a script that suggests the ideal wine based on user-defined preferences.

The initial segment of this endeavor involved creating multiple scraping programs intended to gather data on the wines listed on the Vivino e-commerce site. The starting point was to amass URLs related to wines. For this purpose, a target page was chosen on which all wines, sorted by color (red or white), are listed, with filters applied directly on the site for country (Italy) and price range (from minimum to maximum). A Javascript script was then utilized from the browser console to retrieve all URLs from the selected page. These were subsequently stored in a text file.

The next step was to author a program capable of accessing all the saved URLs, extracting the desired data, and storing it in a csv file. Geographic coordinate information (latitude and longitude), where available, was also collected from the wineries. In conclusion, a program was devised to gather reviews for each wine. Bottle images of 3500 unique wines were downloaded, each named after the corresponding wine.

A preliminary analysis was subsequently performed regarding price distributions under different configurations and wine structure characteristics.

The locations of the wineries were plotted on an Italian regional map, obtained from the ISTAT website. A plot was also created showcasing the distribution of different types of wine. The two plots were then combined to allow for filtering by both region and type of wine.

The subsequent phase was dedicated to review analysis. A list of terminology typically employed by wine connoisseurs for the sensory analysis and description of wines was provided by Roberto Marangoni, a bioinformatics professor at the University of Pisa. These terms were collated into lists, and their frequency within the text field of a review was quantified, considering only reviews exceeding 20 words. Texts were not preprocessed, as it was assumed that these terms would appear in the text in their original form (e.g., "straw yellow", "structured", "angular"). Reviews containing at least seven unique technical terms were categorized as expert reviews, with all others classified as amateur reviews.

A cluster analysis was subsequently conducted based on the taste structure type for the two categories of white and red wines, utilizing the k-means algorithm. Label clustering was also performed to identify potential correlations between the wine structure and the type of label affixed to the bottle. The k-medoids algorithm was chosen for this task, as it selects actual data points as centers (medoids), offering more interpretability of cluster centers than k-means, where the center is not necessarily one of the input data points, but rather the average of the points in the cluster.

In conclusion, a script was composed which, via a system of filters, recommends the best wine according to user preferences.
