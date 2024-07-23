# CS50 Web (version 2020)

## Table of contents

- [CS50 Web (version 2020)](#cs50-web-version-2020)
  - [Table of contents](#table-of-contents)
  - [General info](#general-info)
    - [Description](#description)
    - [Prerequisites (Only for project 1 and beyond)](#prerequisites-only-for-project-1-and-beyond)
    - [Setup](#setup)
    - [Projects](#projects)
      - [1. Project 0 (Search)](#1-project-0-search)
      - [2. Project 1 (Wiki)](#2-project-1-wiki)
      - [3. Project 2 (Commerce)](#3-project-2-commerce)
      - [4. Project 3 (Mail)](#4-project-3-mail)
      - [5. Project 4 (Network)](#5-project-4-network)
      - [6. Capstone](#6-capstone)
  - [Deployment](#deployment)
  - [Vscode extensions](#vscode-extensions)

## General info

### Description
   > Solutions for [CS50W's Projects(version 2020)](https://cs50.harvard.edu/web/2020/)

### Prerequisites (Only for project 1 and beyond)
   * Python 3.7 or greater
   * Django 3.x

### Setup 
1. To make sure that you have install python 3 please open terminal(powershell, cmd ...) and simply type.
   * If you install only python3
   ```bash
   python --version
   ```
   * If you have 2 version of python.
   ```bash
   python3 --version
   ```
2. Create virtual environment
   ```bash
   python -m venv {your-virtual-env-name}
   ```
3. Activate venv for current terminal
   * Linux
   ```bash
   source /your-virtual-env-path-that-you-create/Scripts/activate
   ```
   * Windows
      * powershell
      ```powershell
      .\your-virtual-env-path-that-you-create\Scripts\activate.ps1
      ```
      * cmd
      ```batch
      .\your-virtual-env-path-that-you-create\Scripts\activate.bat
      ```
4. Install Django
   ```sh
   pip install Django
   ```
   Or using requirement file which is included for each project
   ```sh
   pip install -r {requirement-file}
   ```
5. Verify Django installation
   ```sh
   django-admin --version 
   ```
      
### Projects

#### [1. Project 0 (Search)](Search)
   * Description
   > Design a front-end for Google Search, Google Image Search, and Google Advanced Search. More details about project see [this link](https://cs50.harvard.edu/web/2020/projects/0/search/)
   * [Video Demo](https://www.youtube.com/watch?v=NIXez8okMbs)
 
#### [2. Project 1 (Wiki)](Wiki) 
   * Description
   > Design a Wikipedia-like online encyclopedia. More details about project see [this link](https://cs50.harvard.edu/web/2020/projects/1/wiki/)
   * [Video Demo](https://www.youtube.com/watch?v=qYIjgQsfsfg)

#### [3. Project 2 (Commerce)](Commerce)
   * Description
   > Design an eBay-like e-commerce auction site that will allow users to post auction listings, place bids on listings, comment on those listings, and add listings to a “watchlist.”. More details about project see [this link](https://cs50.harvard.edu/web/2020/projects/2/commerce/)
   * Project [Demo](https://commerce-50w.herokuapp.com/)(deployment)
   * [Video Demo](https://www.youtube.com/watch?v=sN0wIE_tghw)

#### [4. Project 3 (Mail)](Mail)
   * Description
   > Design a front-end for an email client that makes API calls to send and receive emails. More details about project see [this link](https://cs50.harvard.edu/web/2020/projects/3/mail/)
   * [Video Demo](https://www.youtube.com/watch?v=rbipMVPtDQE)

#### [5. Project 4 (Network)](Network)
   * Description
   > Design a Twitter-like social network website for making posts and following users. More details about project see [this link](https://cs50.harvard.edu/web/2020/projects/4/network/)
   * [Video Demo](https://www.youtube.com/watch?v=mZwGtA9GS_E)

#### 6. Capstone
   * Description
   > Comming soon.
   * [Video Demo](Final-Project)(Comming soon)

## Deployment 
> See this [link](Deploy-Guide)

## Vscode extensions
1. ms-python.python
2. ms-python.vscode-pylance
3. batisteo.vscode-django
