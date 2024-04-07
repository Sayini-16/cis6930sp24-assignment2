##DATASHEET
##Data Augmentation and Contextual Enrichment of Police Incident Reports Dataset

##Motivation

- **Purpose of the DataSet:**
       - Transparency, public education, research and analysis capabilities, administrative and legal demands, and community involvement were probably the main reasons for creating the dataset. It makes local incidents easier to track, contributes to public safety, helps with policy-making, and improves police department accountability.

Funding Sources and Grant Details for Dataset Creation:
The local government of Norman, Oklahoma most likely provides funding for the dataset, which is a daily incident report from the Norman Police Department. These kinds of datasets are usually supported by the city's budget, which includes public monies allotted to public safety and law enforcement, and are a normal aspect of police department operations.

Composition

Dataset Composition and Instance Types Description:
A particular occurrence or case that the Norman Police Department handled on a particular day is described in detail by each of the instances in the dataset, which are recorded police events. Certain details about the occurrence, such as its nature, time and place, and potential participants or results, are probably included in these cases. As a unified collection of event-based records, the dataset does not include numerous types of instances; rather, it is limited to occurrences.

Dataset Completeness and Sampling Methodology:
The dataset provides a thorough overview of the events of a given day in Norman since it contains all police occurrences that have been reported for that day. It is a full daily log, not a selection.

Instance Data Composition: Raw Information:
An incident's date, time, location, unique incident number, nature description, and Incident ORI are all included in each dataset instance. These are the raw, structured data that make up each instance. With a tabular format for ease of understanding and analysis, this data is unprocessed.

Content Sensitivity and Potential Offensiveness in Dataset:
The dataset contains sensitive event data that may be upsetting, but it is presented objectively, with an emphasis on public safety and awareness, and without any derogatory or offensive information.

Human-Related Aspects Within the Dataset:
The collection does, in fact, pertain to persons as it records police events that include people or groups, including welfare checks, traffic stops, disturbances, and other encounters with law enforcement. Documents that describe events affecting or involving members of the community are by their very nature human subjects.

Collection

Data Acquisition Methods and Validation for Each Instance: 
Law enforcement officials directly observed and reported the occurrences they came across or dealt with, providing the data. Although precise validation techniques are not described in depth in the dataset information supplied, validation most likely incorporates police department protocols to verify record correctness.

Human-centric Elements in the Dataset: 
The collection does, in fact, pertain to persons because it records instances involving contacts between people or groups and law enforcement. These events might involve a range of encounters, including welfare checks, traffic stops, disruptions, and other community-based police enforcement operations.

Data Collection Mechanisms and Validation Procedures: 
The Python script used for the project's data collection visited and extracted information from the public police department websites that were listed. This required utilizing online scraping methods to retrieve information from HTML sites or communicating directly with police department-provided APIs to retrieve event logs. Verifying the extracted information's completeness and correctness against the original source or doing quality control tests on the extraction code to make sure it correctly extracts the required data are two ways to validate the data gathering process.



Preprocessing/cleaning/labeling

Data Preprocessing and Cleaning Procedures: ]
Given that the dataset included a police department's daily event summary, preparation and cleaning were necessary to guarantee data consistency and usefulness. This includes resolving missing or incorrect data entries, standardizing date and time formats, and parsing and extracting pertinent information from unstructured language, such incident reports. PYPDF2 and regex are used in these phases for the extraction and processing standards.

Uses

Previous Utilization of the Dataset for Tasks: 
Because it is a real-time, public resource, this dataset is now being utilized for academic reasons for the CIS 6930 course. These types of datasets are primarily used for a variety of purposes, including public safety evaluations, trend detection, policy-making assistance, criminology research, and law enforcement investigations. 

Considerations for Future Use Due to Dataset Composition and Collection Processes:
The composition, collecting, preprocessing, and labeling procedures of the dataset may have an influence on its future academic applications. Preprocessing processes or labeling standards that are not properly documented or standardized may have an impact on the reproducibility and comparability of study findings. Transparency in data gathering procedures is critical for assuring the reliability and validity of future academic studies and applications.

Distribution

Intellectual Property Rights and Distribution Terms for the Dataset:
The dataset may be released under a copyright or other intellectual property (IP) licence, together with the associated conditions of use (ToU) that govern its use. These conditions would outline how the dataset may be accessed, used, shared, and credited while adhering to legal and ethical issues around data ownership and use rights.

Maintenance
Responsibility for Supporting, Hosting, and Maintaining the Dataset: 
The entity or organisation that developed or gathered the data is most likely responsible for the dataset's support, hosting, and upkeep. In this scenario, it would be the Norman Police Department or the appropriate administrative organisation in charge of keeping law enforcement records in the Norman, Oklahoma region.

Support and Maintenance of Older Versions of the Dataset: 
The choice to support, host, and maintain previous versions of the dataset would be based on the entity's policy and resources. As of today, the daily event summary report is being maintained for the last two months, as well as the weekly and monthly incident reports for the past three years.
