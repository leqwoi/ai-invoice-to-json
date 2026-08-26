---
language:
- en
license: apache-2.0
size_categories:
- 1K<n<10K
task_categories:
- text-classification
- token-classification
- zero-shot-classification
- feature-extraction
- text-generation
pretty_name: Company Documents
tags:
- finance
dataset_info:
  features:
  - name: file_content
    dtype: string
  - name: file_name
    dtype: string
  - name: extracted_data
    dtype: string
  - name: document_type
    dtype: string
  - name: chat_format
    list:
    - name: content
      dtype: string
    - name: role
      dtype: string
  splits:
  - name: train
    num_bytes: 5959141
    num_examples: 2469
  download_size: 1228494
  dataset_size: 5959141
configs:
- config_name: default
  data_files:
  - split: train
    path: data/train-*
---

### Company Documents Dataset

#### Overview

This dataset comprises a comprehensive collection of over 2,000 company documents, categorized into four primary types: invoices, inventory reports, purchase orders, and shipping orders. Each document is provided in PDF format, along with a CSV file containing the text extracted from these documents, their respective labels, and the word count of each document. This dataset is well-suited for various natural language processing (NLP) tasks, such as text classification, information extraction, and document clustering. The most recent update includes mapping all files on PHI3 mini to extract information in JSON format.


#### Dataset Content

- **PDF Documents**: The dataset includes 2,677 PDF files, each representing a unique company document. These documents are derived from the Northwind dataset, which is commonly used for demonstrating database functionalities.
  
  The document types are:
  - **Invoices**: Detailed records of transactions between a buyer and a seller.
  - **Inventory Reports**: Records of inventory levels, including items in stock and units sold.
  - **Purchase Orders**: Requests made by a buyer to a seller to purchase products or services.
  - **Shipping Orders**: Instructions for the delivery of goods to specified recipients.

- **Hugging Face Dataset**: The CSV file (`company-document-text.csv`, 1.38 MB) contains the following columns:
  - **text**: The extracted text content from each document.
  - **file**: File Source.
  - **label**: The category of the document (invoice, inventory report, purchase order, shipping order).
  - **Phi Response**: Extracted information from the document using LLM Phi3, presented in JSON format.
#### Data Summary

- **Total Documents**: 2,677
  
- **Word Count Range**:
  - Minimum: 23 words
  - Maximum: 472 words

#### Example Entries

Here are a few example entries from the CSV file:

- **Shipping Order**: 
  - **Order ID**: 10718
  - **Shipping Details**: "Ship Name: Königlich Essen, Ship Address: Maubelstr. 90, Ship City: ..."
  - **Word Count**: 120

- **Invoice**:
  - **Order ID**: 10707
  - **Customer Details**: "Customer ID: Arout, Order Date: 2017-10-16, Contact Name: Th..."
  - **Word Count**: 66

- **Purchase Order**:
  - **Order ID**: 10892
  - **Order Details**: "Order Date: 2018-02-17, Customer Name: Catherine Dewey, Products: Product ..."
  - **Word Count**: 26

#### Applications

This dataset can be used for:
- **Text Classification**: Train models to classify documents into their respective categories.
- **Information Extraction**: Extract specific fields and details from the documents.
- **Document Clustering**: Group similar documents together based on their content.
- **OCR and Text Mining**: Improve OCR (Optical Character Recognition) models and text mining techniques using real-world data.

#### Citation

Please cite this dataset as follows if you use it in your research:

*Ayoub Cherguelain, 2024, "Company Documents Dataset", [Kaggle](https://www.kaggle.com/datasets/ayoubcherguelaine/company-documents-dataset)*
